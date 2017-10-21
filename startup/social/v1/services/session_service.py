import json

from django.utils.crypto import get_random_string
from copy import deepcopy

from social.models import Login
from customer.models import Customer
from social_service import SocialProfile
from social import models


def get_opposite_platform(platform):
    platform_opposites = {
        'facebook': 'google',
        'google': 'facebook'
    }
    return platform_opposites.get(platform)


def generate_session_token(customer_id):
    return 'startup_name_token_' + str(customer_id) + '_' + get_random_string(length=32)


def session_success_data(login_object):
    return {
        'session_token': login_object.session_token,
        'customer_id': login_object.customer_id
    }


def email_related_sessions(email_id):
    sessions = Login.email_related_logins(email_id)
    platform_sessions_data = {
        'facebook': {
            'customer_record': False,
            'session_token': '',
            'active': False,
            'object': None
        },
        'google': {
            'customer_record': False,
            'session_token': '',
            'active': False,
            'object': None
        }
    }
    if sessions:
        for session in sessions:
            platform_sessions_data[session.platform] = {
                'customer_record': True,
                'session_token': session.session_token,
                'active': session.is_active,
                'object': session
            }
    return platform_sessions_data


def create_new_session(session_input, social_profile):
    new_customer = Customer.objects.create()
    session_object_dict = {
        'platform_token': session_input['platform_token'],
        'source': session_input['source'],
        'platform': session_input['platform'],
        'customer': new_customer,
        'social_data': json.dumps(social_profile.data),
        'email_id': social_profile.email_id,
        'session_token': generate_session_token(new_customer.customer_id),
        'imei': session_input['imei'],
        'app_registration_id': session_input.get('app_registration_id'),
    }
    new_session = Login.objects.create(**session_object_dict)
    return session_success_data(new_session)


def update_session(session_pk, session_data):
    session_data['social_data'] = "abc"
    Login.objects.filter(pk=session_pk).update(**session_data)
    session_obj = Login.objects.get(pk=session_pk)
    return session_success_data(session_obj)


def create_session_from_obj(session_obj, session_input, social_profile, new_session_token=False):
    session_obj.id = None
    session_obj.platform_token = session_input['platform_token']
    session_obj.platform = session_input['platform']
    session_obj.social_data = json.dumps(social_profile.data)
    session_obj.imei = session_input['imei']
    session_obj.app_registration_id = session_input.get('app_registration_id')
    if new_session_token:
        session_obj.session_token = generate_session_token(
            session_obj.customer_id)
    session_obj.save()
    return session_success_data(session_obj)


def get_or_create_sessions(session_input):
    platform = session_input['platform']
    platform_token = session_input['platform_token']
    source = session_input['source']
    imei = session_input['imei']
    app_registration_id = session_input.get('app_registration_id')
    social_profile = SocialProfile(platform, platform_token)
    email_sessions = email_related_sessions(social_profile.email_id)
    opposite_platform = get_opposite_platform(platform)
    session_response = None
    if not (email_sessions['facebook']['customer_record'] or email_sessions['google']['customer_record']):
        # CASE: First Time user with no record in database
        # ACTION: Create new session and return new session_token and
        # customer_id
        session_response = create_new_session(session_input, social_profile)
    else:
        if email_sessions[platform]['customer_record']:
            if email_sessions[platform]['active']:
                # CASE: DB has record of this Customer and his Session is Active
                # ACTION: Update the Session with the new platform token and
                # updated time and return old session_token and customer_id
                session_data = {
                    'platform_token': platform_token,
                    'social_data': json.dumps(social_profile.data),
                    'imei': imei,
                    'app_registration_id': app_registration_id,
                    'deleted_at': None,
                }
                session_response = update_session(
                    email_sessions[platform]['object'].id, session_data)

            else:
                if email_sessions[opposite_platform]['active']:
                    # CASE: DB has record of this Customer and but his Session is InActive and Opposite Session Active
                    # ACTION: Activate this session by the opposite platform
                    # session_token, put this platform token and return old
                    # session_token and customer
                    session_data = {
                        'platform_token': platform_token,
                        'social_data': json.dumps(social_profile.data),
                        'session_token': email_sessions[opposite_platform]['object'].session_token,
                        'imei': imei,
                        'app_registration_id': app_registration_id,
                        'is_active': True,
                        'deleted_at': None,
                    }
                    session_response = update_session(
                        email_sessions[platform]['object'].id, session_data)
                else:
                    if email_sessions[opposite_platform]['customer_record']:
                        # CASE: DB has record of this Customer and but his Session is InActive and Opposite Session is In Active
                        # ACTION: Activate this session by the new session
                        # token and return session_token and customer_id
                        session_data = {
                            'platform_token': platform_token,
                            'social_data': json.dumps(social_profile.data),
                            'session_token': generate_session_token(email_sessions[platform]['object'].customer_id),
                            'imei': imei,
                            'app_registration_id': app_registration_id,
                            'is_active': True,
                            'deleted_at': None,
                        }
                        session_response = update_session(
                            email_sessions[platform]['object'].id, session_data)
                    else:
                        # CASE: DB has record of this Customer and but his Session is InActive and Opposite Session has no Record
                        # ACTION: Activate this session by the new session
                        # token and return session_token and customer_id
                        session_data = {
                            'platform_token': platform_token,
                            'social_data': json.dumps(social_profile.data),
                            'session_token': generate_session_token(email_sessions[platform]['object'].customer_id),
                            'imei': imei,
                            'app_registration_id': app_registration_id,
                            'is_active': True,
                            'deleted_at': None,

                        }
                        session_response = update_session(
                            email_sessions[platform]['object'].id, session_data)
        else:
            if email_sessions[opposite_platform]['customer_record']:
                if email_sessions[opposite_platform]['active']:
                    # CASE: DB has a record of this Customer, but his platform session record is not there and his other platform is active
                    # ACTION: Copy the Session with the other platform
                    # session_token and cust_id and return the session token
                    # and cust_id
                    session_response = create_session_from_obj(email_sessions[opposite_platform][
                                                               'object'], session_input, social_profile)
                else:
                    # CASE: DB has record of this Customer, this platform session record is not there  and his other platform session Inactive
                    # ACTION: Create a the Session and copy the cust_id and
                    # return the session_token and cust_id
                    session_response = create_session_from_obj(email_sessions[opposite_platform][
                                                               'object'], session_input, social_profile, True)
            else:
                pass
                # Not Possible
    model_data = deepcopy(social_profile.model_data)
    model_data.update({'customer_id': session_response['customer_id']})
    upsert_social_profile(model_data)
    return session_response


def upsert_social_profile(model_data):
    social_profile_objects = models.SocialProfile.objects.filter(customer_id=model_data[
                                                                 'customer_id'], email_id=model_data['email_id'], platform=model_data['platform'])
    if social_profile_objects:
        model_filter_data = dict()
        for model_key in ['customer_id', 'email_id', 'platform']:
            model_filter_data[model_key] = model_data.pop(model_key)
        models.SocialProfile.objects.filter(customer_id=model_filter_data['customer_id'], email_id=model_filter_data[
                                            'email_id'], platform=model_filter_data['platform']).update(**model_data)
    else:
        models.SocialProfile.objects.create(**model_data)
