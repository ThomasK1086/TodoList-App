import logging
from typing import TypedDict, List, Dict

from kivy.uix.label import Label

from services import task_service
from ui.controllers.simpletask import SimpleTaskDetailsController
from ui.widgets.groupbox import GroupBox
from ui.widgets.simpletask import SimpleTaskBody
from domain.dtos.basetask import BaseTaskDTO
from utils.types import TasksByGroup


class MainScreenController:
    def __init__(self, task_service: task_service.TaskService):
        self.task_service = task_service
        self._message = "Hello Thomas"
        self.on_change_callbacks = []
        self._refresh_tasklist()

        self.screen = None

    def _refresh_tasklist(self):
        self.tasks_per_group: Dict[int, TasksByGroup] = self.task_service.get_tasks_per_group()

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value
        # Notify whoever is listening (The Widget)
        for callback in self.on_change_callbacks:
            callback(value)

    def rebuild_content(self):
        self._refresh_tasklist()
        group_box_widgets = []

        for group_id, info in self.tasks_per_group.items():
            name = info['group_name']
            task_list = info['tasks']

            box = GroupBox(group_name=name)

            for task_dto in task_list:
                task_controller = SimpleTaskDetailsController(task_dto, task_service=self.task_service)

                task_controller.on_close_callbacks.append(self.rebuild_content)
                task_widget = task_controller.request_list_item()
                box.add_widget(task_widget)

            group_box_widgets.append(box)

        self.screen.group_scroll_view.clear_widgets()
        for box in group_box_widgets:
            self.screen.group_scroll_view.add_widget(box)

    def _display_group_block(self):
        pass

    def on_content_area(self, mainscreen, middle_content_box):
        logging.info("Requested content for main screen")
        pass

    def request_create_task(self):
        self.task_service.create_task()
        self.rebuild_content()

    def open_detail_view(self, task_id, task_type, group_id):
        # TODO: Consider moving this to an ui controller?
        logging.info(f"Requested details on task with id={task_id}.")
        try:
            task_dbo = self.task_service._get_task(task_id, task_type)

            detailview_controller = SimpleTaskDetailsController(task_dbo)
            detailview_controller.request_open_details()
        except Exception as e:
            logging.error(f"Could not open Detail view: {e}")