# -*- coding: utf-8 -*-
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""keyrotator setup file."""

from keyrotator.version import __version__
from setuptools import find_packages
from setuptools import setup

setup(
    name="keyrotator",
    version=__version__,
    url="http://github.com/GoogleCloudPlatform/keyrotator",
    license="Apache 2.0",
    author="Google, Inc.",
    author_email="cloud-service-account-key-utility@google.com",
    description=("Command line utility for managing Google Cloud"
                 "service account access keys."),
    classifiers=[
        # Classifiers to categorize the project. Full listing
        # of available options at:
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License"
    ],
    keywords="gcp google cloud key management",
    packages=find_packages(),
    install_requires=["docopt",
                      "docopt-dispatch",
                      "google-api-python-client",
                      "pytz",
                      "python-dateutil",
                      "retrying",],
    entry_points={
        "console_scripts": ["keyrotator = keyrotator.keyrotator:main"]
    })
