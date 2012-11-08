import datetime
import urlparse

import lxml.html

from billy.scrape.bills import BillScraper, Bill
from .actions import Categorizer


class MBBillScraper(BillScraper):
    jurisdiction = 'mb'
    categorizer = Categorizer()

    def scrape(self, session, chambers):
        url = 'http://web2.gov.mb.ca/bills/sess/index.php'
        doc = lxml.html.fromstring(self.urlopen(url))
        doc.make_links_absolute(url)

        _, real_url = doc.xpath('//meta')[0].attrib['content'].split('=')
        url = urlparse.urljoin(url, real_url)
        doc = lxml.html.fromstring(self.urlopen(url))
        doc.make_links_absolute(url)

        for table in doc.xpath('//table')[1:]:
            # Skip the 2 header rows.
            for tr in table[2:]:
                # Skip formal bills that haven't been printed.
                if len(tr) != 5:
                    continue

                bill = self.parse_bill(session, tr)
                bill.add_source('url')

                self.save_bill(bill)

    def parse_bill(self, session, tr):
        bill_id = tr[0].text.strip()
        title = tr[2].xpath('a')[0].text
        html_url = tr[2].xpath('a')[0].attrib['href']
        pdf_url = tr[3].xpath('a')[0].attrib['href']
        sponsor = tr[1].text.strip()

        bill = Bill(session, 'lower', bill_id, title, type='bill')
        bill.add_sponsor(name=sponsor, type='primary')

        bill.add_version('Introduced', html_url, mimetype='text/html')
        bill.add_version('Introduced', pdf_url, mimetype='application/pdf')

        bill['url'] = html_url

        chaptered = tr[4].xpath('a')
        if chaptered:
            bill['chaptered'] = chaptered[0].text
            bill['chaptered_url'] = chaptered[0].attrib['href']

        return bill
