from billy.scrape.transcripts import TranscriptScraper, Transcript
import lxml.html

class BCTranscriptScraper(TranscriptScraper):
    jurisdiction = 'bc'

    def scrape(self, session, chambers):
        pass
