"""View mixins provided by django-cross-origin."""

from django.http import HttpResponse


ACCESS_CONTROL_ALLOW_ORIGIN_ALL = "*"


class AccessControlMixin(object):

    access_control_allow_origin = ()

    def get_access_control_allow_origin(self):
        """
        An container of origin domains allowed to access this resource.

        An empty container implies that all domains may access this resource.
        """
        return self.access_control_allow_origin

    access_control_allow_credentials = False

    def get_access_control_allow_credentials(self):
        return self.access_control_allow_credentials

    access_control_max_age = 60 * 30  # 30 minutes.

    def get_access_control_max_age(self):
        return self.access_control_max_age

    access_control_allow_methods = None

    def get_access_control_allow_methods(self):
        if self.access_control_allow_methods is None:
            return [
                method
                for method
                in self.http_method_names
                if hasattr(self, method)
            ]
        return self.access_control_allow_methods()

    access_control_allow_headers = ("origin", "content-type", "accept", "authorization")

    def get_access_control_allow_headers(self):
        return self.access_control_allow_headers

    def options(self, request, *args, **kwargs):
        response = HttpResponse()
        response["Access-Control-Allow-Methods"] = ", ".join(method.upper() for method in self.get_access_control_allow_methods())
        return response

    def dispatch(self, request, *args, **kwargs):
        response = super(AccessControlMixin, self).dispatch(request, *args, **kwargs)
        # Write the access control allow origin header.
        request_origin_header = request.META.get("HTTP_ORIGIN", "")
        access_control_allow_origin = self.get_access_control_allow_origin()
        if not access_control_allow_origin:
            # A wildcard allowed origin was used.
            access_control_allow_origin_header = ACCESS_CONTROL_ALLOW_ORIGIN_ALL
        elif request_origin_header.lower() in [n.lower() for n in access_control_allow_origin]:
            # A matched domain was used.
            access_control_allow_origin_header = request_origin_header
        else:
            # No matched domain.
            access_control_allow_origin_header = access_control_allow_origin[0]
        # Add the headers.
        response["Access-Control-Allow-Origin"] = access_control_allow_origin_header
        response["Access-Control-Allow-Credentials"] = str(self.get_access_control_allow_credentials()).lower()
        response["Access-Control-Max-Age"] = str(self.get_access_control_max_age())
        response["Access-Control-Allow-Headers"] = ", ".join(self.get_access_control_allow_headers())
        # Dispatch the response.
        return response
