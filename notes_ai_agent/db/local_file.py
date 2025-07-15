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

import os
from pathlib import Path

from notes_ai_agent.config import agent_config
from notes_ai_agent.db import base_driver


DB_CONFIG = {
    'LOCAL_FILE_DATABASE': {
        'database_file': f'{Path.home()}/.config/notes_ai_agent_tags'
    }
}


class LocalFileDBDriver(base_driver.BaseDBDriver):

    def __init__(self) -> None:
        agent_config.register_options(DB_CONFIG)
        cfg = agent_config.get_config()
        self.tags_file = cfg['LOCAL_FILE_DATABASE']['database_file']

    def initialize(self) -> None:
        if not os.path.exists(self.tags_file):
            with open(self.tags_file, 'w') as file:
                file.write('')

    def get_tags(self) -> set[str]:
        if not os.path.exists(self.tags_file):
            return set()
        with open(self.tags_file, 'r') as file:
            return set(file.read().splitlines())

    def save_tags(self, tags: set[str]) -> None:
        with open(self.tags_file, 'w') as file:
            for tag in sorted(tags):
                file.write(f"{tag}\n")
