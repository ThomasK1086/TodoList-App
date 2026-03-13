from typing import TypedDict, List
from datetime import date

from domain.dtos.basetask import BaseTaskDTO

class Task_DB_Transferobject(TypedDict):
    id: int
    group_id: int
    task_type: str
    date: date
    json_payload: str
    group_name: str

class TaskMetaData_DB_Transferobject(TypedDict):
    id: int
    group_id: int
    task_type: str

class TaskGroup(TypedDict):
    id: int
    name: str

class TasksByGroup(TypedDict):
    group_name: str
    tasks: List[BaseTaskDTO]