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
import yaml

from notes_ai_agent.notes import base

logger = logging.getLogger(__name__)


class ObsidianNote(base.BaseNote):

    def _load(self) -> None:
        if self._note_loaded:
            return

        with open(self.file_path, 'r') as note_file:
            note_content = note_file.read()
            if note_content.startswith('---'):
                # We can assume that if note starts with "---" then
                # it has metadata section added by Obsidian
                note_content_splitted = note_content.split(
                    '---\n', 2)
                self._note['metadata'] = yaml.safe_load(
                    note_content_splitted[1]) or {}
                self._note['content'] = note_content_splitted[2]
            else:
                self._note['metadata'] = {}
                self._note['content'] = note_content

        self._note_loaded = True
