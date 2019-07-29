from django.urls import path, include
from rest_framework import routers

from config.urls import router
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
from paranuara_challenge.paranuara import views as paranuara_views

router.register(r'companies', paranuara_views.CompanyViewSet)
router.register(r'food', paranuara_views.FoodViewSet)
router.register(r'people', paranuara_views.PersonViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
