#!/usr/bin/env python3

# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################
r"""Utility that replaces http_archive with local_repository in WORKSPACE files.

Usage:
  ./kokoro/testutils/replace_http_archive_with_local_repository.py \
    -f <workspace directory> \
    -t <tink local base path>

For examples:
  ./kokoro/testutils/replace_http_archive_with_local_repository.py \
    -f "cc/WORKSPACE" \
    -t "../../tink"
"""

import argparse
import textwrap

_TINK_MONOREPO_GITHUB_ARCHIVE_URL = 'https://github.com/google/tink/archive/master.zip'
_TINK_POLIREPO_GITHUB_ORG_URL = 'https://github.com/tink-crypto'


def _replace_http_archive_with_local_repository(workspace_content: str,
                                                tink_base_path: str) -> None:
  """Replaces http_archive with local_repository in workspace_content.

  Args:
    workspace_content: Content of the WORKSPACE file to modify.
    tink_base_path: Path to the local Tink folder.

  Returns:
    The modified WORKSPACE file content.
  """
  # Remove loading of http_archive.
  http_archive_load = textwrap.dedent("""\
      load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
      """)
  workspace_content = workspace_content.replace(http_archive_load, '')

  # TODO(b/234429843): Remove this once we migrate tink-examples to using
  # tink-py as a dependency instead of tink/python.
  # Tink C++.
  tink_cc_before = textwrap.dedent(f"""\
      http_archive(
          name = "tink_cc",
          urls = ["{_TINK_MONOREPO_GITHUB_ARCHIVE_URL}"],
          strip_prefix = "tink-master/cc",
      )""")
  tink_cc_after = textwrap.dedent(f"""\
      local_repository(
          name = "tink_cc",
          path = "{tink_base_path}/cc",
      )""")
  workspace_content = workspace_content.replace(tink_cc_before, tink_cc_after)

  # Tink C++ AWS-KMS.
  tink_cc_awskms_before = textwrap.dedent(f"""\
      http_archive(
          name = "tink_cc_awskms",
          urls = ["{_TINK_MONOREPO_GITHUB_ARCHIVE_URL}"],
          strip_prefix = "tink-master/cc/integration/awskms",
      )""")
  tink_cc_awskms_after = textwrap.dedent(f"""\
      local_repository(
          name = "tink_cc_awskms",
          path = "{tink_base_path}/cc/integration/awskms",
      )""")
  workspace_content = workspace_content.replace(tink_cc_awskms_before,
                                                tink_cc_awskms_after)

  # Tink C++ Cloud KMS.
  tink_cc_gcpkms_before = textwrap.dedent(f"""\
      http_archive(
          name = "tink_cc_gcpkms",
          urls = ["{_TINK_MONOREPO_GITHUB_ARCHIVE_URL}"],
          strip_prefix = "tink-master/cc/integration/gcpkms",
      )""")
  tink_cc_gcpkms_after = textwrap.dedent(f"""\
      local_repository(
          name = "tink_cc_gcpkms",
          path = "{tink_base_path}/cc/integration/gcpkms",
      )""")
  workspace_content = workspace_content.replace(tink_cc_gcpkms_before,
                                                tink_cc_gcpkms_after)

  # Tink C++.
  tink_cc_before = textwrap.dedent(f"""\
      http_archive(
          name = "tink_cc",
          urls = ["{_TINK_POLIREPO_GITHUB_ORG_URL}/tink-cc/archive/master.zip"],
          strip_prefix = "tink-cc-master",
      )""")
  tink_cc_after = textwrap.dedent(f"""\
      local_repository(
          name = "tink_cc",
          path = "{tink_base_path}/tink_cc",
      )""")
  workspace_content = workspace_content.replace(tink_cc_before, tink_cc_after)

  # Tink C++ AWS-KMS.
  tink_cc_awskms_before = textwrap.dedent(f"""\
      http_archive(
          name = "tink_cc_awskms",
          urls = ["{_TINK_POLIREPO_GITHUB_ORG_URL}/tink-cc-awskms/archive/main.zip"],
          strip_prefix = "tink-cc-awskms-main",
      )""")
  tink_cc_awskms_after = textwrap.dedent(f"""\
      local_repository(
          name = "tink_cc_awskms",
          path = "{tink_base_path}/tink_cc_awskms",
      )""")
  workspace_content = workspace_content.replace(tink_cc_awskms_before,
                                                tink_cc_awskms_after)

  # Tink C++ Google Cloud KMS.
  tink_cc_gcpkms_before = textwrap.dedent(f"""\
      http_archive(
          name = "tink_cc_gcpkms",
          urls = ["{_TINK_POLIREPO_GITHUB_ORG_URL}/tink-cc-gcpkms/archive/main.zip"],
          strip_prefix = "tink-cc-gcpkms-main",
      )""")
  tink_cc_gcpkms_after = textwrap.dedent(f"""\
      local_repository(
          name = "tink_cc_gcpkms",
          path = "{tink_base_path}/tink_cc_gcpkms",
      )""")
  workspace_content = workspace_content.replace(tink_cc_gcpkms_before,
                                                tink_cc_gcpkms_after)

  # Tink Java.
  tink_java_before = textwrap.dedent(f"""\
      http_archive(
          name = "tink_java",
          urls = ["{_TINK_POLIREPO_GITHUB_ORG_URL}/tink-java/archive/main.zip"],
          strip_prefix = "tink-java-main",
      )""")
  tink_java_after = textwrap.dedent(f"""\
      local_repository(
          name = "tink_java",
          path = "{tink_base_path}/tink_java",
      )""")
  workspace_content = workspace_content.replace(tink_java_before,
                                                tink_java_after)
  # Tink Java Google Cloud KMS.
  tink_java_gcpkms_before = textwrap.dedent(f"""\
      http_archive(
          name = "tink_java_gcpkms",
          urls = ["{_TINK_POLIREPO_GITHUB_ORG_URL}/tink-java-gcpkms/archive/main.zip"],
          strip_prefix = "tink-java-gcpkms-main",
      )""")
  tink_java_gcpkms_after = textwrap.dedent(f"""\
      local_repository(
          name = "tink_java_gcpkms",
          path = "{tink_base_path}/tink_java_gcpkms",
      )""")
  workspace_content = workspace_content.replace(tink_java_gcpkms_before,
                                                tink_java_gcpkms_after)
  # Tink Java AWS KMS.
  tink_java_awskms_before = textwrap.dedent(f"""\
      http_archive(
          name = "tink_java_awskms",
          urls = ["{_TINK_POLIREPO_GITHUB_ORG_URL}/tink-java-awskms/archive/main.zip"],
          strip_prefix = "tink-java-awskms-main",
      )""")
  tink_java_awskms_after = textwrap.dedent(f"""\
      local_repository(
          name = "tink_java_awskms",
          path = "{tink_base_path}/tink_java_awskms",
      )""")
  workspace_content = workspace_content.replace(tink_java_awskms_before,
                                                tink_java_awskms_after)

  # Tink Python.
  tink_python_before = textwrap.dedent(f"""\
      http_archive(
          name = "tink_py",
          urls = ["{_TINK_MONOREPO_GITHUB_ARCHIVE_URL}"],
          strip_prefix = "tink-master/python",
      )""")
  tink_python_after = textwrap.dedent(f"""\
      local_repository(
          name = "tink_py",
          path = "{tink_base_path}/python",
      )""")
  workspace_content = workspace_content.replace(tink_python_before,
                                                tink_python_after)

  return workspace_content


def main():
  parser = argparse.ArgumentParser(
      description='Replaces http_archive rules with local_repository rules')
  parser.add_argument('--workspace_file_path', '-f', required=True)
  parser.add_argument('--tink_base_path', '-t', required=True)
  args = parser.parse_args()

  with open(args.workspace_file_path, 'r') as workspace_file:
    content = workspace_file.read()
    content = _replace_http_archive_with_local_repository(
        content, args.tink_base_path)
  with open(args.workspace_file_path, 'w') as workspace_file:
    workspace_file.write(content)


if __name__ == '__main__':
  main()