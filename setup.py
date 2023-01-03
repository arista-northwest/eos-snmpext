# -*- coding: utf-8 -*-

# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

# import sys
import os
from setuptools import setup, find_packages

# if sys.version_info < (2, 7, 0):
#     raise NotImplementedError("Sorry, you need at least Python 2.6 to install.")
#
# sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from snmpext import __version__

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

from os.path import dirname, basename, isfile, join
import glob

def gen_entrypoints(dir="snmpext/extensions"):
    modules = glob.glob(join(dirname(__file__), dir, "*.py"))
    for m in [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]:
        yield "snmpext-%s = snmpext.entry:main" % m

setup(
    name = "snmpext",
    version = __version__,
    author = "Jesse Mather",
    author_email = "jmather@arista.com",
    description = "Collection of custom SNMP extensions",
    long_description = "", #read("README.md"),
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Network Engineers",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Environment :: Functional Testing Automation"
    ],
    packages = find_packages(exclude=['_clab']),

    url = "http://aristanetworks.com",
    license = "Proprietary",
    entry_points = {
        'console_scripts': [s for s in gen_entrypoints()]
    },
    options = {
        'bdist_rpm': {
            'post_install' : 'post_install.sh',
            'post_uninstall' : 'post_uninstall.sh'
        }
    },
)
