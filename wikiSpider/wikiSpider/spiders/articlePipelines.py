from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wikiSpider.items import Article


class ArticleSPider(CrawlSpider):
    name = 'articlePipelines'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']
    rules = [
        Rule(LinkExtractor(allow=r'/wiki/[^:]*$'), callback='parse_items', follow=True)
    ]

    def parse_items(self, response):
        article = Article()
        article['url'] = response.url 
        article['title'] = response.css("h1 span::text").get()
        paragraphs = response.xpath('//div[@id="mw-content-text"]//p//text()').getall()[0:100]
        article['text'] = ' '.join(p.strip() for p in paragraphs if p.strip())
        article['lastUpdated'] = response.css('li#footer-info-lastmod::text').get()

        return article #the spider must return an Article object for the data pipeline to precess it 
    
