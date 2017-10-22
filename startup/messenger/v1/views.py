from django.shortcuts import get_object_or_404, render
from rest_framework import mixins, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import signing

from common.v1.decorators import session_authorize, meta_data_response, catch_exception
from social.models import Login

from . import serializers
from messenger import models

from . tasks import send_verification_mail

import logging
LOGGER = logging.getLogger(__name__)


class EmailVerificationCreate(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize('customer_id')
    def post(self, request, auth_data):
        if auth_data.get('authorized'):
            serializer = serializers.EmailVerificationSerializer(
                data=request.data)
            if serializer.is_valid():
                serializer.validate_foreign_keys()
                email_object = serializer.save()
                send_verification_mail(
                    serializers.EmailVerificationSerializer(email_object).data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class EmailVerificationDetail(APIView):

    def get(self, request, encoded_data):
        try:
            email_data = signing.loads(encoded_data)
            if 'is_verified' in email_data.keys():
                email_data.pop('is_verified')
            email_verification_object = get_object_or_404(
                models.EmailVerification, **email_data)
            serializers.EmailVerificationSerializer().validate_foreign_keys(email_data)
            email_object_updated = serializers.EmailVerificationSerializer().update(
                email_verification_object, {'is_verified': True})
            return render(request, 'messenger/v1/email_verification_success.html')
        except Exception as e:
            return render(request, 'messenger/v1/email_verification_failure.html')
