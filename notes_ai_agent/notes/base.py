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
import hashlib
import typing
import yaml

from notes_ai_agent.notes import constants


class BaseNote(ABC):

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self._note_loaded = False
        self._note = {
            "metadata": {},
            "content": ""
        }

    @abstractmethod
    def _load(self) -> None:
        pass

    def get_content(self) -> str:
        self._load()
        return self._note['content']

    def get_metadata(self) -> dict:
        self._load()
        return self._note['metadata'] or {}

    def get_tags(self) -> set[str]:
        tags = self.get_metadata().get(
            constants.TAGS_KEY, '').split(",")
        return {tag.strip() for tag in tags if tag.strip()}

    def add_metadata(self, key: str,
                     value: typing.Union[str, list]) -> None:
        self._note['metadata'][key] = value

    def processing_forbidden(self):
        return self.get_metadata().get(constants.LLM_FORBIDDEN_KEY, False)

    def content_changed(self):
        content_md5 = self._get_content_md5()
        previous_content_md5 = \
            self.get_metadata().get(constants.CONTENT_MD5_KEY)
        return content_md5 != previous_content_md5

    def _get_content_md5(self):
        return hashlib.md5(
            self.get_content().encode('utf-8')).hexdigest()

    def save(self) -> None:
        content_md5 = self._get_content_md5()
        self.add_metadata(constants.CONTENT_MD5_KEY, content_md5)
        note_metadata = yaml.safe_dump(
            self.get_metadata(), allow_unicode=True)
        full_note_str = f"---\n{note_metadata}\n---\n{self.get_content()}"
        with open(self.file_path, "w", encoding='utf-8') as note_file:
            note_file.write(full_note_str)
