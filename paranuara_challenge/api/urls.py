from django.urls import path, include
from rest_framework import routers

from config.urls import router
from paranuara_challenge.paranuara import urls


urlpatterns = [
    path('', include(router.urls)),
    path('', include(urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
