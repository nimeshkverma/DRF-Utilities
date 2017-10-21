from rest_framework.views import APIView
from rest_framework import status
from decorators import meta_data_response, catch_exception
from services import config_service
from response import MetaDataResponse
import logging
LOGGER = logging.getLogger(__name__)


class Config(APIView):

    @catch_exception(LOGGER)
    def get(self, request):
        return MetaDataResponse(config_service.Config().data, status=status.HTTP_200_OK)
