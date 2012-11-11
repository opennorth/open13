# -*- coding: utf-8 -*-
import lxml.html
from billy.scrape.committees import CommitteeScraper, Committee
from billy.scrape.utils import pdf_to_lxml


class MBCommitteeScraper(CommitteeScraper):

    jurisdiction = 'mb'

    def scrape(self, term, chambers):
        url = ('http://www.gov.mb.ca/legislature/committees/membership.pdf')
        filename, resp = self.urlretrieve(url)
        doc = pdf_to_lxml(filename, type='xml')

        import pdb;pdb.set_trace()
