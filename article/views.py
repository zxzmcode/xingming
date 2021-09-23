import markdown

from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from django.core.cache import cache
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect

import time

from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet
from markdown.extensions.toc import TocExtension
from article.models import Article, Category, Tag

from xingming import settings


# <editor-fold desc="index">
def index_view(request):
    return redirect("article:article_list")


# </editor-fold>


# <editor-fold desc="搜索">

class ArticleSearchView(SearchView):
    # 返回搜索结果集
    context_object_name = 'search_list'
    # 设置分页
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)
    # 搜索结果以浏览量排序
    queryset = SearchQuerySet().order_by('-total_views')


# </editor-fold>

# <editor-fold desc="关于">
def about_author(request):
    return render(request, 'about.html')


# </editor-fold>

# <editor-fold desc="归档时间轴">
class ArchiveView(ListView):
    template_name = 'article/archive.html'
    model = Article
    paginate_by = 5

    def get_context_data(self, *kwargs):
        content = super(ArchiveView, self).get_context_data()
        content['articles'] = Article.objects.all().order_by('-created')
        return content


# </editor-fold>

# <editor-fold desc="标签主页面">
class TagListView(ListView):
    model = Article
    template_name = 'article/tag.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_ordering(self):
        ordering = super(TagListView, self).get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return '-total_views', '-id'
        return ordering


# </editor-fold>

# <editor-fold desc="标签详情页面">
class TagDetailView(ListView):
    """
    标签列表详情
    """
    model = Article
    template_name = 'article/tag.html'
    context_object_name = 'articles'
    paginate_by = 5
    pk_url_kwarg = 'id'

    def get_ordering(self):
        ordering = super(TagDetailView, self).get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return '-total_views', '-id'
        return ordering

    def get_queryset(self, **kwargs):
        queryset = super(TagDetailView, self).get_queryset()
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        return queryset.filter(tags=tag)

    def get_context_data(self, **kwargs):
        content = super(TagDetailView, self).get_context_data()
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        content['tag'] = tag
        content['tags'] = Tag.objects.annotate(num_count=Count('article'))
        return content


# </editor-fold>

# <editor-fold desc="分类主页面">
class CategoryListView(ListView):
    model = Article
    template_name = 'article/category.html'
    context_object_name = 'articles'
    paginate_by = 6

    def get_ordering(self):
        ordering = super(CategoryListView, self).get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return '-total_views', '-id'
        return ordering


# </editor-fold>

# <editor-fold desc="分类详情页面">
class CategoryDetailView(ListView):
    model = Article
    template_name = 'article/category.html'
    context_object_name = 'articles'
    paginate_by = 6
    pk_url_kwarg = 'id'

    def get_ordering(self):
        ordering = super(CategoryDetailView, self).get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return '-total_views', '-id'
        return ordering

    def get_queryset(self, **kwargs):
        queryset = super(CategoryDetailView, self).get_queryset()
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return queryset.filter(category=cate)

    def get_context_data(self, **kwargs):
        content = super(CategoryDetailView, self).get_context_data()
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        content['category'] = cate
        return content


# </editor-fold>

# <editor-fold desc="文章列表类">
class ArticleListView(ListView):
    """
        文章列表类
    """
    model = Article
    template_name = 'article/list.html'
    context_object_name = "articles"
    paginate_by = 5

    # 筛选数据传入list.html中
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 取出置顶轮播图
        context['tops'] = Article.objects.filter(is_top=1)
        return context

    # 最新最热排序
    def get_ordering(self):
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return '-total_views', '-id'
        return '-created', '-id'

    # 获取文章对应的分类
    def get_category(self):
        obj = super(ArticleListView, self).get_queryset()
        category = Category.objects.filter(category=obj.category)
        obj.category = category
        return obj


# </editor-fold>

# <editor-fold desc="文章详情类">
class ArticleDetailView(DetailView):
    """
        文章详情类
    """
    model = Article
    template_name = 'article/detail.html'

    context_object_name = 'article'
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        """
            获取对应文章的信息
        """
        obj = super(DetailView, self).get_object()
        # 设置浏览量增加时间判断,同一篇文章两次浏览超过半小时才重新统计阅览量,作者浏览忽略
        u = self.request.user
        ses = self.request.session
        the_key = 'is_read_{}'.format(obj.id)
        is_read_time = ses.get(the_key)
        if u != obj.author:
            if not is_read_time:
                obj.update_views()
                ses[the_key] = time.time()
            else:
                now_time = time.time()
                t = now_time - is_read_time
                if t > 60 * 30:
                    obj.update_views()
                    ses[the_key] = time.time()
        # 获取文章更新的时间，判断是否从缓存中取文章的markdown,可以避免每次都转换
        ud = obj.updated.strftime("%Y%m%d%H%M%S")
        md_key = '{}_md_{}'.format(obj.id, ud)
        cache_md = cache.get(md_key)
        if cache_md:
            obj.body, obj.toc = cache_md
        else:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.tables',
                TocExtension(slugify=slugify),
            ])
            obj.body = md.convert(obj.body)
            obj.toc = md.toc
            cache.set(md_key, (obj.body, obj.toc), 60 * 60 * 12)
        # 获取评论
        # comments = Comment.objects.filter(article=obj.id)
        # obj.comment = comments
        return obj

# </editor-fold>
