import random

from django import template

from article.models import Category, Article, Tag, FriendsLink
from django.db.models.aggregates import Count
from django.utils.html import mark_safe
import re

register = template.Library()


@register.simple_tag()
def get_friends_list():
    """
    返回友情链接列表
    """
    return FriendsLink.objects.all()


@register.simple_tag
def get_tags_list():
    """
    返回标签列表
    """
    return Tag.objects.annotate(total_num=Count('article'))


@register.simple_tag
def get_category_list():
    """
    返回分类列表
    """
    return Category.objects.annotate(total_num=Count('article'))


@register.simple_tag
def get_newest_article():
    """
    获取最新更新的博客文章
    """
    return Article.objects.all().order_by('-updated')[:6]


@register.simple_tag
def my_highlight(text, q):
    """
    自定义标题搜索词高亮函数，忽略大小写
    """
    if len(q) > 1:
        try:
            text = re.sub(q, lambda a: '<span class="highlighted">{}</span>'.format(a.group()),
                          text, flags=re.IGNORECASE)
            text = mark_safe(text)
        except:
            pass
    return text


@register.simple_tag
def get_total_articles():
    """
    获取最新更新的博客文章
    """
    return Article.objects.all()


@register.simple_tag
def get_total_tags():
    """
    获取最新更新的博客文章
    """
    return Tag.objects.all()


@register.simple_tag
def get_total_catagories():
    """
    获取最新更新的博客文章
    """
    return Category.objects.all()

