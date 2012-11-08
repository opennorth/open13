import lxml.html

from billy.scrape.legislators import LegislatorScraper, Legislator


class SKLegislatorScraper(LegislatorScraper):
    jurisdiction = 'sk'

    def scrape(self, term, chambers):
        url = 'http://www.legassembly.sk.ca/mlas/'
        doc = lxml.html.fromstring(self.urlopen(url))
        doc.make_links_absolute(url)

        for tr in doc.xpath('//table')[1].xpath('tr')[1:]:
            leg = self.scrape_legislator(term, tr)
            leg.add_source(url)
            self.save_legislator(leg)

    def scrape_legislator(self, term, tr):
        url = tr[0].xpath('a/@href').pop()
        full_name = tr[0].xpath('a/text()').pop()
        party = tr[1].text_content()
        district = tr[2].text_content()

        data = dict(term=term, chamber='lower',
            full_name=full_name, url=url, party=party,
            district=district)
        leg = Legislator(**data)

        doc = lxml.html.fromstring(self.urlopen(url))
        doc.make_links_absolute(url)

        leg['photo_url'] = doc.xpath('//img/@src')[0]
        email = doc.xpath('//a[starts-with(@href, "mailto:")]/@href')
        if email:
            leg['email'] = email.pop()[7:]

        xpath = '//div[text()="Legislative Building Address"]'
        chunks = doc.xpath(xpath)[0].getparent().itertext()
        chunks = [s.strip() for s in chunks]
        chunks = filter(None, chunks)

        address = ' '.join(chunks[1:3])
        keys = [s.strip(': ').lower() for s in chunks[-4:][0::2]]
        numbers = dict(zip(keys, chunks[-4:][1::2]))
        leg.add_office('capitol', 'Legislative Building Office',
                       address, **numbers)

        xpath = '//div[text()="Constituency Address"]'
        chunks = doc.xpath(xpath)[0].getparent().itertext()
        chunks = [s.strip() for s in chunks]
        chunks = filter(None, chunks)

        address = chunks[1:-4]
        address.insert(-5, '\n')
        address = ''.join(address).replace(',', ', ')
        keys = [s.strip(': ').lower() for s in chunks[-4:][0::2]]
        numbers = dict(zip(keys, chunks[-4:][1::2]))

        leg.add_office('district', 'Constituency Office',
                       address, **numbers)
        leg.add_source(url)
        return leg
