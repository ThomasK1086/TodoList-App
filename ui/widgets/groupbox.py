from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout

Builder.load_file("ui/widget_styles/groupbox.kv")

class GroupBox(BoxLayout):
    task_container = ObjectProperty(None)
    group_name = StringProperty()