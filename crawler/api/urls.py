from django.conf.urls import url, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register('portfolio', views.PortfolioViewSet)
#router.register('positions_change_list', views.Positions_change_ListView)
#router.register('accumulated_position_list', views.Accumulated_position_ListView)

urlpatterns = [
    url(r'^positions_change/$',
        views.Positions_change_ListView.as_view(), name='positions_change_list'),
    #url(r'^positions_change/(?P<pk>\d+)/$',
    #    views.Positions_change_DetailView.as_view(), name='positions_change_detail'),
    url(r'^accumulated_position/$',
        views.Accumulated_position_ListView.as_view(), name='accumulated_position_list'),
    #url(r'^accumulated_position/(?P<pk>\d+)/$',
    #    views.Accumulated_position_DetailView.as_view(), name='accumulated_position_detail'),
    url('^positions_change/(?P<portfolio>\d+)$', views.Positions_change_List.as_view()),
    url('^accumulated_position/(?P<portfolio>\d+)$', views.Accumulated_position_List.as_view()),
    url(r'^', include(router.urls)),
]