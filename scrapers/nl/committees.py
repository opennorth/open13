# -*- coding: utf-8 -*-
import lxml.html
from billy.scrape.committees import CommitteeScraper, Committee
from scrapelib import HTTPError
import re


class NLCommitteeScraper(CommitteeScraper):

    jurisdiction = 'nl'

    def scrape(self, term, chambers):
        url = 'http://www.assembly.nl.ca/business/committees/default.htm'
        doc = lxml.html.fromstring(self.urlopen(url))
        doc.make_links_absolute(url)

        for anchor in doc.xpath('(//blockquote)[1]/a'):
            name = anchor.text_content()
            comm = Committee('lower', name)
            url = anchor.attrib['href']
            comm.add_source(url)
            self.scrape_committee(comm, url)
            self.save_committee(comm)

    def scrape_committee(self, comm, url):

        try:
            doc = lxml.html.fromstring(self.urlopen(url))
        except HTTPError:
            return
        else:
            doc.make_links_absolute(url)

        for anchor in doc.xpath('(//blockquote)[1]/a'):
            name = anchor.text_content()
            type_ = None
            if anchor.tail:
                res = re.search('\((\S+)\)\s*$', anchor.tail)
                if res:
                    tmp_str = res.group()
                    type_ = tmp_str.strip('()')

            if not type_:
                type_ = 'member'
            comm.add_member(name, type_)

