import datetime
from dataclasses import dataclass

from domain.dtos.basetask import BaseTaskDTO, BaseTaskFactory
from utils import singleton
from utils.singleton import SingletonMetaclass


@dataclass(frozen=True, repr=False, order=False)
class SimpleTaskDTO(BaseTaskDTO):
    # From base class:
    #   id: int
    #   title: str
    #   group: int
    #   created_at: datetime.date
    id: int
    group_id: int
    task_type: str
    title: str

    created_at: datetime.date
    description: str
    _is_completed: bool = False

    @property
    def is_completed(self) -> bool:
        return self._is_completed


class SimpleTaskFactory(BaseTaskFactory, metaclass=SingletonMetaclass):
    def create(self,
        id: int,
        task_type: str,
        title: str,
        group: int,
        created_at: datetime.date,
        description: str,
        is_completed: bool = False,
        ) -> SimpleTaskDTO:
        return SimpleTaskDTO(
            id=id,
            title=title,
            type=task_type,
            group_id=group,
            created_at=created_at,
            description=description,
            _is_completed=is_completed
        )

    def __call__(self, *args, **kwargs) -> SimpleTaskDTO:
        return self.create(*args, **kwargs)