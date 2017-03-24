from crawler.models import Portfolio
from polls.models import Question
from django.shortcuts import render


def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    portfolio=Portfolio.objects.all().count()
    question=Question.objects.count()  # The 'all()' is implied by default.

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'portfolio':portfolio,'question':question},
    )