from datetime import datetime
import re
import lxml.html
from billy.scrape.bills import BillScraper, Bill

def _clean_spaces(s):
    return re.sub('\s+', ' ', s, flags=re.U).strip()

class ONBillScraper(BillScraper):
    jurisdiction = 'on'

    def scrape(self, session, chambers):
        url = 'http://www.ontla.on.ca/web/bills/bills_all.do?locale=en&parlSessionID=%s' % session
        html = self.urlopen(url)
        doc = lxml.html.fromstring(html)
        doc.make_links_absolute(url)

        for row in doc.xpath('//table/tr'):
            id, title_td, sponsor = row.xpath('td')
            bill_id = id.text_content().strip()
            title = title_td.text_content().strip()
            # pull sponsor off different page
            bill = Bill(session, 'lower', bill_id, title)
            # skip to detail page
            detail_url = title_td.xpath('a/@href')[0] + "&detailPage=bills_detail_status"
            bill.add_source(url)
            bill.add_source(detail_url)

            # get actions & sponsors
            self.scrape_details(bill, detail_url)

            self.save_bill(bill)

    def scrape_details(self, bill, detail_url):
        data = self.urlopen(detail_url)
        doc = lxml.html.fromstring(data)

        # sponsors
        for sp in doc.xpath('//span[@class="pSponsor"]/a'):
            bill.add_sponsor('primary', _clean_spaces(sp.text_content()))
        for sp in doc.xpath('//span[@class="sSponsor"]/a'):
            bill.add_sponsor('cosponsor', _clean_spaces(sp.text_content()))

        for row in doc.xpath('//table//tr')[1:]:
            date, stage, activity, committee = row.xpath('td/text()')
            date = datetime.strptime(_clean_spaces(date), "%B %d, %Y")
            stage = _clean_spaces(stage)
            activity = _clean_spaces(activity)
            committee = _clean_spaces(committee)
            # action prefixed with stage if present
            action = '%s - %s' % (stage, activity) if stage else activity
            # default to lower, use committee if present
            actor = committee if committee else 'lower'
            bill.add_action(actor, action, date)

