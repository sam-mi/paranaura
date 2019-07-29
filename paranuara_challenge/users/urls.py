from django.conf.urls import url


from config.urls import router
from .views import UserViewSet, GroupViewSet


from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.UserListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'
    ),
    url(
        regex=r'^(?P<username>[\w.@+-]+)/$',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),
    url(
        regex=r'^~update/$',
        view=views.UserUpdateView.as_view(),
        name='update'
    ),
    url(
        regex=r'^~email/$',
        view=views.UserEmailView.as_view(),
        name='email'
    )
]


router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)


