from UI.login_window import LoginWindow
from UI.register_window import RegisterWindow
from UI.main_window import MainWindow
from UI.settings_window import SettingsWindow
from UI.models_window import ModelsWindow

from app.queries import addModel, getModels
from app.session import Session

class WindowManager:
    def __init__(self):
        self.models_list = {}

        self.active_model_name = None
        self.active_model_path = None

        self.login_window = LoginWindow(self)
        self.register_window = RegisterWindow(self)
        self.main_window = MainWindow(self)
        self.settings_window = SettingsWindow(self)
        self.models_window = ModelsWindow(self)

        self.windows = {
            "login": self.login_window,
            "register": self.register_window,
            "main": self.main_window,
            "settings": self.settings_window,
            "models": self.models_window,
        }

    def switch(self, window_name):
        for window in self.windows.values():
            window.hide()
        self.windows[window_name].show()
        self.windows[window_name].update_user()

    def show(self, window_name):
        self.windows[window_name].show()
        self.windows[window_name].update_user()

    def getModels(self):
        self.models_list = getModels(Session.current_user["user_id"])
        return self.models_list

    def setActiveModel(self, name):
        for model_name, path in self.models_list:
            if model_name == name:
                self.active_model_name = model_name
                self.active_model_path = path
                print("Active model: ", self.active_model_name, self.active_model_path)
                break
