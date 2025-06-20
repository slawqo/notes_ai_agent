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
import typing

from notes_ai_agent.llm import system_prompts
from notes_ai_agent.notes import base as base_notes_driver


class BaseLLMDriver(ABC):

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def send_prompt(self,
                    user_prompt: str,
                    system_prompt: typing.Union[str, None] = None):
        pass

    def process_note(self, note_driver: base_notes_driver.BaseNote) -> dict:
        system_prompt = system_prompts.GET_KEYWORDS_MSG.format(
            keywords=note_driver.get_metadata().get('keywords', '')
        )
        return self.send_prompt(
            note_driver.get_content(),
            system_prompt
        )
