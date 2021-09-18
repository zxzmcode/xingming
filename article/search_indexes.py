# 导入索引
from haystack import indexes
# 导入模型
from article.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    total_views = indexes.IntegerField(model_attr='total_views')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
