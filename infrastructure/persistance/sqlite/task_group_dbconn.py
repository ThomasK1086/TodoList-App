from infrastructure.persistance.sqlite.connection import DBConnection, BaseDatabaseInterface
import sqlite3


class TaskGroupDatabaseInterface(BaseDatabaseInterface):
    def _create_tables(self):
        # Create Groups table
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS groups
                            (
                                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                name TEXT NOT NULL UNIQUE
                            )
                            ''')
        self.cursor.execute('''
                            INSERT INTO groups ( name )
                            SELECT (
                                "default"
                                   )
                            WHERE NOT EXISTS (
                                SELECT 1 from groups WHERE name NOT NULL
                            )
                            ''')
        self.conn.commit()

    def save_group(self, name: str) -> int:
        """:returns: group_id"""
        try:
            self.cursor.execute("INSERT INTO groups (name) VALUES (?)", (name,))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            # Group name already exists
            return self.get_group_id_by_name(name)

    def get_group_id_by_name(self, name):
        """
        :param name: group name
        :return: group_id or None if name not found
        """
        self.cursor.execute("SELECT id FROM groups WHERE name = ?", (name,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def fetch_all_groups(self):
        query = '''
        SELECT groups.id, groups.name
        FROM groups
        '''
        self.cursor.execute(query)
        raw_data = self.cursor.fetchall()
        result = []
        for id, name in raw_data:
            result.append({
                "id": id,
                "name": name
            })
        return result

    def get_sync_params(self):
        query = '''
        SELECT
        COUNT(*), MAX(id)
        FROM groups
        '''
        self.cursor.execute(query)
        res = self.cursor.fetchone()
        return res[0], res[1]
