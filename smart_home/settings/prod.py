import os
from corsheaders.defaults import default_headers

from .base import *

DEBUG = False
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
SITE_DOMAIN = "https://halpiszony.dpdns.org"
FIRMWARE_DEVICE_ENDPOINT = SITE_DOMAIN + "/api/firmware/download/"

CORS_ALLOWED_ORIGINS = [
    "https://halpiszony.dpdns.org",
]
CSRF_TRUSTED_ORIGINS = [
    "https://halpiszony.dpdns.org",
]
ALLOWED_HOSTS = ["halpiszony.dpdns.org"]
CORS_ALLOW_CREDENTIALS = True
