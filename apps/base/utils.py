# Standard Library
# import locale
import random
import string
from datetime import datetime

# Third party Imports
# from django.conf import settings
from django.utils import timezone

# try:
#     locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
# except locale.Error as e:
#     # Error: locale.Error: unsupported locale setting
#     print(f"ADVERTENCIA: {__file__}, linea {e.__traceback__.tb_lineno}: {e}")


DATETIME_DJK_FMT = "%d %B %Y %H:%M"
SHORT_DATETIME_DJK_FMT = "%d %b %Y %H:%M"
DATE_FORMAT = "%d/%m/%Y"
HOUR_FORMAT = "%H:%M"
DATETIME_BASE = "%Y-%m-%d %H:%M:%S"
ORIGINAL_DATETIME = "%Y-%m-%dT%H:%M:%S"


def get_format_date(value, datetime_format=SHORT_DATETIME_DJK_FMT, original_format="%Y-%m-%dT%H:%M:%S"):
    if isinstance(value, str):
        value = datetime.strptime(value, original_format)
    if isinstance(value, datetime):
        value = value.astimezone(timezone.get_current_timezone()).strftime(datetime_format)
    return value


def create_string_random(size=10):
    code = "".join(random.choices(string.ascii_uppercase + string.digits, k=size))
    return code
