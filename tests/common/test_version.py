# Copyright 2014 Microsoft Corporation
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
#
# Requires Python 2.4+ and Openssl 1.0+
#

from __future__ import print_function

import copy
import glob
import json
import mock
import os
import platform
import random
import subprocess
import sys
import tempfile
import textwrap
import zipfile

from tests.protocol.mockwiredata import *
from tests.tools import *

import azurelinuxagent.common.conf as conf
import azurelinuxagent.common.logger as logger
import azurelinuxagent.common.utils.fileutil as fileutil
import azurelinuxagent.common.version as version

from azurelinuxagent.common.utils.flexible_version import FlexibleVersion
from azurelinuxagent.common.version import *


class TestCurrentAgentName(AgentTestCase):
    def setUp(self):
        AgentTestCase.setUp(self)
        return

    @patch("os.getcwd", return_value="/default/install/directory")
    def test_extract_name_finds_installed(self, mock_cwd):
        current_agent, current_version = set_current_agent()
        self.assertEqual(AGENT_LONG_VERSION, current_agent)
        self.assertEqual(AGENT_VERSION, str(current_version))
        return

    @patch("os.getcwd")
    def test_extract_name_finds_latest_agent(self, mock_cwd):
        path = os.path.join(conf.get_lib_dir(), "{0}-{1}".format(
            AGENT_NAME,
            "1.2.3"))
        mock_cwd.return_value = path
        agent = os.path.basename(path)
        version = AGENT_NAME_PATTERN.match(agent).group(1)
        current_agent, current_version = set_current_agent()
        self.assertEqual(agent, current_agent)
        self.assertEqual(version, str(current_version))
        return

class TestGetF5Platforms(AgentTestCase):
    def test_get_f5_platform_bigip_12_1_1(self):
        version_file = textwrap.dedent("""
        Product: BIG-IP
        Version: 12.1.1
        Build: 0.0.184
        Sequence: 12.1.1.0.0.184.0
        BaseBuild: 0.0.184
        Edition: Final
        Date: Thu Aug 11 17:09:01 PDT 2016
        Built: 160811170901
        Changelist: 1874858
        JobID: 705993""")

        mo = mock.mock_open(read_data=version_file)
        with patch(open_patch(), mo):
            platform = version.get_f5_platform()
            self.assertTrue(platform[0] == 'bigip')
            self.assertTrue(platform[1] == '12.1.1')
            self.assertTrue(platform[2] == 'bigip')
            self.assertTrue(platform[3] == 'BIG-IP')

    def test_get_f5_platform_bigip_12_1_0_hf1(self):
        version_file = textwrap.dedent("""
        Product: BIG-IP
        Version: 12.1.0
        Build: 1.0.1447
        Sequence: 12.1.0.1.0.1447.0
        BaseBuild: 0.0.1434
        Edition: Hotfix HF1
        Date: Wed Jun  8 13:41:59 PDT 2016
        Built: 160608134159
        Changelist: 1773831
        JobID: 673467""")

        mo = mock.mock_open(read_data=version_file)
        with patch(open_patch(), mo):
            platform = version.get_f5_platform()
            self.assertTrue(platform[0] == 'bigip')
            self.assertTrue(platform[1] == '12.1.0')
            self.assertTrue(platform[2] == 'bigip')
            self.assertTrue(platform[3] == 'BIG-IP')

    def test_get_f5_platform_bigip_12_0_0(self):
        version_file = textwrap.dedent("""
        Product: BIG-IP
        Version: 12.0.0
        Build: 0.0.606
        Sequence: 12.0.0.0.0.606.0
        BaseBuild: 0.0.606
        Edition: Final
        Date: Fri Aug 21 13:29:22 PDT 2015
        Built: 150821132922
        Changelist: 1486072
        JobID: 536212""")

        mo = mock.mock_open(read_data=version_file)
        with patch(open_patch(), mo):
            platform = version.get_f5_platform()
            self.assertTrue(platform[0] == 'bigip')
            self.assertTrue(platform[1] == '12.0.0')
            self.assertTrue(platform[2] == 'bigip')
            self.assertTrue(platform[3] == 'BIG-IP')

    def test_get_f5_platform_iworkflow_2_0_1(self):
        version_file = textwrap.dedent("""
        Product: iWorkflow
        Version: 2.0.1
        Build: 0.0.9842
        Sequence: 2.0.1.0.0.9842.0
        BaseBuild: 0.0.9842
        Edition: Final
        Date: Sat Oct  1 22:52:08 PDT 2016
        Built: 161001225208
        Changelist: 1924048
        JobID: 734712""")

        mo = mock.mock_open(read_data=version_file)
        with patch(open_patch(), mo):
            platform = version.get_f5_platform()
            self.assertTrue(platform[0] == 'iworkflow')
            self.assertTrue(platform[1] == '2.0.1')
            self.assertTrue(platform[2] == 'iworkflow')
            self.assertTrue(platform[3] == 'iWorkflow')

    def test_get_f5_platform_bigiq_5_1_0(self):
        version_file = textwrap.dedent("""
        Product: BIG-IQ
        Version: 5.1.0
        Build: 0.0.631
        Sequence: 5.1.0.0.0.631.0
        BaseBuild: 0.0.631
        Edition: Final
        Date: Thu Sep 15 19:55:43 PDT 2016
        Built: 160915195543
        Changelist: 1907534
        JobID: 726344""")

        mo = mock.mock_open(read_data=version_file)
        with patch(open_patch(), mo):
            platform = version.get_f5_platform()
            self.assertTrue(platform[0] == 'bigiq')
            self.assertTrue(platform[1] == '5.1.0')
            self.assertTrue(platform[2] == 'bigiq')
            self.assertTrue(platform[3] == 'BIG-IQ')
