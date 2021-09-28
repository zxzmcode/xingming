from django.urls import path, include
from . import views
from .views import CategoryDetailView, CategoryListView, TagDetailView, TagListView, ArticleListView, \
    ArticleDetailView, ArchiveView, ArticleSearchView

app_name = "article"

urlpatterns = [
    # 配置list的入口
    path("list/", ArticleListView.as_view(), name="article_list"),
    # 最新与最热,最新采用的就是list
    path("list/hot/", ArticleListView.as_view(), {'sort': 'v'}, name="article_hot_list"),
    # 文章详情
    path("detail/<slug:slug>/", ArticleDetailView.as_view(), name="article_detail"),
    # 分类总览
    path('category/', CategoryListView.as_view(), name='article_category'),
    # 分类总览列表
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='article_category_list'),
    # 文章分类展示-最热
    path('category/<slug:slug>/hot/', CategoryDetailView.as_view(), {'sort': 'v'}, name='article_category_list_hot'),
    # 标签总览
    path('tag/', TagListView.as_view(), name='article_tag'),
    # 标签列表总览
    path('tag/<slug:slug>/', TagDetailView.as_view(), name='article_tag_list'),
    # 标签列表总览-最热
    path('tag/<slug:slug>/hot/', CategoryDetailView.as_view(), {'sort': 'v'}, name='article_tag_list_hot'),
    # 时间轴 归档
    path('archive/', ArchiveView.as_view(), name='article_archive'),
    # 搜索函数
    path('search/', ArticleSearchView.as_view(), name='article_search'),
]
