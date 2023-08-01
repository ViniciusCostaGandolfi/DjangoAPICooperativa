from django.urls import include, path
from cooperative.views import RouteViewSet
from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

#from users.views import UserViewSet



router = routers.DefaultRouter()
router.register('route', RouteViewSet, basename='rotas')


schema_view = get_schema_view(
    openapi.Info(
        title="Minha API",
        default_version='v1',
        description="Descrição da minha API",
        terms_of_service="https://www.minhaapi.com/terms/",
        contact=openapi.Contact(email="contato@minhaapi.com"),
        license=openapi.License(name="Licença da minha API"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[path('cooperative/', include('cooperative.urls'))],
)


urlpatterns = [
    path('api/', include(router.urls)),
    # path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
# rotafood.railway.app/logistic
# rotafood.railway.app/orders
# rotafood.railway.app/products
# rotafood.railway.app/deliveryman
# rotafood.railway.app/registrar-usuario/