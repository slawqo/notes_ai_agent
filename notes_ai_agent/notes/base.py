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


class BaseNote(ABC):
    
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self._note_loaded = False
        self._note = {
            "metadata": {},
            "content": ""
        }

    @abstractmethod
    def _load_note(self) -> None:
        pass

    def get_note_content(self) -> str:
        self._load_note()
        return self._note['content']

    def get_note_metadata(self) -> dict:
        self._load_note()
        return self._note['metadata']

    def add_metadata(self, key: str,
                     value: typing.Union[str, list]) -> None:
        pass

    def safe_note(self) -> None:
        pass