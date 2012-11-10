# encoding: utf-8

metadata = dict(
    name='Newfoundland and Labrador',
    capitol_timezone='America/Newfoundland',
    abbreviation='nl',
    legislature_name='Newfoundland and Labrador House of Assembly',
    # this should all go away once metadata v2 lands
    lower_chamber_name='',
    upper_chamber_name='',
    lower_chamber_title='Member of the House of Assembly',
    upper_chamber_title='',
    upper_chamber_term='',
    lower_chamber_term='',
    terms=[
        dict(name='47', sessions=['47:1'], start_year=2011, end_year=2012),
    ],
    session_details={
        '47:1': {'type': 'primary',
                 'display_name': '47th General Assembly, 1st Session',
                 '_scraped_name': u'1st Session \u2013 2011-12',
                },
    },
    feature_flags=[],
    _ignored_scraped_sessions=[ 'Swearing-in Ceremony', u'4th Session \u2013 2011', u'3rd Session \u2013 2010-11', u'2nd Session \u2013 2009-2010', u'1st Session \u2013 2008-2009', u'4th Session \u2013 2007', u'3rd Session \u2013 2006-2007', u'2nd Session \u2013 2005-2006', u'1st Session \u2013 2004-2005', 'Swearing-in Ceremony and Election of the Speaker', u'5th Session \u2013 2003', u'4th Session \u2013 2002-2003', u'3rd Session \u2013 2001-2002', u'2nd Session \u2013 2000', u'1st Session \u2013 1999', u'3rd Session \u2013 1998', u'2nd Session \u2013 1997-1998', u'1st Session \u2013 1996-1997', u'3rd Session \u2013 1995', u'2nd Session \u2013 1994-95', u'1st Session \u2013 1993-94', u'4th Session \u2013 1992-93', u'3rd Session \u2013 1991-92' ]
)


def session_list():
    from billy.scrape.utils import url_xpath
    return url_xpath('http://www.assembly.nl.ca/business/hansard/default.htm',
                     '//div[@id="content"]//a/text()')
