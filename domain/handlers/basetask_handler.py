import json
import logging
from datetime import date
from json import JSONDecodeError

from utils.types import Task_DB_Transferobject

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from domain.dtos.basetask import BaseTaskDTO
from utils.singleton import SingletonMetaclass
from typing import Dict, Any, Tuple


class BaseTaskHandler(metaclass=SingletonMetaclass):
    def __init__(self, *args, **kwargs):
        logger.debug("Init called")
        pass

    @classmethod
    def create(cls, *args, **kwargs) -> BaseTaskDTO:
        ...

    @classmethod
    def serialize(cls, task: BaseTaskDTO) -> Dict[str, Any]:
        ...

    @classmethod
    def _pre_deserialize(cls, task_dict: Task_DB_Transferobject) -> Tuple[int, int, str, date, Dict[str, Any]] | None:
        try:
            id = task_dict["id"]
            group_id = task_dict["group_id"]
            task_type = task_dict["task_type"]
            date = task_dict["date"]
            extended_attr = json.loads(task_dict["json_payload"])

            return id, group_id, task_type, date, extended_attr
        except KeyError as e:
            logging.error(f"Failed in pre-deserialization of task (payload={task_dict}: {e}")
        except JSONDecodeError as e:
            id = task_dict["id"]
            group_id = task_dict["group_id"]
            task_type = task_dict["task_type"]
            logging.error(f"Failed in pre-deserialization JSON-Decoding of task {id=}, {task_type=}: {e}")
        return None

    @classmethod
    def _pre_serialize(cls, task: BaseTaskDTO) -> Dict[str, Any]:

        s = {
            "task_id": task.id,
            "group_id": task.group_id,
            "task_type": task.task_type,
            "date": task.created_at
        }
        return s


    @classmethod
    def deserialize(cls, task_dict: Dict[str, Any]) -> BaseTaskDTO:
        ...

    @classmethod
    def to_str(cls, task_dto):
        ...

    @classmethod
    def update(cls, task_dto: BaseTaskDTO, **kwargs) -> BaseTaskDTO:
        ...