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

import json
import logging
import typing

from openai import OpenAI

from notes_ai_agent.config import agent_config
from notes_ai_agent import exceptions
from notes_ai_agent.llm import base_driver

logger = logging.getLogger(__name__)

DRIVER_CONFIG = {
    'OPENAI': {
        'model': 'gpt-4.1',
        'api_key': ''
    },
}

class LLMDriver(base_driver.BaseLLMDriver):

    def initialize(self) -> None:
        agent_config.register_options(DRIVER_CONFIG)
        cfg = agent_config.get_config()
        self.model = cfg['OPENAI']['model']
        self.api_key = cfg['OPENAI']['api_key']
        self._client = None
        if not self.api_key:
            logger.error("API Key for the OpenAI API is required.")
            raise exceptions.InvalidDriverConfiguration()
    
    @property
    def client(self):
        if not self._client:
            self._client = OpenAI(
                api_key=self.api_key,
            )
        return self._client

    def send_prompt(self,
                    user_prompt: str,
                    system_prompt: typing.Union[str, None] = None
                ) -> dict:
        logger.debug(f"Sending usert prompt: '{user_prompt}' to "
                     f"OpenAI LLM model {self.model}")

        llm_response = self.client.responses.create(
            model=self.model,
            input=user_prompt,
            instructions=system_prompt,
        )
        return json.loads(llm_response.output_text)