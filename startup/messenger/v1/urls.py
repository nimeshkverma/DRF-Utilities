from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^customer/send_verification_email/$', views.EmailVerificationCreate.as_view(),
        name='send_verification_email'),
    url(r'^customer/verify_email/(?P<encoded_data>[\w:_-]+)$',
        views.EmailVerificationDetail.as_view(), name='verify_email'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
