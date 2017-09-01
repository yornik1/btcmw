import scrapy
from bs4 import BeautifulSoup
from news.models import Article
import requests # Todo with scrapy request


class CryptocoinsSpider(scrapy.Spider):
    name = "cryptocoins"


    def start_requests(self):
        urls = [
            'https://www.cryptocoinsnews.com/news/',
            'https://www.cryptocoinsnews.com/news/page/2/',
            # 'https://www.cryptocoinsnews.com/news/page/3/',
            # 'https://www.cryptocoinsnews.com/news/page/4/',
            # 'https://www.cryptocoinsnews.com/news/page/5/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        news = list(zip(scrapy.Selector(text=response.body).xpath(
                            '//*/div/h3/a/text()').extract(),
                        scrapy.Selector(text=response.body).xpath(
                            '//*/div/h3/a/@href').extract(),
                        scrapy.Selector(text=response.body).xpath(
                            '//*/a[@class="grid-thumb-image"]/img/@src').extract(),))
        for link in news:
            if not Article.objects.filter(url=link[1]):   # response.urljoin
                try:
                    resp = requests.get(link[1])
                    text = ''.join(scrapy.Selector(text=resp.content).xpath(
                        '//*/div[@class="entry-content"]/p').extract())
                    picture = link[2]  # todo try get from style
                    Article(url=link[1], title=link[0], body=text, picture_url=picture, public=True).save()
                except Exception as e:
                    print(e)
                    continue
