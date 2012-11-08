from billy.scrape.events import EventScraper, Event

import re
import lxml
import datetime as dt

HANSARD_URL = 'http://www.leg.bc.ca/hansard/8-8.htm'

class BCEventScraper(EventScraper):

    jurisdiction = 'bc'

    def lxmlize(self, url):
        with self.urlopen(url) as page:
            page = lxml.html.fromstring(page)
        page.make_links_absolute(url)
        return page

    def scrape(self, chamber, session):
        # XXX: Chamber is meaningless here.
        page = self.lxmlize(HANSARD_URL)
        for row in page.xpath("//table/tr"):
            ids = row.xpath(".//td[@align='left']/p")
            # print [x.text_content() for x in ids]

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
            print hansard_id
            if date == "":
                continue

            times_of_day = [
                "Morning",
                "Afternoon"
            ]
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
                                   type="speech",
                                   mimetype="text/html")

            for x in pdf_links:
                event.add_document(x.text_content(),
                                   x.attrib['href'],
                                   type="speech",
                                   mimetype="application/pdf")

            event.add_source(HANSARD_URL)
            self.save_event(event)
