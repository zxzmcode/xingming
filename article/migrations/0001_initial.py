# Generated by Django 3.2.6 on 2021-09-12 00:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='文章分类')),
                ('slug', models.SlugField(unique=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.TextField(default='XCode是行茗的个人技术博客', help_text='用来作为SEO中description,长度参考SEO标准', max_length=240, verbose_name='描述')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='文章标签')),
                ('slug', models.SlugField(unique=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.TextField(default='izone 是一个使用 Django+Bootstrap4 搭建的个人博客类型网站', help_text='用来作为SEO中description,长度参考SEO标准', max_length=240, verbose_name='描述')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(default='文章描述', max_length=150, verbose_name='文章描述')),
                ('body', models.TextField(verbose_name='文章内容')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('total_views', models.PositiveIntegerField(default=0)),
                ('is_top', models.BooleanField(default=False, verbose_name='置顶')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='article.category', verbose_name='文章分类')),
                ('tags', models.ManyToManyField(to='article.Tag', verbose_name='标签')),
            ],
            options={
                'verbose_name': '博客',
                'ordering': ('-created', '-total_views'),
            },
        ),
    ]
