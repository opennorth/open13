from billy.scrape.transcripts import TranscriptScraper, Transcript
import lxml.html


HANSARD_URL = 'http://www.leg.bc.ca/hansard/8-8.htm'


class BCTranscriptScraper(TranscriptScraper):
    jurisdiction = 'bc'

    def lxmlize(self, url):
        with self.urlopen(url) as page:
            page = lxml.html.fromstring(page)
        page.make_links_absolute(url)
        return page

    def scrape_hansard(self, session, url):
        page = self.lxmlize(url)
        procedure = None
        subject = None
        speaker = None
        text = None
        text_pending = False
        cur_transcript = None

        for para in page.xpath(".//p"):
            try:
                klass = para.attrib['class'].strip()
            except KeyError:
                continue

            if klass == 'ProceduralHeading':
                procedure = para.text_content()
                continue

            if klass == 'SubjectHeading':
                subject = para.text_content()
                cur_transcript = Transcript(session, None, procedure, subject)
                # XXX: This is very bad. Need real data an procedure type
                continue

            if klass == 'SpeakerBegins':
                if text_pending:
                    if cur_transcript is None:
                        print "Missing transcript starting point."
                        continue
                    #cur_transcript.add_transcript(speaker, text)
                    print speaker, 'spoke'
                    text_pending = False
                    text = None
                    speaker = None

                text_pending = True
                try:
                    sobj = para.xpath(".//span[@class='Attribution']")[0]
                    speaker = sobj.text_content()
                except IndexError:
                    # Some pages incorrectly place SpeakerBegins tags
                    # in the HTML. We'll just skip them.
                    text_pending = False
                    continue

                text = para.text_content()
                # print para
                pass

            if klass == 'SpeakerContinues':
                if not text_pending:
                    print "Ugh, something's out of order."
                    continue
                text += '\n' + para.text_content()
                pass

            # print klass

    def scrape(self, session, chambers):
        # XXX: Chamber is meaningless here.
        page = self.lxmlize(HANSARD_URL)
        for row in page.xpath("//table/tr"):
            hansard_html = row.xpath(".//a[contains(text(), 'HTML')]")
            if hansard_html == []:
                continue
            for a in hansard_html:
                self.scrape_hansard(session, a.attrib['href'])
