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

from stevedore.driver import DriverManager

from notes_ai_agent.llm import base_driver


_DRIVER = None

def load_driver(driver_name: str) -> None:
    global _DRIVER
    if not _DRIVER:
        mgr = DriverManager(
            namespace='notes_ai_agent.llm_drivers',
            name=driver_name,
            invoke_on_load=True,
            invoke_args=(),
        )
        _DRIVER = mgr.driver
        _DRIVER.initialize()


def get_loaded_driver():
    return _DRIVER
