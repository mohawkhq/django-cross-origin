from django.conf.urls import url, patterns
from django.views import generic
from django.http import HttpResponse
from django.test import TestCase
from django.test.utils import override_settings

from cross_origin.views import AccessControlMixin, ACCESS_CONTROL_ALLOW_ORIGIN_ALL


class TestCrossOriginView(AccessControlMixin, generic.View):

    def get(self, request):
        return HttpResponse("OK")


FOO_DOT_COM = "http://www.foo.com"
BAR_DOT_COM = "http://www.bar.com"


urlpatterns = patterns("",
    url(r'^$', TestCrossOriginView.as_view()),
    url(r'^restricted/$', TestCrossOriginView.as_view(access_control_allow_origin=(
        FOO_DOT_COM,
        BAR_DOT_COM,
    ))),
)


@override_settings(ROOT_URLCONF="cross_origin.tests")
class CrossOriginViewTest(TestCase):

    def assertCrossOriginResponse(self, response, allow_origin=ACCESS_CONTROL_ALLOW_ORIGIN_ALL):
        self.assertEqual(response["Access-Control-Max-Age"], str(AccessControlMixin.access_control_max_age))
        self.assertEqual(response["Access-Control-Allow-Credentials"], str(AccessControlMixin.access_control_allow_credentials).lower())
        self.assertEqual(response["Access-Control-Allow-Origin"], allow_origin)
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

    def testCrossOriginRestictedGet(self):
        # Test a request to FOO_DOT_COM.
        response = self.client.get("/restricted/",
            HTTP_ORIGIN = FOO_DOT_COM,
        )
        self.assertEqual(response.content, "OK")
        self.assertCrossOriginResponse(response, FOO_DOT_COM)
        # Test a request to BAR_DOT_COM.
        response = self.client.get("/restricted/",
            HTTP_ORIGIN = BAR_DOT_COM,
        )
        self.assertEqual(response.content, "OK")
        self.assertCrossOriginResponse(response, BAR_DOT_COM)

    def testCrossOriginRestictedGetFailing(self):
        # Test a request to somewhere that's not allowed.
        response = self.client.get("/restricted/",
            HTTP_ORIGIN = "http://www.example.com/",
        )
        self.assertEqual(response.content, "OK")
        self.assertCrossOriginResponse(response, FOO_DOT_COM)
