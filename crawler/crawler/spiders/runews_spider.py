import scrapy
from bs4 import BeautifulSoup
from news.models import Article
# from crawler.items import ScrItem
import requests # Todo with scrapy request
URL = 'https://bits.media'

# def format_text(text):
#     p1 = re.compile('<[^<]+?>')
#     p2 = re.compile('\n+')
#
#     result = '\n'.join([line.strip() for line in text.split('\n')])
#     result = re.sub(p1, '', result).strip().replace('\t', '').replace(' \n', '\n').replace(':\n', ': ')
#     # result = re.sub(p2, '\n', result)
#     return result


class RuNewsSpider(scrapy.Spider):
    name = "runews"
    #
    # def __init__(self, **kwargs):
    #     self.item = ScrItem
    #     self.initial_request_url = 'https://bits.media/news/?PAGEN_1=1&SIZEN_1=100'

    def start_requests(self):
        urls = [
            'https://bits.media/news/?SIZEN_1=100',
            'https://bits.media/news/?PAGEN_1=2&SIZEN_1=100',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        # if self.initial_request_url:
        #     yield scrapy.Request(url=self.initial_request_url)

    def parse(self, response):
        page = response.url.split('SIZEN_1')[0][-2] if response.url.split('SIZEN_1')[0][-2].isdigit() else 1
        news = [(scrapy.Selector(text=response.body).xpath(
                    '/html/body/div/div[1]/div[8]/div/div/div[2]/div/ul/li[{}]/a/text()'.format(i)).extract()[0],
                 scrapy.Selector(text=response.body).xpath(
                    '/html/body/div/div[1]/div[8]/div/div/div[2]/div/ul/li[{}]/a/@href'.format(i)).extract()[0]
                 ) for i in
                range(2, 102)]
        for link in news:
            if not Article.objects.filter(url=URL+link[1]):
                try:
                    resp = requests.get(URL+link[1])
                    text = ''.join(scrapy.Selector(text=resp.content).xpath(
                        '/html/body/div/div[1]/div[8]/div/div/div[2]/div/p'
                        ).extract()[:-2]).replace('img src="/images','img src="https://bits.media/images')
                    picture = scrapy.Selector(text=resp.content).xpath(
                        '/html/body/div/div[1]/div[8]/div/div/div[2]/div/p/img/@src').extract_first()
                    if 'bits.media' not in picture:
                        picture = 'https://bits.media' + picture
                    Article(url=URL+link[1], title=link[0], body=text, picture_url=picture, public=True).save()
                except Exception as e:
                    print(e)
                    continue
        # filename = 'bits-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)

    def parse_texts(self, response):
        l = response.meta['item_loader']
        l.selector = l.default_selector_class(response)
        l.response = response

        l.add_detail_xpaths()
        yield l.load_item()