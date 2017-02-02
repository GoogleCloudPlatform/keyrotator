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
"""keyrotator: GCP access key management utility.

Usage:
  keyrotator cleanup (--project-id <PROJECTID>) (--iam-account <ACCOUNT>)
    (--key-max-age <DAYS>)
  keyrotator create (--project-id <PROJECTID>) (--iam-account <ACCOUNT>)
    [--key-type <TYPE>] [--key-algorithm <AlGORITHM>] [--output-file <FILE>]
  keyrotator delete (--project-id <PROJECTID>) (--iam-account <ACCOUNT>)
    (--key-id <KEYID>)
  keyrotator list (--project-id <PROJECTID>) (--iam-account <ACCOUNT>)
  keyrotator (-h | --help)
  keyrotator (--version)

Options:
  --project-id PROJECTID        The project id of the key.
  --iam-account ACCOUNT         The IAM service account id.
  --key-max-age DAYS            An integer in the unit of days for which to
                                delete a key if it is greather than.
  --key-algorithm ALGORITHM     The algorithm of the key to create.
  --key-id KEYID                The id of the key to delete.
  --key-type TYPE               The type of private key to create.
  --output-file FILE            The file name of the newly created key.
  -h --help                     Display the usage.
  --version                     Show the version number.

"""

import logging
import sys
import time

from cleanup import CleanupCommand
from create import CreateCommand
from delete import DeleteCommand
from docopt_dispatch import dispatch
from list import ListCommand
from version import __version__


def main():
  log_filename = "keyrotator" + time.strftime("-%Y-%m-%d-%H%M") + ".log"
  logging.basicConfig(filename=log_filename, level=logging.INFO)
  logging.getLogger("").addHandler(logging.StreamHandler())
  logging.info("Logging established in %s.", log_filename)

  dispatch(__doc__, version=__version__)


@dispatch.on("cleanup")
def Cleanup(project_id, iam_account, key_max_age, **kwargs):
  """For the specifed project, account, and key age delete invalid keys.

  1) List keys for the given GCP Project ID and Service Account.
  2) Determine Key IDs that meet the key_max_age requirement.
  3) Perform a delete for the matching Key IDs.

  Args:
    project_id: The project_id for which to create the key.
    iam_account: The IAM account for which to create the key.
    key_max_age: A positive integer (in days) for which to find keys to delete.
    **kwargs: Additional parameters for the list command.
  """
  _ = kwargs
  command = CleanupCommand()
  sys.exit(command.run(project_id, iam_account, key_max_age))


@dispatch.on("create")
def Create(project_id, iam_account, **kwargs):
  """Creates a new key for an account with the specified key type and algorithm.

  If no key type or key algorithm is provided, it will default the key type to
  TYPE_GOOGLE_CREDENTIALS_FILE format and the key algorithm to KEY_ALG_RSA_4096.
  The resulting key will be output to stdout by default.

  Args:
    project_id: The project_id for which to create the key.
    iam_account: The IAM account for which to create the key.
    **kwargs: Additional parameters for the create command.
  """
  command = CreateCommand()
  sys.exit(command.run(project_id, iam_account, key_type=kwargs["key_type"],
                       key_algorithm=kwargs["key_algorithm"],
                       output_file=kwargs["output_file"]))


@dispatch.on("delete")
def Delete(project_id, iam_account, key_id, **kwargs):
  """Deletes a specific key for an account.

  Args:
    project_id: The project_id for which to delete the key.
    iam_account: The IAM account for which to delete the key.
    key_id: The ID of the key to delete.
    **kwargs: Additional parameters for the delete command.
  """
  _ = kwargs
  command = DeleteCommand()
  sys.exit(command.run(project_id, iam_account, key_id))


@dispatch.on("list")
def List(project_id, iam_account, **kwargs):
  """List keys for service account.

  Args:
    project_id: The project_id for which to list keys.
    iam_account: The IAM account for which to list keys.
    **kwargs: Additional parameters for the list command.
  """
  _ = kwargs
  command = ListCommand()
  sys.exit(command.run(project_id, iam_account))


if __name__ == "__main__":
  main()
