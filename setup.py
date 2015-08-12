from __future__ import with_statement
import sys
from setuptools import setup, find_packages

__version__ = None
with open('textmagic/version.py') as f:
    exec (f.read())

REQUIRES = ['httplib2', 'six']

if sys.version_info < (2, 6):
    REQUIRES.append('simplejson')
if sys.version_info >= (3, 0):
    REQUIRES.append('pysocks')

setup(
    name="textmagic",
    version=__version__,
    description="TextMagic APIv2 client",
    author="Textmagic",
    author_email="support@textmagic.com",
    url="http://code.google.com/p/textmagic-sms-api-python/",
    keywords=["textmagic"],
    install_requires=REQUIRES,
    extras_require={
        ':python_version=="3.2"': ['pysocks'],
        ':python_version=="3.3"': ['pysocks'],
        ':python_version=="3.4"': ['pysocks'],
    },
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        'Intended Audience :: Information Technology',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Telephony",
        ],
)
