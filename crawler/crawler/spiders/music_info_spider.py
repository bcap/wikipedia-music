from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

class MusicInfoSpider(BaseSpider):
    name = "music-info"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = [
        "http://en.wikipedia.org/wiki/Hard_rock",
        "http://en.wikipedia.org/wiki/Drum_and_bass"
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        
        analisedStyle = hxs.select('//*[@id="firstHeading"]/span/text()').extract()[0]

        print "%s Origins:" % (analisedStyle)
        origins = hxs.select('//*[@id="mw-content-text"]/table[@class="infobox hlist"]/tr[th/text() = "Stylistic origins"]/td/a')   
        for origin in origins:
            style = origin.select('@title').extract()[0]
            link = origin.select('@href').extract()[0]
            print "\t%s (%s)" % (style, link)

        print "%s Subgenres:" % (analisedStyle)
        subgenres = hxs.select('//*[@id="mw-content-text"]/table[@class="infobox hlist"]/tr[preceding-sibling::*[1]/th/text() = "Subgenres"]/td/a')
        for subgenre in subgenres:
            style = subgenre.select('@title').extract()[0]
            link = subgenre.select('@href').extract()[0]
            print "\t%s (%s)" % (style, link)

        print "%s Derivatives:" % (analisedStyle)
        derivatives = hxs.select('//*[@id="mw-content-text"]/table[@class="infobox hlist"]/tr[th/text() = "Derivative forms"]/td/a') 
        for derivative in derivatives:
            style = derivative.select('@title').extract()[0]
            link = derivative.select('@href').extract()[0]
            print "\t%s (%s)" % (style, link)
