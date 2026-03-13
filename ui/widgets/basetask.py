import logging

from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder

from ui.widgets.utils import ModernPopup

#from domain.dtos.basetask import BaseTaskDTO
#from ui.widgets.simpletask import SimpleTaskBody

Builder.load_file("ui/widget_styles/basetask.kv")



class TaskDetailButtonsPanel(BoxLayout):
    __events__ = ('on_complete', 'on_delete', 'on_update', 'on_close')

    def on_complete(self, *args): pass
    def on_delete(self, *args): pass
    def on_update(self, *args): pass
    def on_close(self, *args): pass


class TaskDetailButton(Button):
    pass

# Base Task Popup (Handles the Title, Shell, and Buttons)
class TaskPopup(ModernPopup):
    content_area = ObjectProperty(None)
    dto = ObjectProperty(None)
    task_title = StringProperty("")

    def __init__(self, controller, dto: 'BaseTaskDTO', body_type: 'type[SimpleTaskBody]', **kwargs):
        self.controller = controller
        self.body_type = body_type

        self.dto = dto
        self.task_title = dto.title

        self.is_open = False

        super().__init__(**kwargs)
        #self.rebuild_content()

    def on_content_area(self, instance, middle_boxlayout):
        if middle_boxlayout:
            self.content_area = middle_boxlayout

    def on_dto(self, instance, value):
        """Fires automatically when self.dto changes."""
        self.task_title = value.title
        self.rebuild_content()

    def open(self):
        super().open()
        self.rebuild_content()

    def rebuild_content(self):
        """Internal helper to refresh the UI."""
        # Ensure BOTH the DTO and the UI container exist
        if not self.is_open:
            return

        logging.info(f"Popup: re-building content of popup window")
        if self.content_area and self.dto:
            self.content_area.clear_widgets()
            self.body = self.body_type(self.dto)
            self.content_area.add_widget(self.body)

    def on_press_close(self):
        self.controller.request_close()

    def on_press_update(self):
       self.controller.request_update(self.dto)

    def on_press_complete(self):
        self.controller.request_change_status(self.dto)

    def on_press_delete(self):
        self.controller.request_delete(self.dto)
