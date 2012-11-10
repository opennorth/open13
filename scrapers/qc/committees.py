# -*- coding: utf-8 -*-
import pdb
import itertools
import lxml.html
from billy.scrape.committees import CommitteeScraper, Committee


class QCCommitteeScraper(CommitteeScraper):

    jurisdiction = 'qc'

    def scrape(self, chamber, term):
        url = 'http://www.assnat.qc.ca/fr/travaux-parlementaires/commissions/index.html'
        html = self.urlopen(url)
        doc = lxml.html.fromstring(html)
        doc.make_links_absolute(url)

        committees = doc.xpath('//div[@class="conteneurListeCommissions"]//li')
        for li in committees:
            committee_name = li.text_content().strip()
            committee_url = li.xpath('a/@href')[0]
            committee = Committee('lower', committee_name)
            # Get committee members
            html = self.urlopen(committee_url)
            committee_doc = lxml.html.fromstring(html)
            committee_doc.make_links_absolute(committee_url)
            members = committee_doc.xpath('//div[@class="blocMembreCommission"]')
            for div in members:
                member_name = div.xpath('p')[0].text_content().strip()
                member_role = div.xpath('p')[2].text_content().strip()
                committee.add_member(member_name, member_role or 'member')
            # Add sources
            committee.add_source(url)
            committee.add_source(committee_url)
            self.save_committee(committee)
