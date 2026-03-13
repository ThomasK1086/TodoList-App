from infrastructure.persistance.sqlite.task_dbconn import TaskDatabaseInterface
from infrastructure.persistance.sqlite.task_group_dbconn import TaskGroupDatabaseInterface

from services.task_service import TaskService
from ui.controllers.mainscreen import MainScreenController

from ui.screens.mainscreen import MainScreen


class SettingsViewModel:
    pass


class Container:
    def __init__(self):
        self.task_db_interface = TaskDatabaseInterface(db_name="todolist.sqlite")
        self.task_group_db_interface = TaskGroupDatabaseInterface(db_name="todolist.sqlite")

        self.task_creation_service = TaskService(db_task_interface=self.task_db_interface,
                                                 db_group_interface=self.task_group_db_interface)

        # Other services...


    def get_settings_vm(self):
        return SettingsViewModel(self.nav_service)

    def stop(self):
        self.task_db_interface.conn.close()


    def get_main_screen(self):
        mainscreen_controller = MainScreenController(self.task_creation_service)
        mainscreen = MainScreen(controller=mainscreen_controller)
        return mainscreen

