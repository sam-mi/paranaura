from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.urls import path


from rest_framework import routers

from paranuara_challenge.paranuara import views

router = routers.DefaultRouter()

router.register(r'companies', views.CompanyViewSet)
router.register(r'food', views.FoodViewSet)
router.register(r'people', views.PersonViewSet)

urlpatterns = [

    # API URLS
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # FRIENDS
    path('api/friends/<int:pk>/<int:friend>/', views.CommonFriendsViewSet.as_view({'get': 'retrieve'}), name='friends'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:

    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
