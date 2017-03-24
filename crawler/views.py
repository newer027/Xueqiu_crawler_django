# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CrawlerForm
from .models import Portfolio, Accumulated_position, Positions_change
from django.contrib import messages
from crawler.login import login
import requests
from bs4 import BeautifulSoup

agent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
headers = {
    'User-Agent': agent,
    'Host': "xueqiu.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6",
    "Connection": "keep-alive"
}
session = requests.session()


telephone = '18154377749'
password  = 'ML34gbxq'

def dashboard(request):
    portfolios = Portfolio.objects.all()
    form = CrawlerForm(data=request.POST or None)
    if form.is_valid():
        new_item = form.save(commit=False)
        url = 'https://xueqiu.com/'+new_item.title
        headers = login(telephone, password)
        data = session.get(url, headers=headers).text
        try:
            soup = BeautifulSoup(data, "lxml")
            followers = soup.find('li', class_="gender_info" )
            try:
                followers = followers.find_next_siblings("li")[0]
                followers = followers.contents[0]
                slug = soup.find('a', class_="setRemark" )['data-user-id']
            except:
                followers = "无可奉告"
                slug = new_item.title
            if not Portfolio.objects.filter(slug=slug):
                new_item.name = soup.title.string[0:len(soup.title.string)-4]
                new_item.followers = followers
                new_item.slug= slug
                new_item.save()
                messages.success(request, 'Portfolio added successfully')
                return redirect('/crawler')
            else:
                messages.error(request, 'Portfolio already in the database')
        except:
            messages.error(request, 'Portfolio does not exist')
    return render(request, 'crawler/dashboard.html', {'form': form,
                                                      'portfolios': portfolios})


def portfolio_detail(request, slug):
    portfolio = get_object_or_404(Portfolio, slug = slug) #get_object_or_404的用法
    accums = Accumulated_position.objects.filter(portfolio=portfolio)
    positions = Positions_change.objects.filter(portfolio=portfolio)
    return render(request, 'crawler/crawler/detail.html', {'portfolio': portfolio, 'accums':accums, 'positions':positions}) #render的用法
