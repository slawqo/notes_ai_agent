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

from abc import ABC, abstractmethod
import os
import typing

from notes_ai_agent.config import agent_config as config
from notes_ai_agent.llm import system_prompts
from notes_ai_agent.notes import base as base_notes_driver


class BaseLLMDriver(ABC):

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def send_prompt(
            self,
            user_prompt: str,
            system_prompt: typing.Union[str, None] = None) -> dict:
        pass

    def get_known_tags(self) -> set[str]:
        tags_file = config.get_config()['DEFAULT']['local_tags_file']
        if not os.path.exists(tags_file):
            return set()
        with open(tags_file, 'r') as file:
            return set(file.read().splitlines())

    def save_tags(self, tags: set[str]) -> None:
        tags_file = config.get_config()['DEFAULT']['local_tags_file']
        with open(tags_file, 'w') as file:
            file.write('\n'.join(tags))

    def process_note(self, note_driver: base_notes_driver.BaseNote) -> dict:
        current_tags = self.get_known_tags()
        current_tags.update(note_driver.get_tags())
        system_prompt = system_prompts.GET_TAGS_MSG.format(
            tags=current_tags
        )
        llm_response = self.send_prompt(
            note_driver.get_content(),
            system_prompt
        )
        current_tags.update(llm_response['tags'])
        self.save_tags(current_tags)
        return llm_response
