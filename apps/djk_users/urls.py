from django.conf import settings
from django.urls import include, re_path
from django_jinja_knockout.urls import UrlPath

from .views import UserChangeView, main_page

# from django.contrib import admin


urlpatterns_djk_users = [
    re_path(r"^$", main_page, name="main_page", kwargs={"view_title": "Main page", "allow_anonymous": True}),
    UrlPath(UserChangeView)("user_change"),
]

# Allauth views.
if settings.ALLAUTH_DJK_URLS:
    # More pretty-looking bootstrap forms but possibly are not compatible with arbitrary allauth version:
    urlpatterns_djk_users.append(re_path(r"^accounts/", include("django_jinja_knockout._allauth.urls")))
else:
    # Standard allauth DTL templates working with Jinja2 templates via {% load jinja %} template tag library.
    urlpatterns_djk_users.append(re_path(r"^accounts/", include("allauth.urls")))

js_info_dict = {
    "domain": "djangojs",
    "packages": [
        "django_jinja_knockout",
        # "djk_sample",
    ],
}

try:
    from django.views.i18n import JavaScriptCatalog

    urlpatterns_djk_users.append(
        re_path(r"^jsi18n/$", JavaScriptCatalog.as_view(**js_info_dict), name="javascript-catalog"),
    )
except ImportError:
    from django.views.i18n import javascript_catalog

    urlpatterns_djk_users.append(re_path(r"^jsi18n/$", javascript_catalog, js_info_dict, name="javascript-catalog"))

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns_djk_users += staticfiles_urlpatterns()
