from copy import deepcopy
from . import serializers
from social import models


def get_linkedin_profile(customer_id):
    linkedin_profile = {}
    linkedin_objects = models.LinkedinProfile.objects.filter(
        customer_id=customer_id)
    if linkedin_objects:
        serializer = serializers.LinkedinAuthSerializer(linkedin_objects[0])
        linkedin_profile = deepcopy(serializer.data)
        linkedin_profile['customer_id'] = customer_id
    return linkedin_profile


def get_social_profiles(customer_id):
    social_profiles = {
        'google': {},
        'facebook': {},
    }
    social_objects = models.SocialProfile.objects.filter(
        customer_id=customer_id)
    serializer = serializers.SocialProfileSerializer(social_objects, many=True)
    for social_profile in serializer.data:
        social_profiles[social_profile['platform']] = social_profile
    return social_profiles


def get_customer_profiles(customer_id):
    customer_profiles = {
        'linkedin': get_linkedin_profile(customer_id)
    }
    customer_profiles.update(get_social_profiles(customer_id))
    return customer_profiles
