import markdown
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class FriendsLink(models.Model):
    """
    Class: 友情链接的数据模型
    """
    name = models.CharField('博客网站名', max_length=50)
    friend_url = models.CharField('博客URL', max_length=100)
    created = models.DateTimeField('博客创建时间', default=timezone.now)

    class Meta:
        verbose_name = '文章内容'
        verbose_name_plural = verbose_name
        ordering = ['created']


class Tag(models.Model):
    """
    Class: 标签数据模型的class
    """
    name = models.CharField('文章标签', max_length=20)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(default=timezone.now)
    description = models.TextField('描述', max_length=240, default=settings.SITE_DESCRIPTION,
                                   help_text='用来作为SEO中description,长度参考SEO标准')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'slug': self.slug})

    def get_article_list(self):
        """
        Return返回当前标签下所有发表的文章列表
        """
        return Article.objects.filter(tags=self)


class Category(models.Model):
    """
    分类数据模型
    """
    # avatar = models.ImageField(upload_to='category/%Y%m%d/', blank=True)
    name = models.CharField('文章分类', max_length=20)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(default=timezone.now)
    description = models.TextField('描述', max_length=240, default=settings.CATEGORY_DEFAULT_DESCRIPTION,
                                   help_text='用来作为SEO中description,长度参考SEO标准')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('article:category', kwargs={'slug': self.slug})

    def get_article_list(self):
        return Article.objects.filter(category=self)


class Article(models.Model):
    """
    # 博客文章数据模型
    """
    # 文章作者。参数 on_delete 用于指定数据删除的方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100)
    # 文章描述。120字左右
    description = models.TextField('文章描述', max_length=150, default='文章描述')

    # 文章正文。保存大量文本使用 TextField
    body = models.TextField('文章内容')

    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)
    # 浏览量
    total_views = models.PositiveIntegerField(default=0)
    # 是否置顶
    is_top = models.BooleanField('置顶', default=False)

    # 文章分类
    category = models.ForeignKey(Category, verbose_name='文章分类', default=1, on_delete=models.PROTECT)
    # 文章标签
    tags = models.ManyToManyField(Tag, verbose_name='标签')

    # 文章标题图
    # avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)

    # 文章唯一表示符
    slug = models.SlugField(unique=True)

    # 更新浏览量
    def update_views(self):
        self.total_views += 1
        self.save(update_fields=['total_views'])

    # 搜索框的markdown
    def body_to_markdown(self):
        return markdown.markdown(self.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.slug])

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        verbose_name = '博客'
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-created', '-total_views')

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # return self.title 将文章标题返回
        return self.title

    def get_pre(self):
        return Article.objects.filter(id__lt=self.id).order_by('-id').first()

    def get_next(self):
        return Article.objects.filter(id__gt=self.id).order_by('id').first()
