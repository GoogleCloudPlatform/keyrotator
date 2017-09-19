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
"""Module to interact with Google Cloud Platform IAM."""

import logging
import re

from apiclient import discovery
from apiclient import errors
from oauth2client.client import GoogleCredentials
from retrying import retry

RETRY_MULTIPLIER_MS = 1000
RETRY_MAX_SEC = 10000


def _get_iam_service():
  """Get the IAM service.

  Returns:
    An apiclient service object.
  """
  credentials = GoogleCredentials.get_application_default()
  return discovery.build(
      serviceName="iam", version="v1", credentials=credentials)


def retry_if_500_error(exception):
  """Allow retry if we get a 500 error from IAM API."""
  logging.info("Received %s, retrying...", exception)
  return (isinstance(exception, errors.HttpError)
          and exception.resp.status >= 500
          and exception.resp.status < 600)


@retry(wait_exponential_multiplier=RETRY_MULTIPLIER_MS,
       stop_max_delay=RETRY_MAX_SEC,
       retry_on_exception=retry_if_500_error)
def list_keys(project_id, service_account_id):
  """List the keys for a service account.

  Args:
    project_id: String of a project id.  Should contain the specified service
        account.
    service_account_id: String of a service account id.  Should be in the
        specified project.

  Returns:
    Dict of a newly created instance of ServiceAccountKey.
  """
  full_name = "projects/{0}/serviceAccounts/{1}".format(project_id,
                                                        service_account_id)
  keys = _get_iam_service().projects().serviceAccounts().keys()
  request = keys.list(name=full_name, keyTypes="USER_MANAGED")
  return request.execute()


@retry(wait_exponential_multiplier=RETRY_MULTIPLIER_MS,
       stop_max_delay=RETRY_MAX_SEC,
       retry_on_exception=retry_if_500_error)
def create_key(project_id, service_account_id, key_type, key_algorithm):
  """Create a key for a service account.

  Args:
    project_id: String of a project id.  Should contain the specified service
        account.
    service_account_id: String of a service account id.  Should be in the
        specified project.
    key_type: String of a type of key to create.
        https://goo.gl/i4iLsi
    key_algorithm: String of the key's algorithm strength.
        https://goo.gl/zCchyg

  Returns:
    Dict of a newly created instance of ServiceAccountKey.
    Base64 decode "privateKeyData" to obtain credentials JSON.
  """
  full_name = "projects/{0}/serviceAccounts/{1}".format(project_id,
                                                        service_account_id)
  body = {"privateKeyType": key_type, "keyAlgorithm": key_algorithm}
  keys = _get_iam_service().projects().serviceAccounts().keys()
  request = keys.create(name=full_name, body=body)
  return request.execute()


@retry(wait_exponential_multiplier=RETRY_MULTIPLIER_MS,
       stop_max_delay=RETRY_MAX_SEC,
       retry_on_exception=retry_if_500_error)
def delete_key(project_id, service_account_id, key_id):
  """Delete a key from a service account.

  Args:
    project_id: String of a project id.  Should contain the specified service
        account.
    service_account_id: String of a service account id.  Should be in the
        specified project.
    key_id: String of the key id.  Should belong to the specified service
        account.

  Returns:
    Dict.  If successful, the dict will be empty.
  """
  if not re.match("projects/(.*)/serviceAccounts/(.*)/keys/(.*)$", key_id):
    logging.debug("Key id %s is not properly formatted.", key_id)
    key_id = "projects/{0}/serviceAccounts/{1}/keys/{2}".format(
        project_id, service_account_id, key_id)
  keys = _get_iam_service().projects().serviceAccounts().keys()
  request = keys.delete(name=key_id)
  return request.execute()

