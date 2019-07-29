import uuid

from django.db import models
from django.utils import timezone
from model_utils import Choices
from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager


class Company(TimeStampedModel):
    """
    A Company on Paranuara
    """
    name = models.CharField(
        max_length=255,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Food(TimeStampedModel):
    """
    Food available on Paranuara
    """

    name = models.CharField(
        max_length=55,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


GENDER_CHOICES = Choices(
    ('unknown', 'unknown', 'Unknown'),
    ('male', 'male', 'Male'),
    ('female', 'female', 'Female'),
    ('non_binary', 'non_binary', 'Non Binary'),
)


class Person(TimeStampedModel):
    """
    A Citizen of the Colony of Paranuara
    """

    #### REQUIRED ############################################

    guid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4
    )
    _id = models.CharField(
        max_length=24,
        help_text="External System ID"
    )
    index = models.PositiveIntegerField(
        help_text="External System Index"
    )
    name = models.CharField(
        max_length=255,
    )
    email = models.EmailField()

    #### RELATIONS ############################################

    company = models.ForeignKey(
        Company,
        db_index=True,
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='employees'
    )
    friends = models.ManyToManyField(
        "Person",
        blank=True
    )
    food = models.ManyToManyField(
        "Food",
        help_text="Favourite Foods",
        blank=True
    )

    #### OPTIONAL ############################################

    address = models.TextField(
        max_length=255,
        blank=True,
    )
    registered = models.DateTimeField(
        default=timezone.now,
    )
    gender = models.CharField(
        max_length=12,
        choices=GENDER_CHOICES,
        default=GENDER_CHOICES.unknown
    )
    age = models.PositiveSmallIntegerField()
    picture = models.CharField(
        max_length=255,
        help_text="URL for picture",
        blank=True,
    )
    greeting = models.CharField(
        max_length=255,
        blank=True
    )
    phone = models.CharField(
        max_length=30,
        blank=True,
    )
    eye_color = models.CharField(
        max_length=15,
        blank=True
    )
    balance = models.DecimalField(
        decimal_places=2,
        default=0.00,
        max_digits=6
    )
    has_died = models.BooleanField(
        default=False,
    )
    about = models.TextField(
        blank=True
    )


    tags = TaggableManager(blank=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-index',)
        unique_together = ['name', 'email']
