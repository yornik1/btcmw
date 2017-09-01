import scrapy
from bs4 import BeautifulSoup
from news.models import Article
import requests # Todo with scrapy request


class NewsBTCSpider(scrapy.Spider):
    name = "newsbtc"


    def start_requests(self):
        urls = [
            'http://www.newsbtc.com/category/news/',
            'http://www.newsbtc.com/category/news/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        news = list(zip(scrapy.Selector(text=response.body).xpath('//*/div/div/header/h2/a[1]/text()').extract(),
                scrapy.Selector(text=response.body).xpath('//*/div/div/header/h2/a[1]/@href').extract()))
        for link in news:
            if not Article.objects.filter(url=link[1]):   # response.urljoin
                try:
                    resp = requests.get(link[1])
                    text = ''.join(scrapy.Selector(text=resp.content).xpath(
                        '//*/div[@class="entry-content"]/p').extract())
                    picture = scrapy.Selector(text=resp.content).xpath('//*/header/div/img/@src').extract_first()  # todo fix xpath
                    Article(url=link[1], title=link[0], body=text, picture_url=picture, public=True).save()
                except Exception as e:
                    print(e)
                    continue
