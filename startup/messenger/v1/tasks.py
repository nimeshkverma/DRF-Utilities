from __future__ import absolute_import
import requests
from . services import email_service
# from upwards.celery import app


# @app.task
def send_verification_mail(email_verify_data):
    email_service.send_verification_mail(email_verify_data)


# @app.task
def update_email_models(email_object_updated):
    email_service.update_email_models(email_object_updated)

# The commented code is for utilising Celery.
