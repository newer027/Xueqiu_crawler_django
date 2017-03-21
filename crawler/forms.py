from django import forms
from .models import Portfolio


class CrawlerForm(forms.ModelForm):

    class Meta:
        model = Portfolio
        fields = ('title',) #表单的字段