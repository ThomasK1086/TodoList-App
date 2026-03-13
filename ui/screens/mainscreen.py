import logging

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.label import Label

#from kivy.uix.screenmanager import Screen
from ui.widgets.groupbox import GroupBox

Builder.load_file("ui/screen_styles/mainscreen.kv")


class MainScreen(BoxLayout):
    # Kivy-specific property for the .kv file to bind to
    ui_display_name = StringProperty("<not fetched>")
    group_scroll_view = ObjectProperty(None)

    def __init__(self, controller, **kwargs):
        # Two-way link screen <-> controller
        self.controller = controller
        controller.screen = self

        self.ui_display_name = self.controller.message

        super().__init__(**kwargs)
        #self._update_ui(None, None)

    def on_group_scroll_view(self, mainscreen, group_scroll_view):
        logging.debug("MainScreen: Requested ui update for main screen")
        self._update_ui()

    def _update_ui(self):
        # Ensure the UI update happens on the main Kivy thread
        self.controller.rebuild_content()


    def on_button_click(self):
        self.controller.request_create_task()