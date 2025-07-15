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

import argparse
from notes_ai_agent.config import agent_config


def get_cli_program():
    parser = argparse.ArgumentParser(
        prog='Notes AI Agent',
        description=(
            'This is small AI Agent whose only goal '
            'is to parse given markdown document, send '
            'it to the configured LLM model to get '
            'tags and summary and update it in the '
            'markdown tags section.'
        )
    )
    parser.add_argument('filepath')
    parser.add_argument('-c', '--config-file',
                        default=agent_config._DEFAULT_USER_CONFIG_FILE)
    parser.add_argument('-v', '--verbose',
                        action='store_true')
    return parser
