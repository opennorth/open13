import os

SCRAPER_PATHS = [os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'scrapers')]
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DATABASE = 'open13'

# PARTY_DETAILS

LEVEL_FIELD = 'jurisdiction'
BOUNDARY_SERVICE_URL='http://represent.opennorth.ca/'
BOUNDARY_SERVICE_SETS='british-columbia-electoral-districts'
