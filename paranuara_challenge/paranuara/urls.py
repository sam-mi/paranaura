from django.urls import path

from config.urls import router
from paranuara_challenge.paranuara import views

router.register(r'companies', views.CompanyViewSet)
router.register(r'food', views.FoodViewSet)
router.register(r'people', views.PersonViewSet)

urlpatterns = [
    path('friends/<int:pk>/<int:friend>/', views.CommonFriendsViewSet.as_view({'get': 'retrieve'}), name='friends'),
]
