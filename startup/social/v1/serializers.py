from rest_framework import serializers
from common.v1.utils.model_utils import check_pk_existence
from common.v1.exceptions import NotAcceptableError
from customer.models import Customer

from social import models

from services.session_service import get_or_create_sessions
from services.social_service import LinkedinProfile


class LoginSerializer(serializers.Serializer):
    platform_token = serializers.CharField()
    source = serializers.ChoiceField(choices=models.SOURCE_CHOICES)
    platform = serializers.ChoiceField(choices=models.PLATFORM_CHOICES)
    imei = serializers.CharField()
    app_registration_id = serializers.CharField(required=False)

    def save(self):
        return get_or_create_sessions(self.validated_data)


class LogoutSerializer(serializers.Serializer):
    session_token = serializers.CharField(max_length=64)
    customer_id = serializers.IntegerField()

    def save(self):
        return models.Login.delete_session(self.validated_data.get(
            "session_token"), self.validated_data.get("customer_id"))


class LinkedinAuthSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()

    def validate_foreign_keys(self, data=None):
        data = data if data else self.validated_data
        model_pk_list = [
            {"model": Customer, "pk": data.get(
                'customer_id', -1), "pk_name": "customer_id"},
        ]
        for model_pk in model_pk_list:
            if model_pk["pk_name"] in data.keys():
                if not check_pk_existence(model_pk['model'], model_pk['pk']):
                    raise NotAcceptableError(
                        model_pk['pk_name'], model_pk['pk'])

    def upsert(self):
        linkedin_profile = LinkedinProfile(self.validated_data.get(
            "code"), self.validated_data.get("state"))
        self.validated_data.update(linkedin_profile.model_data)
        linkedin_objects = models.LinkedinProfile.objects.filter(
            customer_id=self.validated_data['customer_id'])
        if linkedin_objects:
            models.LinkedinProfile.objects.filter(
                customer_id=self.validated_data['customer_id']).update(**self.validated_data)
        else:
            super(LinkedinAuthSerializer, self).save()

    class Meta:
        model = models.LinkedinProfile
        exclude = ('customer', 'created_at', 'updated_at',
                   'is_active', 'id')


class SocialProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SocialProfile
        exclude = ('created_at', 'updated_at', 'id', 'is_active')


class SessionDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Login
        exclude = ('created_at', 'updated_at', 'source', 'id',
                   'deleted_at', 'social_data', 'is_active')
