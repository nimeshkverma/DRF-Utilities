from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^customer/social_login/$',
        views.SocialLogin.as_view(), name='SocialLogin'),
    url(r'^customer/(?P<pk>[0-9]+)/social_logout/$',
        views.SocialLogout.as_view(), name='SocialLogout'),
    url(r'^customer/linkedin_auth$',
        views.LinkedinAuth.as_view(), name='LinkedinAuth'),
    url(r'^customer/(?P<customer_id>[0-9]+)/social_profiles/$',
        views.SocialProfiles.as_view(), name='SocialProfiles'),
    url(r'^admin/(?P<user_name>[\w\-]+)/customer/session_data/$',
        views.SessionDataList.as_view()),
    url(r'^admin/(?P<user_name>[\w\-]+)/customer/(?P<pk>[0-9]+)/session_data/$',
        views.SessionDataDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
