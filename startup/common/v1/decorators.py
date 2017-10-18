import logging
from functools import wraps
from django.db import IntegrityError
from django.conf import settings
from rest_framework import status
from response import MetaDataResponse
from exceptions import NotAcceptableError, ConflictError


def default_logger():
    logger = logging.getLogger("From the Decorator file")
    return logger


def catch_exception(LOGGER=default_logger()):
    def deco(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except NotAcceptableError as e:
                LOGGER.error("NotAcceptableError:%s" % str(e))
                return MetaDataResponse(e.response, e.meta, status=e.status)
            except ConflictError as e:
                LOGGER.error("MetaDataRresponse:%s" % str(e))
                return MetaDataResponse(e.response, e.meta, status=e.status)
            except IntegrityError as e:
                LOGGER.error("IntegrityError:%s" % str(e))
                return MetaDataResponse({}, str(e), status=status.HTTP_409_CONFLICT)
            except Exception as e:
                LOGGER.error("Encountered Exception%s" % str(e))
                return MetaDataResponse({}, str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return decorated_function
    return deco


def meta_data_response(meta=""):
    def deco(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            vanilla_response = f(*args, **kwargs)
            return MetaDataResponse(vanilla_response.data, meta, status=vanilla_response.status_code)
        return decorated_function
    return deco


def iam(user_group, *args, **kwargs):
    def deco(f):
        def abstract_session_token(request):
            session_token_header_key = 'HTTP_SESSION_TOKEN'
            return request.META.get(session_token_header_key)

        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_name_auth = False
            user_name = kwargs.get('user_name')
            user_name_token = abstract_session_token(args[1])
            if settings.THIRTY_PARTY_SECRETS.get(user_group, {}).get(user_name) == user_name_token:
                user_name_auth = True
            return f(user_name_auth=user_name_auth, *args, **kwargs)
        return decorated_function
    return deco
