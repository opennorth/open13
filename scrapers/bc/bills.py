import datetime
import lxml.html
from billy.scrape.bills import BillScraper, Bill
from billy.scrape.utils import clean_spaces

from .actions import Categorizer


class BCBillScraper(BillScraper):
    jurisdiction = 'bc'
    categorizer = Categorizer()

    def scrape(self, session, chambers):
        # Get the progress table.
        url = 'http://www.leg.bc.ca/%s/votes/progress-of-bills.htm' % session
        doc = lxml.html.fromstring(self.urlopen(url))
        doc.make_links_absolute(url)
        session_start = self.metadata['session_details'][session]['start_date']
        session_end = self.metadata['session_details'][session]['end_date']

        for tr in doc.xpath('//table[@class="votestable"]/tr')[1:]:
            bill_id = clean_spaces(tr[0].text_content()).strip('*')
            if 'Ruled out of order' in bill_id:
                continue
            title = clean_spaces(tr[1].text_content())
            if title == 'Title':
                # This is a header row.
                continue
            sponsor = clean_spaces(tr[2].text_content())
            chapter = tr[-1].text_content()

            bill = Bill(session, 'lower', bill_id, title, type='bill')
            bill.add_sponsor(name=sponsor, type='primary')

            if chapter:
                bill['chapter'] = chapter

            # Actions and version urls.
            data = zip([
                'Reading',
                'Second Reading',
                'Committee',
                'Report',
                'Amended',
                'Third Reading',
                'Royal Assent',
                'S.B.C. Chap. No.'],
                tr[3:-1])

            for action, td in data:
                version_url = td.xpath('a/@href')
                if version_url:
                    bill.add_version(url=version_url.pop(), name=action,
                        mimetype='text/html')

                date_text = td.text_content()
                date = None
                for fmt in [r'%b %d', r'%b. %d']:
                    try:
                        date = datetime.datetime.strptime(date_text, fmt)
                    except ValueError:
                        continue
                    else:
                        break
                if date is None:
                    continue

                # guess the year of the action
                date = datetime.datetime(month=date.month, day=date.day,
                                         year=session_start.year)
                if date < session_start or date > session_end:
                    date = datetime.datetime(month=date.month, day=date.day,
                                             year=session_end.year)
                if date < session_start or date > session_end:
                    self.error('action %s appears to have occured on %s, '
                               'which is outside of session', action, date)
                # XXX: it should be noted that this isn't perfect
                # if a session is longer than a year there's a chance we get
                # the action date wrong (with a preference for the earliest
                # year)
                # in practice this doesn't seem to happen, and hopefully
                # if/when it does they will add years to these action dates


                attrs = dict(action=action, date=date, actor='lower')
                attrs.update(self.categorizer.categorize(action))
                bill.add_action(**attrs)

            bill.add_source(url)
            self.save_bill(bill)
