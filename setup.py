from distutils.core import setup

from cross_origin import __version__


version_str = ".".join(str(n) for n in __version__)


setup(
    name = "django-cross-origin",
    version = version_str,
    license = "BSD",
    description = "A Django app enabling cross-origin resource sharing in views.",
    author = "Dave Hall",
    author_email = "dave@etianen.com",
    url = "http://github.com/mohawkhq/django-cross-origin",
    packages = [
        "cross_origin",
    ],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
)
