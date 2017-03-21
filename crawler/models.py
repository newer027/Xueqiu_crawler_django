from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.core.urlresolvers import reverse


class Portfolio(models.Model):
    STAUTS_CHOICE = (
        ('pending', 'Pending'),
        ('done', 'Done'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    created = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STAUTS_CHOICE, default='pending')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) #slugify的用法
        super(Portfolio, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('crawler:detail', args=[self.slug])


class Positions_change(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='changes')
    time = models.DateTimeField()
    name = models.CharField(max_length=80)
    code = models.CharField(max_length=20)
    detail = models.CharField(max_length=80)

    class Meta:
        ordering = ('-time',)

    def __str__(self):
        return '{} changed: {}, followed by {}'.format(self.name, self.detail, self.portfolio)


class Accumulated_position(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='accum')
    stock = models.CharField(max_length=20)
    percent = models.DecimalField(max_digits=10, decimal_places=2)
    people = models.PositiveIntegerField(db_index=True, default=0)

    class Meta:
        ordering = ('percent',)

    def __str__(self):
        return '{} totol percentage: {}, followed by {}'.format(self.stock, self.percent, self.portfolio)