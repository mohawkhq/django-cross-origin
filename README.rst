django-cross-origin
===================

**django-cross-origin** is a Django app enabling cross-origin resource sharing in views.


Features
--------

- Enable CORS on Django class-based generic views with a simple mixin.
- Full customization of all CORS headers via accessor override.


Installation
------------

1. Checkout the latest django-cross-origin release and copy or symlink the
   ``cross_origin`` directory into your ``PYTHONPATH``.  If using pip, run 
   ``pip install django-cross-origin``.
2. Add ``'cross_origin'`` to your ``INSTALLED_APPS`` setting.


Usage
-----

To enable CORS on a Django class-based view, simply mixin the `cross_origin.views.AccessControlMixin`
to your view:

::

    from django.views import generic
    from cross_origin.views import AccessControlMixin

    class YourView(AccessControlMixin, generic.TemplateView):

        """Your view code here!"""


All CORS response headers can be customized by overriding accessor methods on your view. For a complete
list of available accessors, see the source code for `AccessControlMixin <https://github.com/mohawkhq/django-cross-origin/blob/master/cross_origin/views.py>`_.


More information
----------------

The django-cross-origin project was developed at `Mohawk <http://www.mohawkhq.com/>`_, and
is released as Open Source under the MIT license.

You can get the code from the `django-cross-origin project site <http://github.com/mohawkhq/django-cross-origin>`_.


Contributors
------------

The following people were involved in the development of this project.

- Dave Hall - `Blog <http://blog.etianen.com/>`_ | `GitHub <http://github.com/etianen>`_ | `Twitter <http://twitter.com/etianen>`_ | `Google Profile <http://www.google.com/profiles/david.etianen>`_