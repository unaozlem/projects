import scrapy
from scrapy.crawler import CrawlerProcess


url_first = "https://www.lyrics.com/artist/The-Rolling-Stones/5298"


# Create the Spider class
class Lyrics_Spider(scrapy.Spider):
    name = "lyrics_spider"

    # start_requests method
    def start_requests(self):
        yield scrapy.Request(url=url_first, callback=self.parse_front)

    # First parsing method
    def parse_front(self, response):
        lyric_links = response.xpath("//td/a/@href")
        links_to_follow = lyric_links.extract()
        print(lyric_links)
        for url in links_to_follow:
            yield response.follow(url=url, callback=self.parse_pages)

    # Second parsing method
    def parse_pages(self, response):
        # Create a SelectorList of the lyric titles text
        lyrics_body = response.xpath('./pre[@class="lyric-body"]/text()')
        # Extract the text and strip it clean
        lyrics = lyrics_body.extract_first().strip()
        # Fill in the dictionary
        dc_dict[lyrics] = lyrics


dc_dict = dict()

# Run the Spider
process = CrawlerProcess()
process.crawl(Lyrics_Spider)
process.start()
