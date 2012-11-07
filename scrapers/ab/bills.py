import re
import datetime
import lxml.html
from billy.scrape.bills import BillScraper, Bill

from .actions import Categorizer


class ABBillScraper(BillScraper):
    jurisdiction = 'ab'
    categorizer = Categorizer()

    def scrape(self, session, chambers):
        url = ('http://www.assembly.ab.ca/net/index.aspx?p=bill&section=doc')
        doc = lxml.html.fromstring(self.urlopen(url))
        doc.make_links_absolute(url)

        table1 = doc.xpath('//table[@id="Table1"]').pop()
        xpath = 'following-sibling::table/descendant::tr'
        for td1, td2 in table1.xpath(xpath)[1:]:

            bill_id = td1.text_content().replace(u'\xa0', ' ')
            bill_id.strip('*')
            title = td1.text_content()
            bill = Bill(session, 'lower', bill_id, title, type='bill')
            url = bill['url'] = td1.xpath('a/@href').pop()
            bill.add_source(url)
            self.scrape_bill(bill, url)
            self.save_bill(bill)

    def scrape_bill(self, bill, url):
        doc = lxml.html.fromstring(self.urlopen(url))
        doc.make_links_absolute(url)
        xpath = '//table[@id="Table1"]/descendant::tr'
        for (action, lines) in doc.xpath(xpath)[1:]:
            action = action.text_content().strip().strip(':')
            lines = lines.text_content().splitlines()
            lines = [x.strip() for x in lines]
            lines = filter(None, lines)
            for line in lines:
                date = re.search(r'\S+ \S+', line)
                hansard = re.search(r'\(.+?\)', line)
                text = re.search(r' \x97 (.+)', line)
                if not all([date, hansard]):
                    self.logger.critical('Stuff missing!')
                date = date.group()
                hansard = hansard.group()
                for fmt in [r'%b %d', r'%b. %d']:
                    try:
                        date = datetime.datetime.strptime(date, fmt)
                    except ValueError:
                        continue
                    else:
                        break
                date = datetime.datetime(month=date.month, day=date.day,

                                         # XXX: Horific hack alert
                                         # Assuming the current year applies.
                                         year=datetime.datetime.now().year)
                if text:
                    action += (text.group().replace(u'\x97', '-'))

                attrs = dict(action=action, date=date, actor='lower')
                bill.add_action(**attrs)


