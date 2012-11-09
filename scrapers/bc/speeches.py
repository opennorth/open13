from billy.scrape.speeches import SpeechScraper, Speech
from billy.scrape.events import Event

import datetime as dt
import lxml.html
import logging
import re

logger = logging.getLogger('open13')
HANSARD_URL = 'http://www.leg.bc.ca/hansard/8-8.htm'


class BCSpeechScraper(SpeechScraper):
    jurisdiction = 'bc'

    def lxmlize(self, url):
        with self.urlopen(url) as page:
            page = lxml.html.fromstring(page)
        page.make_links_absolute(url)
        return page

    def scrape_hansard(self, session, chamber, url, hansard_id):
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
                attribution = [x.text_content().strip() for x in
                               para.xpath(".//span[@class='Attribution']")]

                # XXX: Check if we have a J. Q. Public: at the begining
                # to mark as attributed. Early results show fail on picking
                # that up.

                if attribution == []:
                    logger.debug("Error: Speaker began without attribution")
                    logger.debug("  URL: %s" % (url))
                    logger.debug("  Txt: %s" % (para.text_content()[:30]))
                    continue

                if day is None:
                    logger.debug("Error: Day is None. Bad juju.")
                    logger.debug(url)
                    continue

                if speech:
                    self.save_object(speech)

                person = attribution[0]
                if person.endswith(":"):
                    person = person.rstrip(":")
                if person == "":
                    logger.debug("Error: empty person string. Bad juju.")
                    continue

                text = para.text_content()
                speech = Speech(session,
                                chamber,
                                hansard_id,
                                day,
                                sequence,
                                person,
                                text,
                                subject=subject,
                                section=procedure)
                speech.add_source(url)
                sequence += 1
                continue

            if klass == 'SpeakerContinues':
                if speech is None:
                    logger.debug("Continue before a begin. bad juju.")
                    continue

                text = para.text_content()
                speech['text'] += "\n%s" % (text)
                continue

            if klass == 'DateOfTranscript' or klass == 'TitlePageDate':
                date_text = para.text_content().strip().encode(
                    "ascii",
                    "ignore"
                )
                day = dt.datetime.strptime(date_text, "%A, %B %d, %Y")
                continue

        if speech:
            self.save_object(speech)

    def scrape(self, session, chambers):
        # XXX: Chamber is meaningless here.
        page = self.lxmlize(HANSARD_URL)
        for row in page.xpath("//table/tr"):
            hansard_id = row.xpath(".//td[@align='left']")
            ids = row.xpath(".//td[@align='left']/p")
            web_links = row.xpath(".//a[contains(text(), 'HTML')]")
            pdf_links = row.xpath(".//a[contains(text(), 'PDF')]")

            if web_links == [] and pdf_links == []:
                continue
            if ids == []:
                continue

            ids = ids[-1]
            date = ids.text.strip()
            hansard_id = ids.xpath(".//br")[0].tail
            hansard_id = re.sub("\s+", " ", hansard_id).strip()
            if date == "":
                continue

            times_of_day = ["Morning", "Afternoon"]
            time_of_day = None
            for time in times_of_day:
                if date.endswith(time):
                    date = date.rstrip(", %s" % (time))
                    time_of_day = time
            when = dt.datetime.strptime(date, "%A, %B %d, %Y")
            event = Event(
                session,
                when,
                'cow:meeting',
                "%s session on %s" % (
                  time_of_day,
                    date
                ) if time_of_day else "Session on %s" % (date),
                location='Parliament Buildings',
                record_id=hansard_id  # Official record's ID for speeches.
            )
            for x in web_links:
                event.add_document(x.text_content(),
                                   x.attrib['href'],
                                   type="transcript",
                                   mimetype="text/html")
            for x in pdf_links:
                event.add_document(x.text_content(),
                                   x.attrib['href'],
                                   type="transcript",
                                   mimetype="application/pdf")
            event.add_source(HANSARD_URL)
            self.save_object(event)

            for a in web_links:
                self.scrape_hansard(session, 'lower',
                                    a.attrib['href'], hansard_id)
