import datetime
from typing import List

from infrastructure.persistance.sqlite.connection import DBConnection, BaseDatabaseInterface
import sqlite3

from utils.types import Task_DB_Transferobject, TaskMetaData_DB_Transferobject


class TaskDatabaseInterface(BaseDatabaseInterface):
    def _create_tables(self):
        """Initializes the tasks table scheme."""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            group_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            date DATETIME NOT NULL,
            json_payload TEXT,
            FOREIGN KEY ( group_id ) REFERENCES groups ( id )
        )
        ''')
        self.conn.commit()

    def save_task(self, task_id: int, group_id: int, task_type: str, date: datetime.date, json_payload: str) -> int:
        if task_id >= 0:
            self.cursor.execute('''
            INSERT OR REPLACE INTO tasks 
            (id, group_id, type, date, json_payload) 
            VALUES (?, ?, ?, ?, ?)
            ''', (task_id, group_id, task_type, date, json_payload)
            )
        else:
            self.cursor.execute('''
            INSERT OR REPLACE INTO tasks 
            (group_id, type, date, json_payload) 
            VALUES (?, ?, ?, ?)
            ''', (group_id, task_type, date, json_payload)
            )
        id_of_inserted = self.cursor.lastrowid

        # todo: add commit/rollback by service that calls this method on conn
        self.conn.commit()
        return id_of_inserted


    def get_task_by_id(self, task_id: int, include_group_name: bool = False) -> Task_DB_Transferobject:
        if include_group_name:
            query = '''
            SELECT tasks.id, tasks.group_id, tasks.type, tasks.date, tasks.json_payload, groups.name 
            FROM tasks
                JOIN groups ON tasks.group_id = groups.id
            WHERE tasks.id = ?
            '''
        else:
            query = '''
            SELECT *
            FROM tasks
            WHERE id = ?
            '''
        self.cursor.execute(query, (task_id, ))
        raw_result = self.cursor.fetchone()
        if raw_result is None:
            raise KeyError(f"Task with id={task_id} could not be fetched from the DB: Id not found.")

        if include_group_name:
            _, group_id, task_type, date, json_payload, group_name = raw_result
        else:
            _, group_id, task_type, date, json_payload = raw_result
        result: Task_DB_Transferobject = {
            "id": task_id,
            "group_id": group_id,
            "task_type": task_type,
            "date": date,
            "json_payload": json_payload,
        }
        if include_group_name: result['group_name'] = group_name
        return result

    def fetch_all_tasks(self) -> List[TaskMetaData_DB_Transferobject]:
        """Returns tasks joined with their group names for the UI."""
        query = """
                SELECT tasks.id, group_id, type
                FROM tasks
                         JOIN groups ON tasks.group_id = groups.id \
                """
        self.cursor.execute(query)
        raw_data =  self.cursor.fetchall()

        result = []
        for task_id, group_id, task_type in raw_data:
            result.append({
                "id": task_id,
                "group_id": group_id,
                "task_type": task_type
            })
        return result

    def get_sync_params(self):
        query = '''
        SELECT
        COUNT(*), MAX(id)
        FROM tasks
        '''
        self.cursor.execute(query)
        res = self.cursor.fetchone()
        return res[0], res[1]

    def delete_task(self, id):
        query = '''
        DELETE FROM tasks WHERE id = ?
        '''
        self.cursor.execute(query, (id,))
        pass
