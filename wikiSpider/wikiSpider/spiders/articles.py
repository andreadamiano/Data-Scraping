from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wikiSpider.items import Article

# class ArticleSpider(CrawlSpider):
#     name = "articles"
#     allowed_domains = ["en.wikipedia.org"] #global filter 
#     start_urls = ['https://en.wikipedia.org/wiki/Python_(programming_language)']
#     rules = (
#             Rule(LinkExtractor(
#             allow=r'https://en\.wikipedia\.org/wiki/[^:]*$',  # Only article pages 
#             deny=[r'/wiki/Special:', r'/wiki/File:']  # Deny patterns
#             ), 
#             callback='parse_items',
#             follow=True),
#             )  #local filters 

#     custom_settings = {
#         'DOWNLOAD_DELAY' : 5, 
#         'DEPTH_LIMIT': 0
#     }


#     def parse_items(self, response):
#         url = response.url 
#         title = response.css("h1 span::text").get()
#         paragraphs = response.xpath('//div[@id="mw-content-text"]//p//text()').getall()[0:100]
#         text = ' '.join(p.strip() for p in paragraphs if p.strip())

#         # print(f"Url: {url}")
#         # print(f"Title: {title}")
#         # print(f"Text: {text}")

#         self.logger.info(f"URL: {url}")
#         self.logger.info(f"Title: {title}")
#         self.logger.info(f"Text: {text[:500]}...")


class ArticleSpider (CrawlSpider):
    name = 'articles'
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ['https://en.wikipedia.org/wiki/Python_(programming_language)']
    rules = [
        Rule(LinkExtractor(allow=r'/wiki/[^:]*$'), callback = 'parse_items' , follow= True, cb_kwargs= {'is_article': True}),
        # Rule(LinkExtractor(allow='^.*$'), callback = 'parse_items' , follow= True, cb_kwargs= {'is_article': False}),

    ]

    custom_settings = {
        'DOWNLOAD_DELAY' : 5, 
        'DEPTH_LIMIT': 1, 
        'ROBOTSTXT_OBEY' : False 
    }

    def parse_items (self, response, is_article):
        article = Article()
        if is_article:
            article['url'] = response.url 
            article['title'] = response.css("h1 span::text").get()
            paragraphs = response.xpath('//div[@id="mw-content-text"]//p//text()').getall()[0:100]
            article['text'] = ' '.join(p.strip() for p in paragraphs if p.strip())
            article['lastUpdated'] = response.css('li#footer-info-lastmod::text').get()


            return article

        else:
            url = response.url 
            self.logger.info(f"URL: {url}")
            self.logger.info("This is not an article")

