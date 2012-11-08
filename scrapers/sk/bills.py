import datetime
from itertools import takewhile
from collections import namedtuple

import lxml.html

from billy.scrape.bills import BillScraper, Bill
from billy.scrape.utils import pdf_to_lxml
from .actions import Categorizer


DummyBR = namedtuple('DummyBR', 'tag text tail')


class MBBillScraper(BillScraper):
    jurisdiction = 'sk'
    categorizer = Categorizer()

    def scrape(self, session, chambers):
        print session
        url = 'http://www.legassembly.sk.ca/legislative-business/bills/'
        doc = lxml.html.fromstring(self.urlopen(url))
        doc.make_links_absolute(url)

        url = doc.xpath('//a[text() = "Progress of Bills"]/@href').pop()
        filename, resp = self.urlretrieve(url)

        doc = pdf_to_lxml(filename)

        actions = [
            'First Reading',
            'Crown recommendation',
            'Committee',
            'Second Reading',
            'Committee',
            'Amend Date',
            'Third Reading',
            'Royal Assent',
            'In Effect'
            ]

        for a in doc.xpath('//a[contains(@href, "legdocs/Bills")]'):
            bill_id = a.text_content().strip()
            predicate = lambda el: el.tag == 'br'
            sibs = list(takewhile(predicate, a.itersiblings()))

            # If the star is missing, insert it to avoid complicated code.
            if not sibs[0].tail.strip() == '*':
                sibs.insert(0, DummyBR('br', None, '*'))

            title_chunks = [sibs[1].tail.strip()]
            sponsor = sibs[2].tail.strip()
            dates = sibs[3].tail.split(u'\xa0')
            title_chunks.extend((br.tail or '').strip() for br in sibs[4:])
            title = ' '.join(title_chunks).strip()

            bill = Bill(session, 'lower', bill_id, title, type='bill')
            bill.add_sponsor(name=sponsor, type='primary')

            for action, date in zip(actions, dates):
                date = datetime.datetime.strptime(date.strip(), '%Y-%m-%d')
                attrs = dict(action=action, date=date, actor='lower')
                attrs.update(self.categorizer.categorize(action))
                bill.add_action(**attrs)

            bill.add_source(url)
            bill.add_version('Introduced', a.attrib['href'],
                mimetype='application/pdf')
            self.save_bill(bill)
