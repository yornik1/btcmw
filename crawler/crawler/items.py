from scrapy_djangoitem import DjangoItem
from news.models import Article
#
# import django
# django.setup()


class ScrItem(DjangoItem):
    django_model = Article

# class Article(scrapy.Item):
#     # define the fields for your item here like:
#     name = scrapy.Field()
#     last_updated = scrapy.Field(serializer=str)
