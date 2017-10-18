from datetime import datetime
from django.core.validators import RegexValidator
from django.db import models

mobile_number_regex = RegexValidator(
    regex=r'^$|\d{10}$', message="Mobile number must be entered in the format: '9999999999'. 10 digits allowed.")
pan_regex = RegexValidator(
    regex=r'[a-zA-Z]{5}\d{4}[a-zA-Z]{1}', message="PAN must be entered in the format: 'ABCDE1234F'. 10 Characters allowed.")
aadhaar_regex = RegexValidator(
    regex=r'^\d{12}$', message="AADHAAR must be entered in the format: '123456789123'. 12 digits allowed.")
alphabet_regex = RegexValidator(
    regex=r'[a-zA-Z]+', message="Data must be entered in Alphabets only.")
alphabet_regex_allow_empty = RegexValidator(
    regex=r'$|[a-zA-Z]+', message="Data must be entered in Alphabets only.")
alphabet_whitespace_regex = RegexValidator(
    regex=r'[a-zA-Z ]+', message="Data must be entered in Alphabets only.")
alphabet_whitespace_regex_allow_empty = RegexValidator(
    regex=r'$|[a-zA-Z ]+', message="Data must be entered in Alphabets only.")
pincode_regex = RegexValidator(
    regex=r'^[1-9][0-9]{5}$', message="Pincode must be entered in format: '123456'. 6 Characters allowed.")
numeric_regex = RegexValidator(
    regex=r'[0-9]+', message="Data must be entered in Digits only.")
YEAR_CHOICES = []
for r in range(1950, (datetime.now().year + 1)):
    YEAR_CHOICES.append((r, r))


MALE = 'Male'
FEMALE = 'Female'
OTHER = 'Other'

GENDER_CHOICES = (
    (MALE, 'Male'),
    (FEMALE, 'Female'),
    (OTHER, 'Other')
)


class LifeTimeTrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class ActiveModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class InActiveModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ActiveObjectManager(models.Manager):

    def get_queryset(self):
        return super(ActiveObjectManager, self).get_queryset().filter(is_active=True).order_by('pk')
