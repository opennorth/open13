# -*- coding: utf-8 -*-
import itertools
import lxml.html
from billy.scrape.committees import CommitteeScraper, Committee


class CACommitteeScraper(CommitteeScraper):

    jurisdiction = 'ab'

    def scrape(self, chamber, term):
        url = 'http://www.assembly.ab.ca/net/index.aspx?p=membership_list'
        html = self.urlopen(url)
        doc = lxml.html.fromstring(html)
        doc.make_links_absolute(url)

        committees = doc.xpath('//div[@id="_ctl0_Panel_committees"]')
        divs = committees[0].xpath('div')[1:]
        for div in divs[:]:
            if 'class' in div.attrib and \
              div.attrib['class'] == 'committeetype_header':
                divs.remove(div)
        divs = iter(divs)

        while True:
            try:
                name, _, content = itertools.islice(divs, 3)
            except ValueError, StopIteration:
                break

            committee_name = name.text_content()[4:]
            committee = Committee('lower', committee_name)
            for td in content.xpath('table/descendant::td'):
                if td.xpath('a[contains(@href, "number")]'):
                    name = td.xpath('a')[0].text_content()
                    role = (td.xpath('a')[0].tail or '').strip('() ')
                    committee.add_member(name, role or 'member')

            xpath = 'table/descendant::td/a[contains(@href, "committees")]/@href'
            committee_url = content.xpath(xpath).pop()
            committee.add_source(url)
            committee.add_source(committee_url)
            self.save_committee(committee)
