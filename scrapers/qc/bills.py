#import re
import pdb
import lxml.html
from billy.scrape.bills import BillScraper, Bill
from billy.scrape.utils import clean_spaces

class QCBillScraper(BillScraper):
    jurisdiction = 'qc'

    def scrape(self, session, chambers):
        urlified_session_id = session.replace(':', '-')
        url = 'http://www.assnat.qc.ca/fr/travaux-parlementaires/projets-loi/projets-loi-%s.html' % urlified_session_id
        html = self.urlopen(url)
        doc = lxml.html.fromstring(html)
        doc.make_links_absolute(url)

        for row in doc.xpath('//table[@id="tblListeProjetLoi"]/tbody/tr'):
            #pdb.set_trace()
            id_td, details_td = row.xpath('td')[:2]
            bill_id = clean_spaces(id_td.text_content())
            pdf_link = details_td.xpath('p[@class="lienAssocie"]//a')[0]
            bill_name = clean_spaces(pdf_link.text_content())
            pdf_url = pdf_link.xpath('@href')[0]
            detail_url = 'http://www.assnat.qc.ca/fr/travaux-parlementaires/projets-loi/projet-loi-%s-%s.html' % (bill_id, urlified_session_id)
            bill = Bill(session, 'lower', bill_id, bill_name)
            bill.add_source(url)
            bill.add_source(detail_url)
            bill.add_source(pdf_url)
            # get actions & sponsors
            self.scrape_details(bill, detail_url)
            self.save_bill(bill)

    def scrape_details(self, bill, detail_url):
        data = self.urlopen(detail_url)
        doc = lxml.html.fromstring(data)

        # Collect all the h3s together in a dict
        headings = dict()
        for heading in doc.xpath('//h3'):
            title = clean_spaces(heading.text_content())
            if len(title) > 0:
                headings[title] = heading

        # sponsors
        # TODO: is it possible for there to be more than one sponsor?
        sponsor = headings['Auteur'].xpath('following-sibling::*//a')[0].text_content().strip()
        bill.add_sponsor('primary', sponsor)

        # TODO: scrape actions
