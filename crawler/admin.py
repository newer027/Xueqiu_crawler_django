from django.contrib import admin
from .models import Portfolio, Positions_change, Accumulated_position


class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created', 'status', 'num', 'name', 'followers')
admin.site.register(Portfolio, PortfolioAdmin)


class Positions_change_Admin(admin.ModelAdmin):
    list_display = ('portfolio', 'time', 'name', 'code',
                       'detail')
    list_filter = ('portfolio', 'name')
admin.site.register(Positions_change, Positions_change_Admin)


class Accumulated_position_Admin(admin.ModelAdmin):
    list_display = ('portfolio', 'stock', 'percent', 'people')
    list_filter = ('portfolio','people')
admin.site.register(Accumulated_position, Accumulated_position_Admin)