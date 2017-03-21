from rest_framework import serializers
from ..models import Positions_change, Accumulated_position, Portfolio


class Positions_change_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Positions_change
        fields = ('portfolio', 'time', 'name', 'code', 'detail')


class Accumulated_position_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Accumulated_position
        fields = ('portfolio', 'stock', 'percent', 'people')


class Portfolio_Serializer(serializers.ModelSerializer):
    accum = Accumulated_position_Serializer(many=True, read_only=True)
    changes = Positions_change_Serializer(many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = ('title', 'slug', 'created', 'status', 'accum', 'changes')