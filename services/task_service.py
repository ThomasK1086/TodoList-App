import logging
from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Union

from domain.dtos.basetask import BaseTaskDTO

from infrastructure.persistance.sqlite.task_dbconn import TaskDatabaseInterface
from infrastructure.persistance.sqlite.task_group_dbconn import TaskGroupDatabaseInterface
from utils.singleton import SingletonMetaclass

from core.registry import TaskFeatureRegistry
from utils.types import TaskGroup, TaskMetaData_DB_Transferobject, TasksByGroup


class TaskService(metaclass=SingletonMetaclass):
    def __init__(self,
                 db_task_interface: TaskDatabaseInterface,
                 db_group_interface: TaskGroupDatabaseInterface
                 ):
        self.db_task_interface = db_task_interface
        self.db_group_interface = db_group_interface
        self.registry = TaskFeatureRegistry()


    def create_task(self, task_type: str ="simple_task") -> None:
        #TODO: Move to task creation service
        task = self.registry.get_feature(task_type)

        task_dto = task.handler.create(
            id=-1,
            title="Test2",
            task_type="simple_task",
            group=0,
            created_at=datetime.now(),
            description="Clean the Kitchen"
        )
        validation_ok = task.validator.validate(task_dto)
        id = self._save_task(task_dto)
        logging.info(f"TaskSaver.create_task: Task created with {id=}.")

    def _save_task(self, task_dto: BaseTaskDTO) -> int:
        task = self.registry.get_feature(task_dto.task_type)
        task_serial = task.handler.serialize(task_dto)
        id = self.db_task_interface.save_task(**task_serial)
        logging.info(f"TaskService._save_task: Task saved with {id=}.")
        return id

    def _get_task(self, id: int, task_type: str) -> BaseTaskDTO:
        serial_task = self.db_task_interface.get_task_by_id(id)
        task = self.registry.get_feature(task_type)
        task_dto = task.handler.deserialize(serial_task)
        return task_dto

    def delete_task(self, task_dto) -> bool:
        self.db_task_interface.delete_task(task_dto.id)
        self.db_task_interface.conn.commit()
        return True

    def change_task_status(self, task_dto) -> BaseTaskDTO:
        task = self.registry.get_feature(task_dto.task_type)
        new_dto = task.handler.update(task_dto, is_completed=(not task_dto.is_completed))
        logging.info(f"TaskService.change_task_status: Flipping status: old={task_dto.is_completed}, new={new_dto.is_completed}")
        self._save_task(new_dto)
        return new_dto

    def update_task(self, task_dto) -> BaseTaskDTO:
        return task_dto


    def _get_all_groups(self) -> List[TaskGroup]:
        group_list = self.db_group_interface.fetch_all_groups()
        return group_list # List[{id: int, name: str}]

    def _get_all_task_metadata(self) -> List[TaskMetaData_DB_Transferobject]:
        task_list = self.db_task_interface.fetch_all_tasks()
        return task_list # List[{id: int, group_id: int, task_type: str}]

    def get_tasks_per_group(self) -> Dict[int, TasksByGroup]:
        groups_with_tasks = {}
        groups = self._get_all_groups()
        task_metadata = self._get_all_task_metadata()
        for group in groups:
            group_id = group["id"]
            groups_with_tasks[group_id] = {
                "group_name": group["name"],
                "tasks": []
            }
        for task_info in task_metadata:
            id = task_info["id"]
            group_id = task_info["group_id"]
            task_type = task_info["task_type"]

            task_dto = self._get_task(id, task_type)

            groups_with_tasks[group_id]["tasks"].append(task_dto)
        return groups_with_tasks



