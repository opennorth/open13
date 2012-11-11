import re
import locale
from datetime import datetime
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
        # scrape all the actions for this session
        actions = self.scrape_actions(urlified_session_id)

        for row in doc.xpath('//table[@id="tblListeProjetLoi"]/tbody/tr'):
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
            # add actions
            for action in actions[bill_id]:
                bill.add_action('lower', action['name'], action['date'])
            # get sponsors
            self.scrape_details(bill, detail_url)
            self.save_bill(bill)

    def scrape_actions(self, session_id):
        """
        Scrapes all the actions for all the bills in a given session, and
        returns them as a dictionary keyed by bill ID.
        """
        actions_list_url = 'http://www.assnat.qc.ca/fr/travaux-parlementaires/projets-loi/rapport/projets-loi-%s.html' % session_id
        actions_doc = lxml.html.fromstring(self.urlopen(actions_list_url))
        # compile regular expressions for bill action dates
        long_date_pattern = re.compile('\d\d? \w+ \d\d\d\d')
        short_date_pattern = re.compile('\d\d\d\d-\d\d-\d\d')
        # Make a dictionary of actions for each bill number
        actions = dict()
        for td in actions_doc.xpath('//table[@id="tblListeProjetLoi"]/tbody/tr/td'):
            bill_number = td.xpath('div/div/div')[0].text_content()
            bill_number = clean_spaces(bill_number.strip(u'N\xb0'))
            actions[bill_number] = []
            for action_row in td.xpath('div/div/table//tr'):
                action_name_td, action_date_td = action_row.xpath('td')
                action_name = action_name_td.text_content().strip(': ')
                action_date = clean_spaces(action_date_td.text_content())
                # Parse date using regexp
                # Need to set locale to french since the dates are in French
                locale.setlocale(locale.LC_ALL, 'fr_CA.utf8')
                try:
                    action_date = long_date_pattern.search(action_date).group(0)
                    action_date = datetime.strptime(action_date, '%d %B %Y')
                except AttributeError:
                    try:
                        action_date = short_date_pattern.search(action_date).group(0)
                        action_date = datetime.strptime(action_date, '%Y-%m-%d')
                    except:
                        # Can't parse the date, so giving up
                        continue
                actions[bill_number].append({
                    'name': action_name,
                    'date': action_date,
                })
        return actions
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
        if 'Auteur' in headings:
            sponsor = headings['Auteur'].xpath('following-sibling::*//a')[0].text_content().strip()
            bill.add_sponsor('primary', sponsor)
