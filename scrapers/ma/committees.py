# -*- coding: utf-8 -*-
import lxml.html
from billy.scrape.committees import CommitteeScraper, Committee
from scrapelib import HTTPError


class MBCommitteeScraper(CommitteeScraper):

    jurisdiction = 'mb'

    def scrape(self, term, chambers):
        pass