import lxml.html

from billy.scrape.legislators import LegislatorScraper, Legislator
from billy.scrape.utils import clean_spaces

class BCLegislatorScraper(LegislatorScraper):
    jurisdiction = 'bc'

    def scrape(self, term, chambers):

        url = ('http://www.leg.bc.ca/mla/3-2.htm')
        doc = lxml.html.fromstring(self.urlopen(url))
        doc.make_links_absolute(url)

        row_xpath = '//img[contains(@src, "members_sm")]'
        for img in doc.xpath(row_xpath):
            data = {}
            data['photo_url'] = img.attrib['src']
            leg_url = img.getparent().attrib['href']
            leg = self.scrape_legislator(data, leg_url, term)
            leg.add_source(url, page="legislator list page")
            self.save_legislator(leg)

    def scrape_legislator(self, data, url, term):
        doc = lxml.html.fromstring(self.urlopen(url))
        doc.make_links_absolute(url)

        # Full name.
        full_name = doc.xpath('//b[starts-with(., "MLA:")]/text()').pop()
        if ':' in full_name:
            _, full_name = full_name.split(':')
        full_name.strip('Hon. ')
        full_name = clean_spaces(full_name)

        # Offices
        for xpath in [('//b[starts-with(., "MLA:")]/../'
                             'following-sibling::p/b/i/text()'),
                      ('//b[starts-with(., "MLA:")]/../'
                             'following-sibling::p/em/b/text()'),
                      ('//b[starts-with(., "MLA:")]/../'
                             'following-sibling::p/em/strong/text()'),
                      ('//b[starts-with(., "MLA:")]/../'
                             'following-sibling::p/strong/em/text()')]:
            district = doc.xpath(xpath)
            if district:
                district = district.pop()
                break

        for xpath in [('//b[starts-with(., "MLA:")]/../'
                          'following-sibling::p/b/text()'),
                      ('//b[starts-with(., "MLA:")]/../'
                          'following-sibling::p/strong/text()')]:
            party = doc.xpath(xpath)
            if party:
                party = clean_spaces(party.pop()).title()
                break

        email = doc.xpath('//a[starts-with(@href, "mailto:")]/text()').pop()

        xpath = '//p[starts-with(., "Phone:")]/../following-sibling::td[1]'
        phone = [p.text_content() for p in doc.xpath(xpath)]
        if len(phone) == 1:
            phone.append(doc.xpath('//p[starts-with(., "Phone:")]')[-1][0].tail)

        xpath = '//p[starts-with(., "Fax:")]/../following-sibling::td[1]'
        fax = [p.text_content() for p in doc.xpath(xpath)]
        if len(fax) == 1:
            fax.append(doc.xpath('//p[starts-with(., "Fax:")]')[-1][0].tail)

        xpath = '//p[starts-with(., "Toll free:")]/../following-sibling::td[1]'
        toll_free = [p.text_content() for p in doc.xpath(xpath)]

        leg = Legislator(term=term, full_name=full_name, email=email,
            district=district, party=party, chamber='lower', **data)
        leg['toll_free_phone'] = toll_free
        leg['url'] = url

        # Constituencies
        for dist_office in doc.xpath(
            '//b[contains(., "Constituency:")]'):
            dist_office = dist_office.getparent().getparent().text_content()
            _, dist_office = dist_office.split(':')
            dist_office = dist_office.strip()
            leg.add_office('district', 'constituency',
                address=dist_office,
                phone=phone.pop(), fax=fax.pop())

        # Capitol
        xpath = '//*[starts-with(., "Office:")]/../../text()'
        capitol_address = doc.xpath(xpath)
        capitol_address = '\n'.join(s.strip() for s in capitol_address)
        capitol_address = capitol_address.strip()
        leg.add_office('capitol', 'Office', address=capitol_address,
            phone=phone.pop(), fax=fax.pop())

        leg.add_source(url, page="legislator detail page")
        return leg
