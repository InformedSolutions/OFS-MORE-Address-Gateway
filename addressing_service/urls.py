from django.conf import settings
from django.conf.urls import url
import re
from application.views import postcode_request, change_api_key

urlpatterns = [
    url(r'^api/v1/addresses/api-key/$', change_api_key),
    url(r'^api/v1/addresses/(?P<postcode>[\w\ ]+)/$', postcode_request),
]

if settings.URL_PREFIX:
    prefixed_url_pattern = []
    for pat in urlpatterns:
        pat.regex = re.compile(r"^%s/%s" % (settings.URL_PREFIX[1:], pat.regex.pattern[1:]))
        prefixed_url_pattern.append(pat)
    urlpatterns = prefixed_url_pattern
