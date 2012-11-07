import datetime
import lxml.html
from billy.scrape.bills import BillScraper, Bill

from .actions import Categorizer


class ABBillScraper(BillScraper):
    jurisdiction = 'bc'
    categorizer = Categorizer()

    def scrape(self, session, chambers):
        url = 'http://www.leg.bc.ca/legislation/bills.htm'
        doc = lxml.html.fromstring(self.urlopen(url))
        doc.make_links_absolute(url)

        # Get the progress table.
        url = doc.xpath('//a[text()="Progress of Bills"]/@href').pop()
        doc = lxml.html.fromstring(self.urlopen(url))
        doc.make_links_absolute(url)

        for tr in doc.xpath('//table[@class="votestable"]/tr')[1:]:
            bill_id = tr[0].text_content()
            title = tr[1].text_content()
            if title == 'Title':
                # This is a header row.
                continue
            sponsor = tr[2].text_content()
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
                date = datetime.datetime(month=date.month, day=date.day,

                                         # XXX: Horific hack alert
                                         # Assuming the current year applies.
                                         year=datetime.datetime.now().year)

                attrs = dict(action=action, date=date, actor='lower')
                bill.add_action(**attrs)

            bill.add_source(url)
            self.save_bill(bill)
