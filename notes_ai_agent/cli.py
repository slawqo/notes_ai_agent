#
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

import logging
import sys

from notes_ai_agent.config import agent_config as config
from notes_ai_agent.config import cli_config
from notes_ai_agent.llm import driver_manager as llm_driver_manager
from notes_ai_agent.notes import constants as notes_constants
from notes_ai_agent.notes import notes_manager

logger = logging.getLogger(__name__)


def main():
    # TODO: add config file path here, it should be taken
    # from the argparse
    cli_prog = cli_config.get_cli_program()
    cli_arguments = cli_prog.parse_args()
    if cli_arguments.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if cli_arguments.config_file:
        config.set_user_config_file(cli_arguments.config_file)
    cfg = config.get_config()

    llm_driver_name = cfg['DEFAULT']['llm_driver']
    if not llm_driver_name:
        logging.error("'llm_driver' has to be specified")
        sys.exit(1)

    llm_driver_manager.load_driver(llm_driver_name)
    llm_driver = llm_driver_manager.get_loaded_driver()

    note = notes_manager.load_note(
        cfg['DEFAULT']['notes_driver'],
        file_path=cli_arguments.filepath
    )
    if note.processing_forbidden():
        logger.info(f"Processing of the note {cli_arguments.filepath} "
                    "by the LLM is not allowed.")
        sys.exit(0)

    if not note.content_changed():
        logger.info(f"Content of the note {cli_arguments.filepath} "
                    "has not changed. No processing needed.")
        sys.exit(0)

    new_note_metadata = llm_driver.process_note(note)
    note.add_metadata(
        notes_constants.KEYWORDS_KEY,
        new_note_metadata['keywords']
    )
    if new_note_metadata.get('summary'):
        note.add_metadata(
            notes_constants.SUMMARY_KEY,
            new_note_metadata['summary']
        )
    note.save()
