from __future__ import unicode_literals
import itertools
from collections import OrderedDict, namedtuple
from django.conf.urls import url
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import NoReverseMatch
from rest_framework import exceptions, renderers, views
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.schemas import SchemaGenerator
from rest_framework.settings import api_settings
from rest_framework.urlpatterns import format_suffix_patterns


class HybridRouter(DefaultRouter):
    def __init__(self, *args, **kwargs):
        super(HybridRouter, self).__init__(*args, **kwargs)
        self._view_urls = {}
        self._include_urls = {}

    def register_view(self, url):
        self._view_urls[url.name] = url

    def remove_view(self, name):
        del self._view_urls[name]

    def register_include(self, url):
        self._view_urls[url.namespace] = url

    @property
    def view_urls(self):
        ret = {}
        ret.update(self._view_urls)
        return ret

    def get_urls(self):
        urls = super(HybridRouter, self).get_urls()
        for api_view_key in self._view_urls.keys():
            urls.append(self._view_urls[api_view_key])
        return urls

    def get_api_root_view(self, api_urls=None):
        # Copy the following block from Default Router
        api_root_dict = OrderedDict()
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)

        view_urls = self._view_urls
        include_urls = self._include_urls

        class APIRoot(views.APIView):
            """
            The Presnt  browsable API.

            ### Authentication

            Our API uses [token authentication][5].

            For clients to authenticate, the token key should be included in the
            Authorization HTTP header. The key should be prefixed by the string literal
            "Token", with whitespace separating the two strings. For example:

                Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

            To get an authentication token you will first have to login using the
            'rest_login' url at `/auth/login`.

            [5]: http://www.django-rest-framework.org/api-guide/authentication/
            """
            _ignore_model_permissions = True

            def parse_view_url(self, view_url, request):
                ret = {}
                try:
                    url_name = view_url.name
                    if url_name:
                        ret[url_name] = reverse(url_name, request=request)
                except AttributeError:
                    namespace = view_url.namespace
                    for url in view_url.url_patterns:
                        try:
                            ret.update(self.parse_view_url(url, request))
                        except NoReverseMatch:
                            return ret

                return ret

            def get(self, request, *args, **kwargs):
                ret = OrderedDict()
                namespace = request.resolver_match.namespace
                for key, url_name in api_root_dict.items():
                    if namespace:
                        url_name = namespace + ':' + url_name
                    try:
                        ret[key] = reverse(
                            url_name,
                            args=args,
                            kwargs=kwargs,
                            request=request,
                            format=kwargs.get('format', None)
                        )
                    except NoReverseMatch:
                        # Don't bail out if eg. no list routes exist, only detail routes.
                        continue

                # In addition to what had been added, now add the APIView urls
                for key in view_urls.keys():
                    ret.update(self.parse_view_url(view_urls[key], request))

                return Response(ret)

        return APIRoot.as_view()
