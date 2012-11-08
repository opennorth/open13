import lxml.html

from billy.scrape.legislators import LegislatorScraper, Legislator


class MBLegislatorScraper(LegislatorScraper):
    jurisdiction = 'mb'

    def scrape(self, term, chambers):
        index_url = 'http://www.gov.mb.ca/legislature/members/photos.html'
        doc = lxml.html.fromstring(self.urlopen(index_url))
        doc.make_links_absolute(index_url)

        for img in doc.xpath('//img')[8:]:
            try:
                url = img.getparent().attrib['href']
            except KeyError:
                try:
                    url = img.getparent().getparent().attrib['href']
                except KeyError:
                    # Aha! We have reached the end of the img list.
                    # Double check...
                    if 'alt' not in img.attrib:
                        # And we're done.
                        return

            data = dict(term=term, chamber='lower',
                full_name=img.attrib['alt'], url=url)
            data['photo_url'] = img.attrib['src']

            doc = lxml.html.fromstring(self.urlopen(url))
            doc.make_links_absolute(url)

            chunks = [s.strip() for s in doc.xpath('//td')[-4].itertext()]
            chunks = filter(None, chunks)[::-1]

            # Toss name.
            chunks.pop()

            data['district'] = chunks.pop()

            # Toss position...maybe capture later.
            if 'minister' in chunks[-1].lower():
                chunks.pop()

            data['party'] = chunks.pop()

            # Toss email cruft.
            chunks.pop()

            data['email'] = chunks.pop()

            leg = Legislator(**data)

            while True:
                try:
                    if 'office' in chunks[-1].lower():
                        self.parse_office(leg, chunks)
                    else:
                        chunks.pop()
                except IndexError:
                    print 'no more chunks'
                    break

            leg.add_source(url)
            leg.add_source(index_url)
            self.save_legislator(leg)

    def parse_office(self, leg, chunks):
        office = {}
        office_name = chunks.pop().strip(':')
        if office_name.lower() == 'office':
            office_type = 'capitol'
        else:
            office_type = 'district'

        address = []
        while 'phone:' not in chunks[-1].lower():
            address.append(chunks.pop())

        address = ' '.join(address)
        address = ' '.join(address.split())
        address = address.replace(' 450', '\n450')
        address = address.replace(' Winnipeg', '\nWinnipeg')

        phone = []
        while 'fax:' not in chunks[-1].lower():
            phone.append(chunks.pop())
        phone = ''.join(phone).replace('Phone:', '').strip()

        fax = []
        while 'office:' not in chunks[-1].lower():
            fax.append(chunks.pop())
            if not chunks:
                break
        fax = ''.join(fax).replace('Fax:', '').strip()

        office.update(phone=phone, fax=fax, address=address)
        leg.add_office(office_type, office_name, **office)
