from kivy.app import App
from kivy.base import Builder

from core.container import Container
from ui.widgets.example import MyWidget




Builder.load_file("ui/theme.kv")
class DoItApp(App):
    def build_config(self, config):
        config.setdefaults('section1', {
            'key1': 'value1',
            'key2': '42'
        })

    def build(self):
        self.container = Container()

        main_screen = self.container.get_main_screen()
        return main_screen

    def build_settings(self, settings):
        jsondata = """... put the json data here ..."""
        settings.add_json_panel('Test application',
                                self.config, data=jsondata)

    def on_pause(self):
      # Here you can save data if needed
      return True

    def on_resume(self):
      # Here you can check if any data needs replacing (usually nothing)
      pass

    def on_stop(self):
        self.container.stop()


if __name__ == "__main__":
    DoItApp().run()
