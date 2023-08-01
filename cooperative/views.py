from dataclasses import asdict
from typing import List
from django.http import HttpRequest
from rest_framework import status
from rest_framework import viewsets, permissions
from cooperative.dataclasses import BaseData, DriverData, OrderData, RouteData
from cooperative.utilits.cooperative_travel_salesman import CooperativeTravelSalesman

from .serializers import *
from rest_framework.request import Request
from rest_framework.response import Response



class RouteViewSet(viewsets.ModelViewSet):
    serializer_class  = RouteSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Route.objects.all()
    
    
    
    def get_text_orders(self, driver: DriverData, orders: List[OrderData], sorted_indexes: List[int]) -> str:
        text_orders = f'''
        *Rota do: {driver.name}!*
        Itens da Rota: {driver.itens_list}
        
        '''
        for i, index in enumerate(sorted_indexes):
            index = index - 1
            text = f'''
            ----------------------------------
            Pedido {i+1}
            Nome: {orders[index].name}
            Endereço: {orders[index].adress} {orders[index].adress_complement} 
            Itens: {orders[index].itens}
            Telefone: {orders[index].phone}
            '''
            text_orders += text
            # print(text)
        text_orders += '----------------------------------'
        text_orders += f'\n\n Agr {driver}! \n\n'
        return  text_orders
            
    
    def get_lint_google_maps(self, points: List[List[float]], sorted_indexes: List[int]) -> str:
        link_google_maps = 'https://www.google.com/maps/dir/'
        for index in sorted_indexes:
            point = points[index]
            link_google_maps += f'{point[0]},{point[1]}/'
        return link_google_maps
        
    def create(self, request: Request, *args, **kwargs):
        serializer = RouteSerializer(data=request.data)
        json = {}
        if serializer.is_valid(raise_exception=True):
            base = BaseData(**serializer.validated_data.get('base', {}))
            driver: DriverData = DriverData(**serializer.validated_data.get('driver', {}))
            orders: List[OrderData] = [OrderData(**order_data) for order_data in serializer.validated_data.get('orders', [])]
            route = RouteData(base=base, orders=orders, driver=driver)
            # use_longest_point: bool | None = serializer.validated_data.get("use_longest_point", None)
            
            
            # print(route.__dict__)
            points_lat_lon = [[route.base.latitude, route.base.longitude]]
            for order in route.orders:
                points_lat_lon.append([order.latitude, order.longitude])
                
                
            if route.driver.latitude is not None and route.driver.longitude is not None:
                points_lat_lon.append([route.driver.latitude, route.driver.longitude])
                
                instance = CooperativeTravelSalesman(points=points_lat_lon, use_last_point=True)
                answer = instance.resolve()
                route.text_route = self.get_text_orders(route.driver, route.orders, answer["ordem"][1:-2])
                route.google_maps_link = self.get_lint_google_maps(points_lat_lon, answer["ordem"][:-1])
                route.sorted_route_indexes = answer["ordem"]
            
            
            elif route.use_longest_point is not None:                
                instance = CooperativeTravelSalesman(points=points_lat_lon, use_last_point=True)
                answer = instance.resolve()
                route.text_route = self.get_text_orders(route.driver, route.orders, answer["ordem"][1:-1])
                route.google_maps_link = self.get_lint_google_maps(points_lat_lon, answer["ordem"][:-1])
                route.sorted_route_indexes = answer["ordem"]
                
                

            return Response({"data": asdict(route)}, status=status.HTTP_201_CREATED, *args, **kwargs)
            # return super().create(request, *args, **kwargs)