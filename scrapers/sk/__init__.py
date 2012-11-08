# encoding: utf-8

metadata = dict(
    name='Saskatchewan',
    capitol_timezone='America/Chicago',
    abbreviation='sk',
    legislature_name=u'Legislative Assembly of Saskatchewan',
    # this should all go away once metadata v2 lands
    lower_chamber_name='',
    upper_chamber_name='',
    lower_chamber_title='MLA',
    upper_chamber_title='',
    upper_chamber_term='',
    lower_chamber_term='',
    terms=[
        dict(name='27', sessions=['27:1'], start_year=2009, end_year=2011),
    ],
    session_details={
        '27:1': {'type': 'primary',
                 'display_name': '1st Session, 27th Legislature',
                 '_scraped_name': '1st Session, 27th Legislature',
                },
    },
    feature_flags=[],
    _ignored_scraped_sessions=[
        '4th Session, 26th Legislature',
        '3rd Session, 26th Legislature',
        '2nd Session, 26th Legislature',
        '1st Session, 26th Legislature',
        '3rd Session, 25th Legislature',
        '2nd Session, 25th Legislature',
        '1st Session, 25th Legislature',
        '4th Session, 24th Legislature',
        '3rd Session, 24th Legislature',
        '2nd Session, 24th Legislature',
        '1st Session, 24th Legislature',
        '4th Session, 23rd Legislature',
        '3rd Session, 23rd Legislature']
)


def session_list():
    from billy.scrape.utils import url_xpath
    xpath = ('//div[@class="navigation insert"]/'
             'descendant::div[@class="xrm-attribute-value"]/p/text()')
    ret = url_xpath(
        'http://www.legassembly.sk.ca/legislative-business/bills/',
        xpath)
    return [s.replace(u'\xa0', ' ') for s in ret]


