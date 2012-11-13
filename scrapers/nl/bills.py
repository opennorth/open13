import datetime
import lxml.html
from billy.scrape.bills import BillScraper, Bill
from billy.scrape.utils import clean_spaces

from .actions import Categorizer


class NLBillScraper(BillScraper):
    jurisdiction = 'nl'
    categorizer = Categorizer()

    def scrape(self, session, chambers):
        # Get the progress table.
        url = 'http://www.assembly.nl.ca/business/bills/ga47session1.htm'
        doc = lxml.html.fromstring(self.urlopen(url))
        doc.make_links_absolute(url)

        for tr in doc.xpath('//table[@class="bills"]/tr')[1:]:
            bill_id = clean_spaces(tr[0].text_content()).strip('*')
            if not bill_id:
                break # empty rows extend past actual list of bills

            title = clean_spaces(tr[1].text_content())
            sponsor = "NA"
            # sponsor = clean_spaces(tr[2].text_content())
            chapter = tr[-1].text_content()

            bill = Bill(session, 'lower', bill_id, title, type='bill')
            bill.add_sponsor(name=sponsor, type='primary')

            if chapter:
                bill['chapter'] = chapter

            # Actions and version urls.
            data = zip([
                'First Reading',
                'Second Reading',
                'Committee',
                'Amendments',
                'Third Reading',
                'Royal Assent',
                'Act'],
                tr[2:-1])

            for action, td in data:
                # version_url = td.xpath('a/@href')
                # if version_url:
                #     bill.add_version(url=version_url.pop(), name=action,
                #         mimetype='text/html')

                date_text = td.text_content()
                date = None
                fmt = r'%b. %d/%Y'
                try:
                    date = datetime.datetime.strptime(date_text, fmt)
                except ValueError:
                    continue
                else:
                    break
                if date is None:
                    continue

                attrs = dict(action=action, date=date, actor='lower')
                attrs.update(self.categorizer.categorize(action))
                bill.add_action(**attrs)

            bill.add_source(url)
            self.save_bill(bill)
