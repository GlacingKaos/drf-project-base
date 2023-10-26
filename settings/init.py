import os

import environ

from .base import *  # noqa: F401

ROOT_DIR = environ.Path(__file__) - 2  # (/a/b/myfile.py - 2 = /a/)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
APPS_DIR = ROOT_DIR.path("apps")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

ENV_NAME = env("ENV_NAME", default="CHANGEME!!!")

if ENV_NAME == "production":
    from .production import *  # noqa: F401
elif ENV_NAME == "staging":
    from .staging import *  # noqa: F401
else:
    from .local import *  # noqa: F401
