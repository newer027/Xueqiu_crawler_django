from rest_framework import generics
from ..models import Positions_change, Accumulated_position, Portfolio
from .serializers import Positions_change_Serializer, Accumulated_position_Serializer, Portfolio_Serializer
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

class Positions_change_ListView(generics.ListAPIView):
   queryset = Positions_change.objects.all()
   serializer_class = Positions_change_Serializer


"""
class Positions_change_DetailView(generics.RetrieveAPIView):
   queryset = Positions_change.objects.all()
   serializer_class = Positions_change_Serializer
"""


class Accumulated_position_ListView(generics.ListAPIView):
   queryset = Accumulated_position.objects.all()
   serializer_class = Accumulated_position_Serializer


"""
class Accumulated_position_DetailView(generics.RetrieveAPIView):
   queryset = Accumulated_position.objects.all()
   serializer_class = Accumulated_position_Serializer


class PortfolioViewSet(viewsets.ReadOnlyModelViewSet):
   queryset = Portfolio.objects.all()
   serializer_class = Portfolio_Serializer
"""


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 4


class PortfolioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = Portfolio_Serializer
    pagination_class = LargeResultsSetPagination

    @detail_route(methods=['get'],
            serializer_class=Portfolio_Serializer,
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])

    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class Positions_change_List(generics.ListAPIView):
    serializer_class = Positions_change_Serializer

    def get_queryset(self):
        portfolio = self.kwargs['portfolio']
        return Positions_change.objects.filter(portfolio=portfolio)


class Accumulated_position_List(generics.ListAPIView):
    serializer_class = Accumulated_position_Serializer

    def get_queryset(self):
        portfolio = self.kwargs['portfolio']
        return Accumulated_position.objects.filter(portfolio=portfolio)