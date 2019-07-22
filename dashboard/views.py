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

import os
from django.conf import settings
# Create your views here.
#------------------------------------LDA MODEL--------------------------------------------------------
import gensim
from gensim import models, corpora
from gensim.similarities import MatrixSimilarity
from nltk import word_tokenize
from nltk.corpus import stopwords


import pandas as pd
import re

import pickle

def clean_text(text):
    STOPWORDS = stopwords.words('english')
    tokenized_text = word_tokenize(text.lower())
    cleaned_text = [t for t in tokenized_text if t not in STOPWORDS and re.match(r'[a-zA-Z\-][a-zA-Z\-]{2,}', t)]
    return cleaned_text

def findtopic(text):
    dictionary = corpora.Dictionary.load_from_text(os.path.join(settings.BASE_DIR, 'dictionary'))
    bow = dictionary.doc2bow(clean_text(text))
    ldamodel = models.LdaModel.load('ldamodel')
    topics = ldamodel[bow]
    topicidlist = []
    for i in topics:
        topicid,prob = i
        topicidlist.append(topicid)
    return ''.join([str(x) for x in topicidlist])

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = datetime.now()
            topics = findtopic(post.text)
            post.topic = topics
            post.save()
            form = PostForm()
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
    post = Post.objects.order_by('-published_date')[:6]
    context = {
        "object_list":news,
        "post_list":post,
    }
    return render(request,'index.html',context = context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    posttopic = post.topic
    relpost = Post.objects.filter(topic = posttopic).exclude(pk=pk)
    #print("relatedpost",relpost,"posttopic",posttopic)
    return render(request, 'post_detail.html', {'post': post,'related':relpost})

def getmypost(request):
    post = Post.objects.filter(author = request.user)
    return render(request,'postlist.html',{'post_list':post,'info':"My Articles",'deletebtn':1})

def getallpost(request):
    post = Post.objects.order_by('-published_date')
    return render(request,'postlist.html',{'post_list':post,'info':"All Articles"})

def deletemypost(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('/postlist/user/')

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return index(request)