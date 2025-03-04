# Copyright 2022 The AI Flow Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import io
import logging
import os
import unittest
from contextlib import redirect_stdout

from notification_service import settings
from notification_service.cli import cli_parser
from notification_service.cli.commands.config_command import config_init, config_get_value, config_list
from notification_service.settings import NOTIFICATION_HOME

logger = logging.getLogger(__name__)


class TestCliConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = cli_parser.get_parser()
        cls.config_str = """
            server_port: 50052
            db_uri: sqlite:///ns.db
            enable_ha: false
            ha_ttl_ms: 10000
            advertised_uri: 127.0.0.1:50052
        """
        cls.tmp_config_file = os.path.join(os.path.dirname(__file__), 'notification_server.yaml')
        with open(cls.tmp_config_file, 'w') as f:
            f.write(cls.config_str)
        settings.NOTIFICATION_HOME = os.path.dirname(__file__)

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(cls.tmp_config_file):
            os.remove(cls.tmp_config_file)

    def setUp(self) -> None:
        self.config_file = NOTIFICATION_HOME + '/notification_server.yaml'
        if os.path.exists(self.config_file):
            os.remove(self.config_file)

    def test_cli_config_get_value(self):
        config_init(self.parser.parse_args(['config', 'init']))
        with redirect_stdout(io.StringIO()) as stdout:
            config_get_value(self.parser.parse_args(['config', 'get-value', 'server_port']))
            self.assertEquals('50052', str.splitlines(stdout.getvalue())[0])
        with self.assertRaises(SystemExit):
            config_get_value(self.parser.parse_args(['config', 'get-value', 'server_ip']))

    def test_cli_config_init(self):
        with self.assertLogs('notification_service.cli.commands.config_command', 'INFO') as log:
            config_init(self.parser.parse_args(['config', 'init']))
            log_output = '\n'.join(log.output)
            self.assertIn('Notification server config generated at {}.'.format(self.config_file), log_output)

            config_init(self.parser.parse_args(['config', 'init']))
            log_output = "\n".join(log.output)
            self.assertIn('Notification server config has already initialized at {}.'.format(self.config_file),
                          log_output)

    def test_cli_config_list(self):
        config_init(self.parser.parse_args(['config', 'init']))
        with redirect_stdout(io.StringIO()) as stdout:
            config_list(self.parser.parse_args(['config', 'list']))
            self.assertIn('server_port: 50052', stdout.getvalue())
