from kivy.lang import Builder
from kivy.uix.popup import Popup

Builder.load_file("ui/widget_styles/utils.kv")

class ModernPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def open(self):
        super().open()