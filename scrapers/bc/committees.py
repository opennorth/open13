# -*- coding: utf-8 -*-
import itertools
import lxml.html
from billy.scrape.committees import CommitteeScraper, Committee


class CACommitteeScraper(CommitteeScraper):

    jurisdiction = 'bc'

    def scrape(self, term, chambers):
        pass