import logging

from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, ListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.base import Builder
from kivy.uix.scrollview import ScrollView

from domain.dtos.basetask import BaseTaskDTO
from domain.dtos.simpletask import SimpleTaskDTO
from ui.widgets.basetask import TaskPopup

#from ui.controllers.simpletask import SimpleTaskDetailsController

Builder.load_file("ui/widget_styles/simpletask.kv")

from ui.theme import *

class SimpleTaskBody(ScrollView):
    dto = ObjectProperty(None)

    def __init__(self, dto: BaseTaskDTO, **kwargs):
        assert isinstance(dto, SimpleTaskDTO)
        self.task_title = dto.title
        self.description = dto.description
        self.creation_date = dto.created_at.strftime("%d/%m/%Y %I:%M:%S %p")
        self.is_completed = dto.is_completed

        # trigger ui update
        self.dto = dto
        super().__init__(**kwargs)

    def on_dto(self, instance, value: BaseTaskDTO):
        assert isinstance(value, SimpleTaskDTO)

        self.task_title = value.title
        self.description = value.description
        self.creation_date = value.created_at.strftime("%d/%m/%Y %I:%M:%S %p")
        self.is_completed = value.is_completed



class SimpleTaskListItem(ButtonBehavior, BoxLayout):
    dto = ObjectProperty(None)
    color = ListProperty([1, 1, 1, 1])

    def __init__(self, controller, dto: BaseTaskDTO, **kwargs):
        assert isinstance(dto, SimpleTaskDTO)
        self.dto = dto
        self.controller = controller

        cutoff = 100
        display_label = f"{dto.title}: {dto.description}"
        is_overlong = (len(display_label) > cutoff)


        display_label = display_label[:(cutoff-3)] if is_overlong else display_label + "..."
        self.display_label = dto.title
        self._set_color()
        super().__init__(**kwargs)

    def on_release(self):
        self.controller.request_open_details()

    def _set_color(self):
        self.color = (COLOR_DARKERGREEN if self.dto.is_completed else COLOR_DARKGREEN)
        self.hover_color = HOVERCOLOR

    def on_checkbox_activate(self):
        logging.warning(f"SimpleTaskListItem: Checkbox was activated")
        self.controller.request_change_status(self.dto)
        self._set_color()
