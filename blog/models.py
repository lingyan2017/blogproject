import markdown
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags


class Category(models.Model):

    name = models.CharField(max_length=100,verbose_name='分类名')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField(max_length=100,verbose_name='标签名')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):

    title = models.CharField(max_length=70,verbose_name='文章标题')
    body = models.TextField(verbose_name='文章正文')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')

    excerpt = models.CharField(max_length=200,blank=True,verbose_name='摘要')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,verbose_name='类别')
    tags = models.ManyToManyField(Tag,blank=True,verbose_name='标签')
    author = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='作者')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def save(self,*args,**kwargs):
        # 首先实例化一个 Markdown 类，用于渲染 body 的文本。
        # 由于摘要并不需要生成文章目录，所以去掉了目录拓展。
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        # 先将 Markdown 文本渲染成 HTML 文本
        # strip_tags 去掉 HTML 文本的全部 HTML 标签
        # 从文本摘取前 54 个字符赋给 excerpt
        self.excerpt = strip_tags(md.convert(self.body))[:54]

        super().save(*args, **kwargs)
