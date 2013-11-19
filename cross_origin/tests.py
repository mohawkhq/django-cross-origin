from django.conf.urls import url, patterns
from django.views import generic
from django.http import HttpResponse
from django.test import TestCase
from django.test.utils import override_settings

from cross_origin.views import AccessControlMixin


class TestCrossOriginView(AccessControlMixin, generic.View):

    def get(self, request):
        return HttpResponse("OK")


urlpatterns = patterns("",
    url(r'^$', TestCrossOriginView.as_view()),
)


@override_settings(ROOT_URLCONF="cross_origin.tests")
class CrossOriginViewTest(TestCase):

    def assertCrossOriginResponse(self, response):
        self.assertEqual(response["Access-Control-Max-Age"], str(AccessControlMixin.access_control_max_age))
        self.assertEqual(response["Access-Control-Allow-Credentials"], str(AccessControlMixin.access_control_allow_credentials).lower())
        self.assertEqual(response["Access-Control-Allow-Origin"], "*")
        self.assertEqual(response["Access-Control-Allow-Headers"], ", ".join(AccessControlMixin.access_control_allow_headers))

    def testCrossOriginGetRequest(self):
        response = self.client.get("/")
        self.assertEqual(response.content, "OK")
        # Test the headers.
        self.assertCrossOriginResponse(response)
        self.assertEqual(response.get("Access-Control-Allow-Methods"), None)

    def testCrossOriginOptionsRequest(self):
        response = self.client.options("/")
        self.assertEqual(response.content, "")
        # Test the headers.
        self.assertCrossOriginResponse(response)
        self.assertEqual(response["Access-Control-Allow-Methods"], "GET, HEAD, OPTIONS")
