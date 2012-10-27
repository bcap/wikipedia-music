from sets import Set
from urlparse import urljoin
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from crawler.items import MusicInfoItem

class MusicInfoSpider(BaseSpider):
    wikipediaDomain = "en.wikipedia.org"
    visitedURLs = Set()
    
    name = "music-info"
    allowed_domains = [wikipediaDomain]
    start_urls = [
        "http://en.wikipedia.org/wiki/Hard_rock",
#        "http://en.wikipedia.org/wiki/Drum_and_bass"
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        item = MusicInfoItem()
        item['url'] = response.url
        item['name'] = hxs.select('//*[@id="firstHeading"]/span/text()').extract()[0]
        item['origins'] = self.parseGenres(response, hxs.select('//*[@id="mw-content-text"]/table[@class="infobox hlist"]/tr[th/text() = "Stylistic origins"]/td/a'))
        item['derivatives'] = self.parseGenres(response, hxs.select('//*[@id="mw-content-text"]/table[@class="infobox hlist"]/tr[th/text() = "Derivative forms"]/td/a')) 
        item['subgenres'] = self.parseGenres(response, hxs.select('//*[@id="mw-content-text"]/table[@class="infobox hlist"]/tr[preceding-sibling::*[1]/th/text() = "Subgenres"]/td/a'))
        
        self.visitedURLs.add(response.url)

        gatheredURLs = Set([i['url'] for i in Set(item['origins']) | Set(item['subgenres']) | Set(item['derivatives'])])
        nonVisitedURLs = (self.visitedURLs - gatheredURLs) | (gatheredURLs - self.visitedURLs)

        for url in nonVisitedURLs:
            yield Request(url, callback = self.parse)

        yield item

    def parseGenres(self, response, selector):
        result = []
        for selected in selector:
            item = MusicInfoItem()
            item['name'] = selected.select('@title').extract()[0]
            item['url'] = urljoin(response.url, selected.select('@href').extract()[0])
            result.append(item)
        return result
