from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices



@python_2_unicode_compatible
class User(AbstractUser):
    

    # First Name and Last Name do not cover name patterns
    # around the globe.
    salutation = models.CharField(_('Salutation'), blank=True, null=True, max_length=55)
    name = models.CharField(_('Name of User'), blank=True, null=True, max_length=255)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    

    def get_full_name(self):
        if not self.name == '':
            return self.name
        else:
            return self.username

    



