from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
    openapi.Info(
        title="Minha APIss",
        default_version='v2',
        description="Descrição da minha APIaa",
        terms_of_service="https://www.minhaapi.com/terms/",
        contact=openapi.Contact(email="contato@minhaapi.com"),
        license=openapi.License(name="Licença da minha API"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
 
 
urlpatterns = [
    path('cooperative/', include('cooperative.urls')),
]