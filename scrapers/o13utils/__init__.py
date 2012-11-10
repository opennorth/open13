import json
import urllib2

from billy.scrape.legislators import LegislatorScraper, Legislator

class RepresentLegislatorScraper(LegislatorScraper):
    """A legislator scraper that pulls data from represent.opennorth.ca.
    Subclasses need to set the following two class attributes:

    jurisdiction = 'on'
    representative_set = 'ontario-legislature'
    """

    latest_only = True

    def scrape(self, term, chambers):

        represent_url = 'http://represent.opennorth.ca/representatives/%s/?limit=500' % self.representative_set
        data = json.load(urllib2.urlopen(represent_url))
        for rep in data['objects']:
            leg = Legislator(term, 'lower',
                rep['district_name'],
                rep['name'],
                party=rep.get('party_name'),
                photo_url=rep.get('photo_url'),
                url=rep.get('url'),
                email=rep.get('email')
            )
            leg.add_source(rep['source_url'])
            for rep_office in rep.get('offices', []):
                name = rep_office.get('postal', '').split('\n')[0]
                if not name:
                    name = (rep_office.get('type').title() + ' office').split()
                leg.add_office(
                    'capitol' if rep_office.get('type') == 'legislature' else 'district',
                    name,
                    phone=rep_office.get('tel'),
                    fax=rep_office.get('fax'),
                    address=rep_office.get('postal')
                )
            self.save_legislator(leg)
