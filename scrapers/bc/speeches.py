from billy.scrape.speeches import SpeechScraper, Speech

import datetime as dt
import lxml.html
import re


HANSARD_URL = 'http://www.leg.bc.ca/hansard/8-8.htm'


class BCSpeechScraper(SpeechScraper):
    jurisdiction = 'bc'

    def lxmlize(self, url):
        with self.urlopen(url) as page:
            page = lxml.html.fromstring(page)
        page.make_links_absolute(url)
        return page

    def scrape_hansard(self, session, url, hansard_id):
        subject = None
        procedure = None
        speech = None
        day = None
        sequence = 1

        page = self.lxmlize(url)
        for para in page.xpath(".//p"):
            try:
                klass = para.attrib['class'].strip()
            except KeyError:
                continue  # Some para entries have no class.

            if klass == 'SubjectHeading':
                subject = re.sub("\s+", " ", para.text_content()).strip()

            if klass == 'ProceduralHeading':
                procedure = re.sub("\s+", " ", para.text_content()).strip()

            if klass == 'SpeakerBegins':
                attribution = para.xpath(".//span[@class='Attribution']")
                if attribution == []:
                    print "Error: Speaker began without attribution"
                    print "  URL: %s" % (url)
                    print "  Txt: %s" % (para.text_content()[:30])
                    continue
                if day is None:
                    print "Error: Day is None. Bad juju."
                    continue

                if speech:
                    self.save_speech(speech)

                person = attribution[0].text_content().strip()
                if person.endswith(":"):
                    person = person.rstrip(":")
                if person == "":
                    print "Error: empty person string. Bad juju."
                    continue

                text = para.text_content()
                speech = Speech(session,
                                hansard_id,
                                day,
                                sequence,
                                person,
                                text,
                                subject=subject,
                                procedure=procedure)
                speech.add_source(url)
                sequence += 1
                continue

            if klass == 'SpeakerContinues':
                if speech is None:
                    print "Continue before a begin. bad juju."
                    continue

                text = para.text_content()
                speech['text'] += "\n%s" % (text)
                continue

            if klass == 'DateOfTranscript':
                date_text = para.text_content().strip().encode(
                    "ascii",
                    "ignore"
                )
                day = dt.datetime.strptime(date_text, "%A, %B %d, %Y")
                continue

            # print "Unknown class ID: %s" % (klass)

        if speech:
            self.save_speech(speech)

    def scrape(self, session, chambers):
        # XXX: Chamber is meaningless here.
        page = self.lxmlize(HANSARD_URL)
        for row in page.xpath("//table/tr"):
            hansard_id = row.xpath(".//td[@align='left']")
            if len(hansard_id) < 2:
                continue

            brs = hansard_id[1].xpath(".//br")
            if len(brs) != 1:
                continue

            hansard_id = brs[0].tail.strip()
            hansard_html = row.xpath(".//a[contains(text(), 'HTML')]")

            if hansard_html == []:
                continue
            for a in hansard_html:
                self.scrape_hansard(session, a.attrib['href'], hansard_id)
