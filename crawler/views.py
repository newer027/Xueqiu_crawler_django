# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CrawlerForm
from .models import Portfolio, Accumulated_position, Positions_change
from django.contrib import messages
from crawler.login import login
import json
import requests


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
        url0 = 'https://xueqiu.com/stock/portfolio/stocks.json?size=1000&pid=-1&tuid='+new_item.title+'&cuid=1180102135&_=1477728185503'
        headers = login(telephone, password)
        data = session.get(url0, headers=headers).text
        data = json.loads(data)
        if "stocks" in data:
            if not Portfolio.objects.filter(title=new_item.title):
                new_item.save()
                messages.success(request, 'Portfolio added successfully')
                return redirect('/crawler')
            else:
                messages.error(request, 'Portfolio already in the database')
        else:
            messages.error(request, 'Portfolio does not exist')
    return render(request, 'crawler/dashboard.html', {'form': form,
                                                      'portfolios': portfolios}) #render的用法


def portfolio_detail(request, slug):
    portfolio = get_object_or_404(Portfolio, slug = slug) #get_object_or_404的用法
    accums = Accumulated_position.objects.filter(portfolio=portfolio)
    positions = Positions_change.objects.filter(portfolio=portfolio)
    return render(request, 'crawler/crawler/detail.html', {'portfolio': portfolio, 'accums':accums, 'positions':positions}) #render的用法