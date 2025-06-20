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


from notes_ai_agent.common import driver_manager as common_driver_manager


_DRIVER = None

def load_note(driver_name: str, **driver_kwargs) -> None:
    global _DRIVER
    if not _DRIVER:
        _DRIVER = common_driver_manager.load_driver(
            driver_name,
            'notes_ai_agent.note_drivers',
            **driver_kwargs
        )
    return _DRIVER


def get_loaded_driver():
    return _DRIVER
