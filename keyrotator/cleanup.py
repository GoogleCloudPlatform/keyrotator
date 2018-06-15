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
"""keyrotator Cleanup command."""

from datetime import datetime
from datetime import timedelta
import logging

from dateutil import parser
from delete import DeleteCommand
from list import ListCommand
import pytz


class CleanupCommand(object):
  """Implementation of the keyrotator cleanup command."""

  def run(self, project_id, iam_account, key_max_age):
    """Runs the list and delete commands for keyrotator.

    Args:
      project_id: The project_id for which to create the key.
      iam_account: The IAM account for which to create the key.
      key_max_age: An integer in units of days for which to find keys to delete.

    Returns:
      An integer indicating status.
    """
    current_keys = ListCommand().run(
        project_id, iam_account, return_results=True)

    signed_key_max_age = abs(int(key_max_age))
    current_datetime = datetime.now(pytz.utc)

    invalid_keys = []

    for key in current_keys:
      try:
        key_creation_time = parser.parse(key["validAfterTime"])
      except ValueError as e:
        logging.error("Ooops, unable to convert creation time: %s", e)

      diff_time = current_datetime - key_creation_time

      if diff_time.days > signed_key_max_age:
        logging.info("Found invalid key %s created %s", key["name"],
                     key_creation_time)
        invalid_keys.append(key)

    for key in invalid_keys:
      DeleteCommand().run(project_id, iam_account, key["name"])

    if not invalid_keys:
      logging.info("No keys to cleanup.")

    return 0
