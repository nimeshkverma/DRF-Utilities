from django.db import models


class Customer(models.Model):
    first_name = models.CharField(
        blank=False, null=False, max_length=256, unique=True)
    last_name = models.CharField(
        blank=False, null=False, max_length=256, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s__%s__%s" % (str(self.id), str(self.first_name), str(self.last_name))
