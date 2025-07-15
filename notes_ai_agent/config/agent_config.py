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
from pathlib import Path


_CONF = None


_DEFAULT_USER_CONFIG_FILE = f"{Path.home()}/.config/notes_ai_agent.conf"
_USER_CONFIG_FILE = _DEFAULT_USER_CONFIG_FILE

DEFAULT_CONFIG = {
    'DEFAULT': {
        'llm_driver': '',  # This is mandatory to be set in the config file
        'notes_driver': 'obsidian',
        'db_driver': 'sqlite',
    },
}


def _get_config() -> configparser.ConfigParser:
    init()
    return _CONF


def _set_configuration_values(configuration_values: dict) -> None:
    global _CONF
    init()
    for section, options in configuration_values.items():
        _CONF[section] = options


def set_user_config_file(file_path: str) -> None:
    global _USER_CONFIG_FILE
    _USER_CONFIG_FILE = file_path


def init() -> None:
    """Init configuration and load values from the config file"""
    global _CONF
    if not _CONF:
        _CONF = configparser.ConfigParser()
        _set_configuration_values(DEFAULT_CONFIG)
        _CONF.read(_USER_CONFIG_FILE)


def get_config() -> configparser.ConfigParser:
    init()
    return _CONF


def register_options(config_options: dict):
    """Register new config options with default values

    This function is used to set default values of config options
    needed for example by any of the drivers.
    """
    init()
    _set_configuration_values(config_options)
    _CONF.read(_USER_CONFIG_FILE)
