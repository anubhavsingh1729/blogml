from django.shortcuts import render,redirect,get_object_or_404
from . models import News,Post
import requests
from bs4 import BeautifulSoup
import json
from datetime import timedelta, timezone, datetime
import os
import shutil
import math
from . forms import PostForm
from django.views import generic

from django.contrib.auth import logout as auth_logout
# Create your views here.

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid:
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = datetime.now()
            post.save()
    else:
        form = PostForm()
    return render(request, 'post_new.html', {'form': form})

def scrape(request):
    News.objects.all().delete()
    #user_p = userProfile.objects.filter(user=request.user).first()
    #user_p.last_scrape = datetime.now(timezone.utc)
    #user_p.save()

    url = 'https://inshorts.com/en/read'
    response = requests.get(url)
    response_text = response.text
    soup = BeautifulSoup(response_text, 'lxml')
    headlines = soup.find_all(attrs={"itemprop": "headline"})
    articlebody = soup.find_all(attrs = {"itemprop": "articleBody"})
    author = soup.find_all(attrs = {"class": "author"})
    datemonth = soup.find_all(attrs = {"class": "date"})
    for i in range(len(list(headlines))):
        headline = headlines[i].text
        body = articlebody[i].text
        auth = author[2*i].text
        date = datemonth[i].text

        new_news = News()
        new_news.headline = headline
        new_news.text = body
        new_news.author = auth
        new_news.datemonth = date
        new_news.save()
    return redirect('/index/')

def index(request):
    news = News.objects.all()
    post = Post.objects.all().order_by('-published_date')
    context = {
        "object_list":news,
        "post_list":post,
    }
    return render(request,'index.html',context = context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

def getmypost(request):
    post = Post.objects.filter(author = request.user)
    return render(request,'postlist.html',{'post_list':post})

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return index(request)