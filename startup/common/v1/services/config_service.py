from django.conf import settings


class Config(object):

    def __init__(self):
        self.data = self.__get_data()

    def __get_base_url(self):
        return settings.BASE_URL

    def __get_versions(self):
        return settings.VERSIONS

    def __get_versioned_base_url(self):
        return settings.VERSIONED_BASE_URL

    def __get_data(self):
        config_data = {

            'base_url': self.__get_base_url(),
            'versions': self.__get_versions(),
            'versioned_base_url': self.__get_versioned_base_url(),
        }

        return config_data
