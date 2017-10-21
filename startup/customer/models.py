from django.db import models
from common.models import ActiveModel, ActiveObjectManager


class Customer(ActiveModel):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(
        blank=True, null=True, max_length=256)
    last_name = models.CharField(
        blank=True, null=True, max_length=256)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    def validate_customer(self, customer_id):
        is_valid_customer = False
        if Customer.active_objects.get(pk=customer_id):
            is_valid_customer = True
        return is_valid_customer

    def save(self, *args, **kwargs):
        # Do some task which you want to do before saving the object into the database
        # This is for demonstration as we are not doing anything after the
        # override
        super(Customer, self).save(*args, **kwargs)

    @staticmethod
    def exists(customer_id):
        exists = False
        customer_objects = Customer.objects.filter(customer_id=customer_id)
        if customer_objects:
            exists = True
        return exists

    class Meta(object):
        db_table = "customer"

    def __unicode__(self):
        return "%s__%s__%s" % (str(self.id), str(self.first_name), str(self.last_name))
