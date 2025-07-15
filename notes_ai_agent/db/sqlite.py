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

import os
import sqlite3

from notes_ai_agent.config import agent_config
from notes_ai_agent.db import base_driver


DB_CONFIG = {
    'DATABASE': {
        'database_file': os.path.join(
            os.path.expanduser('~'), '.config.notes_ai_agent.db')
    }
}

KEYWORDS_SEPARATOR = ","

class Database:

    def __init__(self) -> None:
        agent_config.register_options(DB_CONFIG)
        cfg = agent_config.get_config()
        self.db_file = cfg['DATABASE']['database_file']
        self.conn = sqlite3.connect(self.db_file)
        self._init_db()

    def close(self) -> None:
        self.conn.close()

    def _init_db(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS document_keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_path TEXT NOT NULL,
                keywords TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_keywords(self, document_path: str, keywords: set[str]) -> None:
        keywords_str = KEYWORDS_SEPARATOR.join(keywords)
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO document_keywords (document_path, keywords) VALUES (?, ?)
        """, (document_path, keywords_str))
        self.conn.commit()

    def get_all_keywords(self) -> set[str]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT keywords FROM document_keywords
        """)
        keywords = set()
        for row in cursor.fetchall():
            keywords.update(row[0].split(KEYWORDS_SEPARATOR))
        return keywords

    def get_document_keywords(self, document_path: str) -> set[str]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT keywords FROM document_keywords WHERE document_path = ?",
            (document_path,)
        )
