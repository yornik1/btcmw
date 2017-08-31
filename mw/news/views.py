from news.models import Article
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

# Create your views here.



class Articles(ListView):
    model = Article
    paginate_by = 35
    # template_name = "main/singleoffer_list.html"

    def get_queryset(self, *args, **kwargs):
        return super(Articles, self).get_queryset(*args, **kwargs).filter(public=True)


class ArticleDetail(DetailView):
    model = Article
