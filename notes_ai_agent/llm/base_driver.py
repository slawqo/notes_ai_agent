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

from abc import ABC
from abc import abstractmethod
import typing

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

    def process_note(self, note: base_notes_driver.BaseNote,
                     existing_tags: set[str]) -> dict:
        existing_tags.update(note.get_tags())
        system_prompt = system_prompts.GET_TAGS_MSG.format(
            tags="\n".join(existing_tags)
        )
        llm_response = self.send_prompt(
            note.get_content(),
            system_prompt
        )
        return llm_response
