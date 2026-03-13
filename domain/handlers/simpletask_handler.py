import datetime
import json
import logging
from typing import Dict, Any

from domain.dtos.simpletask import SimpleTaskDTO
from domain.handlers.basetask_handler import BaseTaskHandler
from utils.types import Task_DB_Transferobject


class SimpleTaskHandler(BaseTaskHandler):
    @classmethod
    def create(cls,
               id: int,
               task_type: str,
               title: str,
               group: int,
               created_at: datetime.date,
               description: str,
               is_completed: bool = False,
               ) -> SimpleTaskDTO:
        task = SimpleTaskDTO(
            id=id,
            title=title,
            task_type=task_type,
            group_id=group,
            created_at=created_at,
            description=description,
            _is_completed=is_completed
        )
        return task

    @classmethod
    def serialize(cls, task: SimpleTaskDTO) -> Dict[str, Any]:
        s = cls._pre_serialize(task)
        extended_attributes = {
            "title": task.title,
            "description": task.description,
            "is_completed": task.is_completed,
        }
        s["json_payload"] = json.dumps(extended_attributes)
        return s

        return s

    @classmethod
    def deserialize(cls, task_dict: Task_DB_Transferobject) -> SimpleTaskDTO | None:
        payload = cls._pre_deserialize(task_dict)
        if payload is None:
            return None

        id, group_id, task_type, created_at, extended_attributes = payload
        try:
            title = extended_attributes["title"]
            description = extended_attributes["description"]
            is_completed = extended_attributes["is_completed"]
        except KeyError as e:
            logging.error(f"Deserialization error: unexpected or wrong JSON payload for SimpleTask {id}."
                          f"Received {extended_attributes}, which lead to Keyerror: {e}.")
            return None

        return SimpleTaskDTO(
            id=id,
            group_id=group_id,
            task_type=task_type,
            created_at=created_at,
            title=title,
            description=description,
            _is_completed=is_completed,
        )



    @classmethod
    def to_str(cls, task: SimpleTaskDTO, short: bool = True) -> str:
        s =  f"SimpleTaskDTO: (title={task.title}, description={task.description}"
        if not short:
            s += f", type={task.type}, id={task.id}), group_id={task.group_id}, created_at={task.created_at}, is_completed={task.is_completed}"
        s += ")"
        return s

    @classmethod
    def update(cls, dto: SimpleTaskDTO, **kwargs) -> SimpleTaskDTO:
        args = {}
        for a in ["title", "description", "group_id","created_at"]:
            args[a] = kwargs.get(a, None) or getattr(dto, a)
        for a in ["id", "task_type"]:
            args[a] = getattr(dto, a)

        if "_is_completed" in kwargs:
            s = kwargs.get("_is_completed")
        elif "is_completed" in kwargs:
            s = kwargs.get("is_completed")
        else:
            s = getattr(dto, "is_completed")
        args["_is_completed"] = s

        return SimpleTaskDTO(
            **args
        )