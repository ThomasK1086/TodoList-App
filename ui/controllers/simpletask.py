import logging

from domain.dtos.basetask import BaseTaskDTO
from domain.dtos.simpletask import SimpleTaskDTO
from ui.controllers.basetask import BaseTaskDetailsController
from ui.widgets.basetask import TaskPopup
from ui.widgets.simpletask import SimpleTaskBody, SimpleTaskListItem


class SimpleTaskDetailsController(BaseTaskDetailsController):
    def __init__(self, task_dto: BaseTaskDTO, task_service):
        super().__init__(task_dto, task_service)
        self.popup = TaskPopup(
            controller=self,
            dto=task_dto,
            body_type=SimpleTaskBody,
        )
        self.popup.is_open = False

        self.list_item = SimpleTaskListItem(
            controller=self,
            dto=task_dto,
        )


