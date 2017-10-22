import requests
from django.conf import settings


def send_otp(otp_data):
    url = settings.SMS_GATEWAY_URL.format(sms_gateway_api_key=settings.SMS_GATEWAY_API_KEY,
                                          mobile_number=otp_data[
                                              "mobile_number"],
                                          otp_code=otp_data["otp_code"],
                                          sms_gateway_template=settings.SMS_GATEWAY_TEMPLATE)
    response = requests.request("GET", url)
    return response
