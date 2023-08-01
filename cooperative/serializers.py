from rest_framework import serializers
from .models import *


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Base
        exclude = ['id', 'route']
        ref_name = 'CooperativeBase'

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        exclude = ['id', 'route']
        ref_name = 'CooperativeDriver'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['id', 'route']
        ref_name = 'CooperativeOrder'
        
class RouteSerializer(serializers.ModelSerializer):
    base = BaseSerializer(required=False, default={
            "adress": "R. Domingos Rodrigues, 420 - Lapa",
            "adress_complement": "",
            "latitude": -23.5219926,
            "longitude": -46.7076168
        }
    )
    driver = DriverSerializer()
    orders = OrderSerializer(many=True)

    class Meta:
        model = Route
        exclude = ['id', 'google_maps_link', 'sorted_route_indexes', "text_route"]
        ref_name = 'CooperativeRoute'
