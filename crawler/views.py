# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CrawlerForm
from .models import Portfolio, Accumulated_position, Positions_change
from django.contrib import messages



def dashboard(request):
    portfolios = Portfolio.objects.all()
    form = CrawlerForm(data=request.POST or None)
    if form.is_valid():
        new_item = form.save(commit=False)
        if not Portfolio.objects.filter(title=new_item.title):
            new_item.save()
            messages.success(request, 'Portfolio added successfully')
            return redirect('/crawler')
        else:
            messages.error(request, 'Portfolio already in the database')
    return render(request, 'crawler/dashboard.html', {'form': form,
                                                      'portfolios': portfolios}) #render的用法


def portfolio_detail(request, slug):
    portfolio = get_object_or_404(Portfolio, slug = slug) #get_object_or_404的用法
    accums = Accumulated_position.objects.filter(portfolio=portfolio)
    positions = Positions_change.objects.filter(portfolio=portfolio)
    return render(request, 'crawler/crawler/detail.html', {'portfolio': portfolio, 'accums':accums, 'positions':positions}) #render的用法