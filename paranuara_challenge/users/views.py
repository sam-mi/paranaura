from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from allauth.account.views import EmailView


from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions, status, mixins
from django.contrib.auth.models import Group
from .serializers import UserSerializer, GroupSerializer, PasswordSerializer
from .permissions import IsAdminOrIsSelf

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse(
            'users:detail',
            kwargs={'username': self.request.user.username}
        )


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', ]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse(
            'users:detail',
            kwargs={'username': self.request.user.username}
        )

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserEmailView(LoginRequiredMixin, EmailView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.request.user
        return context



class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        methods=['post'],
        detail=True,
        serializer_class=PasswordSerializer,
        permission_classes=[IsAdminOrIsSelf])
    def update_password(self, request, pk=None):
        user = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({
                    'message': "Incorrect old password"
                })
            data = serializer.validated_data
            if data['new_password'] == data['confirm_password']:
                user.set_password(data['new_password'])
                user.save()
                return Response({'status': 'password set'})
            else:
                return Response({
                    'message': "Your passwords don't match",
                })
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class GroupViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer





