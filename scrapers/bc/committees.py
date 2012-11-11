# -*- coding: utf-8 -*-
import lxml.html
from billy.scrape.committees import CommitteeScraper, Committee
from scrapelib import HTTPError


class BCCommitteeScraper(CommitteeScraper):

    jurisdiction = 'bc'

    def scrape(self, term, chambers):
        url = 'http://www.leg.bc.ca/cmt/index.htm'
        doc = lxml.html.fromstring(self.urlopen(url))
        doc.make_links_absolute(url)

        for anchor in doc.xpath('//h5/../descendant::a'):
            name = anchor.text_content()
            name = ' '.join(name.split())
            if not name or 'Facebook' in name:
                continue
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

        for url in doc.xpath('//a[contains(., "Current Membership")]/@href'):
            doc = lxml.html.fromstring(self.urlopen(url))
            doc.make_links_absolute(url)

        xpath = '//h4[text()="Membership"]/../descendant::ul/li/a'
        for anchor in doc.xpath(xpath):
            name = anchor.text_content()
            type_ = None
            if anchor.tail:
                type_ = anchor.tail.strip(u'\xa0 ()')
            if not type_:
                type_ = 'member'
            comm.add_member(name, type_)

