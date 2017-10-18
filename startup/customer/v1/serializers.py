from rest_framework import serializers

from customer import models


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Customer
