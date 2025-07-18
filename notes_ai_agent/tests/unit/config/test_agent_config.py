# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import configparser
import os
import tempfile
import unittest
from unittest import mock

from notes_ai_agent.config import agent_config


class TestAgentConfig(unittest.TestCase):
    """Test cases for agent_config module"""

    def setUp(self):
        """Reset global state before each test"""
        # Reset global variables to their initial state
        agent_config._CONF = None
        agent_config._USER_CONFIG_FILE = agent_config._DEFAULT_USER_CONFIG_FILE

    def tearDown(self):
        """Clean up after each test"""
        # Reset global variables after each test
        agent_config._CONF = None
        agent_config._USER_CONFIG_FILE = agent_config._DEFAULT_USER_CONFIG_FILE

    def test_init_creates_config_with_defaults(self):
        """Test that init() creates a ConfigParser with default values"""
        # Ensure config is not initialized
        self.assertIsNone(agent_config._CONF)

        # Mock the config file reading to prevent real file interference
        with mock.patch.object(configparser.ConfigParser, 'read'):
            agent_config.init()

        self.assertIsNotNone(agent_config._CONF)
        self.assertIsInstance(agent_config._CONF, configparser.ConfigParser)

        # Check that default values are set
        self.assertEqual(agent_config._CONF['DEFAULT']['llm_driver'], '')
        self.assertEqual(
            agent_config._CONF['DEFAULT']['notes_driver'], 'obsidian'
        )
        self.assertEqual(
            agent_config._CONF['DEFAULT']['db_driver'], 'local_file'
        )

    def test_init_only_initializes_once(self):
        """Test that init() only initializes config once"""
        with mock.patch.object(configparser.ConfigParser, 'read') as mock_read:
            agent_config.init()
            config_first_call = agent_config._CONF

            agent_config.init()
            config_second_call = agent_config._CONF

            # Should be the same object
            self.assertIs(config_first_call, config_second_call)
            # read() should only be called once during first initialization
            self.assertEqual(mock_read.call_count, 1)

    def test_init_reads_user_config_file(self):
        """Test that init() attempts to read the user config file"""
        with mock.patch.object(configparser.ConfigParser, 'read') as mock_read:
            agent_config.init()
            mock_read.assert_called_once_with(
                agent_config._USER_CONFIG_FILE
            )

    def test_get_config_returns_initialized_config(self):
        """Test that get_config() returns the initialized configuration"""
        with mock.patch.object(configparser.ConfigParser, 'read'):
            config = agent_config.get_config()

            self.assertIsNotNone(config)
            self.assertIsInstance(config, configparser.ConfigParser)
            self.assertEqual(config, agent_config._CONF)

    def test_get_config_calls_init_if_not_initialized(self):
        """Test that get_config() calls init() if config is not initialized"""
        with mock.patch(
            'notes_ai_agent.config.agent_config.init'
        ) as mock_init:
            agent_config.get_config()
            mock_init.assert_called_once()

    def test_set_user_config_file(self):
        """Test setting a custom user config file path"""
        custom_path = "/custom/path/to/config.conf"
        agent_config.set_user_config_file(custom_path)

        self.assertEqual(agent_config._USER_CONFIG_FILE, custom_path)

    def test_set_user_config_file_affects_init(self):
        """Test that setting custom config file affects init() behavior"""
        custom_path = "/custom/path/to/config.conf"
        agent_config.set_user_config_file(custom_path)

        with mock.patch.object(configparser.ConfigParser, 'read') as mock_read:
            agent_config.init()
            mock_read.assert_called_once_with(custom_path)

    def test_set_configuration_values(self):
        """Test the private _set_configuration_values() function"""
        test_config = {
            'TEST_SECTION': {
                'test_option': 'test_value',
                'another_option': 'another_value'
            }
        }

        with mock.patch.object(configparser.ConfigParser, 'read'):
            agent_config._set_configuration_values(test_config)

            self.assertEqual(
                agent_config._CONF['TEST_SECTION']['test_option'],
                'test_value'
            )
            self.assertEqual(
                agent_config._CONF['TEST_SECTION']['another_option'],
                'another_value'
            )

    def test_set_configuration_values_calls_init(self):
        """Test that _set_configuration_values() calls init()"""
        test_config = {'TEST': {'key': 'value'}}

        with mock.patch(
                'notes_ai_agent.config.agent_config.init') as mock_init:
            # Mock init to actually initialize _CONF so the function doesn't
            # fail
            def mock_init_side_effect():
                if agent_config._CONF is None:
                    agent_config._CONF = configparser.ConfigParser()
            mock_init.side_effect = mock_init_side_effect

            agent_config._set_configuration_values(test_config)
            mock_init.assert_called_once()

    def test_register_options_adds_new_config_options(self):
        """Test that register_options() adds new configuration options"""
        new_options = {
            'NEW_SECTION': {
                'new_option': 'new_value',
                'another_new_option': 'another_new_value'
            }
        }

        with mock.patch.object(configparser.ConfigParser, 'read'):
            agent_config.register_options(new_options)

            self.assertEqual(
                agent_config._CONF['NEW_SECTION']['new_option'], 'new_value'
            )
            self.assertEqual(
                agent_config._CONF['NEW_SECTION']['another_new_option'],
                'another_new_value'
            )

    def test_register_options_reads_config_file(self):
        """Test that register_options() reads config after setting defaults"""
        new_options = {'TEST': {'key': 'value'}}

        with mock.patch.object(configparser.ConfigParser, 'read') as mock_read:
            agent_config.register_options(new_options)
            # register_options calls init() (which reads) and then reads again
            self.assertEqual(mock_read.call_count, 2)
            mock_read.assert_called_with(agent_config._USER_CONFIG_FILE)

    def test_register_options_calls_init(self):
        """Test that register_options() calls init()"""
        new_options = {'TEST': {'key': 'value'}}

        with mock.patch(
                'notes_ai_agent.config.agent_config.init'
                ) as mock_init:
            # Mock init to actually initialize _CONF so the function doesn't
            # fail
            def mock_init_side_effect():
                if agent_config._CONF is None:
                    agent_config._CONF = configparser.ConfigParser()
            mock_init.side_effect = mock_init_side_effect

            with mock.patch.object(configparser.ConfigParser, 'read'):
                agent_config.register_options(new_options)
            self.assertEqual(mock_init.call_count, 2)

    def test_integration_with_real_config_file(self):
        """Integration test with a real temporary config file"""
        with tempfile.NamedTemporaryFile(
                mode='w', suffix='.conf', delete=False) as temp_file:
            temp_file.write("""
[DEFAULT]
llm_driver = test_llm_driver
custom_option = custom_value

[CUSTOM_SECTION]
custom_key = custom_val
            """)
            temp_file_path = temp_file.name

        try:
            agent_config.set_user_config_file(temp_file_path)
            config = agent_config.get_config()

            # Check that file values override defaults
            self.assertEqual(config['DEFAULT']['llm_driver'],
                             'test_llm_driver')
            self.assertEqual(config['DEFAULT']['custom_option'],
                             'custom_value')
            self.assertEqual(config['CUSTOM_SECTION']['custom_key'],
                             'custom_val')

            # Check that other defaults are still present
            self.assertEqual(config['DEFAULT']['notes_driver'], 'obsidian')
            self.assertEqual(config['DEFAULT']['db_driver'], 'local_file')

        finally:
            os.unlink(temp_file_path)

    def test_init_with_nonexistent_config_file(self):
        """Test that init() handles nonexistent config files gracefully"""
        agent_config.set_user_config_file('/nonexistent/path/config.conf')

        # This should not raise an exception
        agent_config.init()

        # Should still have default values
        self.assertEqual(
            agent_config._CONF['DEFAULT']['notes_driver'], 'obsidian')
        self.assertEqual(
            agent_config._CONF['DEFAULT']['db_driver'], 'local_file')

    def test_multiple_register_options_calls(self):
        """Test multiple calls to register_options()"""
        options1 = {'SECTION1': {'key1': 'value1'}}
        options2 = {'SECTION2': {'key2': 'value2'}}

        with mock.patch.object(configparser.ConfigParser, 'read'):
            agent_config.register_options(options1)
            agent_config.register_options(options2)

            self.assertEqual(
                agent_config._CONF['SECTION1']['key1'], 'value1')
            self.assertEqual(
                agent_config._CONF['SECTION2']['key2'], 'value2')

    def test_register_options_overwrites_existing_sections(self):
        """Test that register_options() can overwrite existing sections"""
        initial_options = {'TEST_SECTION': {'key': 'initial_value'}}
        updated_options = {
            'TEST_SECTION': {
                'key': 'updated_value',
                'new_key': 'new_value'}}

        with mock.patch.object(configparser.ConfigParser, 'read'):
            agent_config.register_options(initial_options)
            self.assertEqual(
                agent_config._CONF['TEST_SECTION']['key'],
                'initial_value')

            agent_config.register_options(updated_options)
            self.assertEqual(
                agent_config._CONF['TEST_SECTION']['key'],
                'updated_value')
            self.assertEqual(
                agent_config._CONF['TEST_SECTION']['new_key'],
                'new_value')
