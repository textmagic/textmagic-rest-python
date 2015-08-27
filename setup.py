from __future__ import with_statement
import sys
from setuptools import setup, find_packages

__version__ = None
with open('textmagic/version.py') as f:
    exec (f.read())

REQUIRES = ['httplib2', 'six']

if sys.version_info < (2, 6):
    REQUIRES.append('simplejson')

setup(
    name="textmagic",
    version=__version__,
    description="TextMagic APIv2 client",
    author="Textmagic",
    author_email="support@textmagic.com",
    url="https://github.com/textmagic/textmagic-rest-python",
    keywords=["textmagic"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        'Intended Audience :: Information Technology',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Telephony",
        ],
)
