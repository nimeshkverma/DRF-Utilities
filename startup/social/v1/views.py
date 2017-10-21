from copy import deepcopy
from rest_framework import status, mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from common.v1.decorators import session_authorize, meta_data_response, catch_exception, iam
from customer.models import Customer

from . import serializers
from social import models
from . import utils

import logging
LOGGER = logging.getLogger(__name__)


class SocialLogin(APIView):

    # @catch_exception(LOGGER)
    @meta_data_response()
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            social_login_data = serializer.save()
            return Response(social_login_data, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SocialLogout(APIView):

    # @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def post(self, request, auth_data):
        if auth_data.get('authorized'):
            serializer = serializers.LogoutSerializer(data=auth_data)
            if serializer.is_valid():
                serializer.save()
                return Response({}, status.HTTP_204_NO_CONTENT)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class LinkedinAuth(APIView):

    def authorize_and_parse_linkedin(self, request_data):
        processed_state = self.process_state(request_data.get('state', ''))
        request_data.update(processed_state)
        serializer = serializers.LinkedinAuthSerializer(data=request_data)
        if serializer.is_valid():
            serializer.validate_foreign_keys()
            serializer.upsert()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status.HTTP_400_BAD_REQUEST)

    def process_state(self, state):
        state_raw_list = state.split(',')
        state_dict = {}
        for raw_param in state_raw_list:
            raw_param_list = raw_param.split(':')
            state_dict[raw_param_list[0]] = raw_param_list[1]
        return state_dict

    # @catch_exception(LOGGER)
    @meta_data_response()
    def get(self, request):
        request_data = deepcopy(request.GET)
        if request_data:
            return self.authorize_and_parse_linkedin(request_data)
        else:
            return Response({}, status.HTTP_200_OK)


class SocialProfiles(APIView):

    # @catch_exception(LOGGER)
    @meta_data_response()
    def get(self, requests, customer_id):
        if Customer.exists(customer_id):
            return Response(utils.get_customer_profiles(customer_id), status.HTTP_200_OK)
        else:
            return Response({}, status.HTTP_404_NOT_FOUND)


class SessionDataList(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      generics.GenericAPIView):
    queryset = models.Login.objects.all().order_by('customer')
    serializer_class = serializers.SessionDataSerializer

    # @catch_exception(LOGGER)
    @meta_data_response()
    @iam('admin')
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # @catch_exception(LOGGER)
    @meta_data_response()
    @iam('admin')
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SessionDataDetail(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):
    queryset = models.Login.objects.all()
    serializer_class = serializers.SessionDataSerializer

    # @catch_exception(LOGGER)
    @meta_data_response()
    @iam('admin')
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # @catch_exception(LOGGER)
    @meta_data_response()
    @iam('admin')
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # @catch_exception(LOGGER)
    @meta_data_response()
    @iam('admin')
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
