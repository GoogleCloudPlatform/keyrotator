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
"""keyrotator Create command."""

import json
import logging
import iam_service


DEFAULT_KEY_TYPE = "TYPE_GOOGLE_CREDENTIALS_FILE"
DEFAULT_KEY_ALGO = "KEY_ALG_RSA_2048"


class CreateCommand(object):
  """Implementation of the keyrotator create command."""

  def run(self, project_id, iam_account, key_type=DEFAULT_KEY_TYPE,
          key_algorithm=DEFAULT_KEY_ALGO, output_file=None):
    """Runs the create command for keyrotator."""
    response = iam_service.create_key(project_id, iam_account,
                                      key_type, key_algorithm)

    if output_file:
      self._write_key(path=output_file, payload=response)
    else:
      logging.info("Key successfully created.")
      logging.debug("Key details: %s",
                    json.dumps(response, sort_keys=True,
                               indent=4, separators=(",", ": ")))

    return 0

  def _write_key(self, path, payload):
    """Writes the key out to the filesystem."""
    with open(path, "w") as outfile:
      json.dump(payload, outfile)
