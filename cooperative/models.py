from django.db import models


class Route(models.Model):
    text_route = models.CharField(max_length=2048)
    google_maps_link = models.CharField(max_length=2048)
    sorted_route_indexes = models.JSONField()
    use_longest_point = models.BooleanField(default=None, null=True)
    
class Base(models.Model):
    adress = models.CharField(max_length=1024, default='R. Domingos Rodrigues, 420 - Lapa', null=True)
    adress_complement = models.CharField(max_length=1024, default='', null=True)
    latitude = models.FloatField(null=True, default=-23.5219926)
    longitude = models.FloatField(null=True, default=-46.7076168)
    route = models.OneToOneField(Route, null=True, on_delete=models.SET_NULL,related_name="base")
    

class Order(models.Model):
    name = models.CharField(max_length=128)
    itens = models.CharField(max_length=2048)
    adress = models.CharField(max_length=1024)
    phone = models.CharField(max_length=20)
    adress_complement = models.CharField(max_length=1024)
    latitude = models.FloatField()
    longitude = models.FloatField()
    route = models.ForeignKey(Route, null=True, on_delete=models.SET_NULL,related_name="orders")

class Driver(models.Model):
    name = models.CharField(max_length=128)
    itens_list = models.CharField(max_length=2048)
    adress = models.CharField(max_length=1024, null=True)
    adress_complement = models.CharField(max_length=1024, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    route = models.OneToOneField(Route, null=True, on_delete=models.SET_NULL,related_name="route")
