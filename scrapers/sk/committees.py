# -*- coding: utf-8 -*-
import lxml.html
from billy.scrape.committees import CommitteeScraper, Committee
from scrapelib import HTTPError


class SKCommitteeScraper(CommitteeScraper):

    jurisdiction = 'sk'

    def scrape(self, term, chambers):
        pass
