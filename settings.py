import os
from django.conf import settings
from django.apps import apps

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'oracle.geotech.com.co/geotech',
        'USER': 'skytech',
        'PASSWORD': 'skytech'
    }
}

INSTALLED_APPS = (
    'db',
)
SECRET_KEY = '6few3nci_q_o@l1dlbk81%wcxe!*6r29yu629&d97!hiqat9fa'
