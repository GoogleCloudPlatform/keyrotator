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
"""keyrotator List command."""

import logging
import re

import iam_service


class ListCommand(object):
  """Implementation of the keyrotator list command."""
  keyname_pattern = re.compile("keys/(.*)$")

  def run(self, project_id, iam_account, return_results=False):
    """Runs the list_keys command for keyrotator.

    Args:
      project_id: The project_id for which to create the key.
      iam_account: The IAM account for which to create the key.
      return_results: Boolean to return results or exit code.

    Returns:
      An integer indicating status or a dictionary containing
      key data given an input parameters.
    """
    response = iam_service.list_keys(project_id, iam_account)

    if response and "keys" in response:
      logging.info("Current key listing:")
      for key in response["keys"]:
        key_path = self.keyname_pattern.search(key["name"])
        logging.info("Key: %s\n\tCreated: %s\n\tExpires: %s",
                     key_path.group(1), key["validAfterTime"],
                     key["validBeforeTime"])

      if return_results:
        return response["keys"]

    return 0
