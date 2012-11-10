from billy.scrape.speeches import SpeechScraper, Speech

import datetime
import lxml.html
import re

from .utils import clean_spaces


class ONSpeechScraper(SpeechScraper):
    jurisdiction = 'on'

    def lxmlize(self, url):
        with self.urlopen(url) as page:
            page = lxml.html.fromstring(page)
        page.make_links_absolute(url)
        return page


    def scrape(self, session, chambers):

        months = [(2012, 10)]
        for year, month in months:
            url = 'http://www.ontla.on.ca/web/house-proceedings/house_current.do?locale=en&Month=%s&Year=%s' % (month, year)
            doc = self.lxmlize(url)

            for day_url in doc.xpath('//span[@class="date"]/parent::a/@href'):
                self.scrape_day(session, 'lower', day_url)


    def scrape_day(self, session, chamber, day_url):
        doc = self.lxmlize(day_url)

        date = re.findall('Date=(\d{4}-\d{1,2}-\d{1,2})', day_url)[0]
        when = datetime.datetime.strptime(date, '%Y-%m-%d')
        sequence = 0
        last_h2 = ''
        section = ''
        speech = None

        transcript = doc.xpath('//div[@id="transcript"]')[0]
        # skip first item, navgation div
        for item in transcript.getchildren()[1:]:
            if item.tag == 'h2':
                # new major section
                last_h2 = clean_spaces(item.text_content())
                section = last_h2
            elif item.tag == 'h3':
                # new subsection
                section = last_h2 + ': ' + clean_spaces(item.text_content())
            elif item.tag == 'p' and item.get('class') == 'speakerStart':
                # new speaker
                # 99% of the time there are two children, <a>, <strong>
                # sometimes there are more (looks like format errors),
                # so we warn for now
                children = item.getchildren()
                a = children[0]
                strong = children[1]
                if len(children) > 2:
                    self.warning('found extra tags in speakerStart: %s',
                                 ', '.join(x.tag for x in children))
                anchor = day_url + '#' + a.get('name')
                speaker = strong.text_content().rstrip(':')
                text = strong.tail
                sequence += 1
                speech = Speech(session, chamber, 'floor-' + date, when,
                                sequence, speaker, text, section=section)
                speech.add_source(anchor)
            elif item.tag == 'p' and item.get('class') == 'timeStamp':
                timestamp = item.text_content()
                when = when.replace(hour=int(timestamp[:-2]),
                                    minute=int(timestamp[-2:]))
            elif item.tag == 'p' and (item.get('class') == 'procedure' or
                    item.get('class') == None and speech == None):
                # procedural action indicated by procedural tag or by
                # an empty tag with nobody speaking in prior session
                anchor = day_url + '#' + item.xpath('a')[0].get('name')
                sequence += 1

                if item.text_content().strip() == '':
                    continue

                speech = Speech(session, chamber, 'floor-' + date, when,
                                sequence, '-fixme-', item.text_content(),
                                section=section, type='procedure')
                speech.add_source(anchor)
                self.save_speech(speech)
                speech = None
            elif item.tag == 'p' and item.get('class') == None:
                if not item.text_content():
                    continue
                if len(item.getchildren()) > 1:
                    self.warning('found extra tags in speakerStart: %s',
                                 ', '.join(x.tag for x in children))
                speech['text'] += '\n\n' + item.text_content()
                self.save_speech(speech)
            elif item.tag == 'p':
                self.error('unknown p class=%s', item.get('class'))
            else:
                self.error('unexpected tag <%s>', item.tag)
