import re

import markdown
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

from blog.models import Post, Category, Tag


def index(request):
    post_list = Post.objects.all()
    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context=context)


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 'markdown.extensions.toc',
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'blog/detail.html', context={'post': post})


def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year, created_time__month=month)
    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context=context)


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context=context)


def tag(request, pk):
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t)
    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context=context)
