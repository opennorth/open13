from billy.scrape.speeches import SpeechScraper, Speech

import datetime as dt
import lxml.html


HANSARD_URL = 'http://www.leg.bc.ca/hansard/8-8.htm'


class BCSpeechScraper(SpeechScraper):
    jurisdiction = 'bc'

    def lxmlize(self, url):
        with self.urlopen(url) as page:
            page = lxml.html.fromstring(page)
        page.make_links_absolute(url)
        return page

    def scrape_hansard(self, session, url):
        subject = None
        procedure = None
        speech = None

        def save_speech():
            if speech:
                self.save_speech(speech)
                speech = None

        page = self.lxmlize(url)
        for para in page.xpath(".//p"):
            try:
                klass = para.attrib['class'].strip()
            except KeyError:
                continue  # Some para entries have no class.

            print klass

    def scrape(self, session, chambers):
        # XXX: Chamber is meaningless here.
        page = self.lxmlize(HANSARD_URL)
        for row in page.xpath("//table/tr"):
            hansard_html = row.xpath(".//a[contains(text(), 'HTML')]")
            if hansard_html == []:
                continue
            for a in hansard_html:
                self.scrape_hansard(session, a.attrib['href'])
