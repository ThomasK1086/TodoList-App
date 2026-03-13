import logging

from domain.dtos.basetask import BaseTaskDTO
from domain.dtos.simpletask import SimpleTaskDTO
from ui.widgets.basetask import TaskPopup
from ui.widgets.simpletask import SimpleTaskBody, SimpleTaskListItem


class BaseTaskDetailsController:
    def __init__(self, task_dto: BaseTaskDTO, task_service):
        self.popup = None
        self.list_item = None

        self.task_service = task_service

        self.on_close_callbacks=[]

    def request_list_item(self):
        return self.list_item

    def request_open_details(self):
        self.popup.is_open = True
        logging.debug("BaseTaskController: Received request to open popup.")
        self.popup.open()

    def request_change_status(self, dto):
        logging.debug("BaseTaskController: Received request to change task status.")
        new_dto = self.task_service.change_task_status(dto)

        self.popup.dto = new_dto
        self.list_item.dto = new_dto

    def request_delete(self, dto):
        logging.debug("BaseTaskController: Received request to delete task.")
        self.task_service.delete_task(dto)
        self.request_close()

    def request_update(self, dto):
        logging.debug("BaseTaskController: Received request to update task.")
        new_dto = self.task_service.update_task(dto)

        self.popup.dto = new_dto
        self.list_item.dto = new_dto

    def request_close(self):
        logging.debug("BaseTaskController: Received request to close popup.")
        self.popup.is_open = False
        self.popup.dismiss()
        for callback in self.on_close_callbacks:
            callback()
