from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from mindbox.jarvis_db import is_record_exist, create_record
from mindbox.widgets.messages import send_record_exist_msg
from mindbox.open_commands import open_window
from mindbox.string_operation import get_keywords_from_string
from mindbox.windows.window_names import MAIN_WINDOW


class CreateWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name_text_input = ObjectProperty()
        self.keywords_text_input = ObjectProperty()
        self.file_or_dir_button = ObjectProperty()
        self.scr_manager = self.manager


    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.config_keyboard()


    def config_keyboard(self):
        self.keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self.keyboard.bind(on_key_down=self._on_keyboard_down)


    def _keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self._on_keyboard_down)
        self.keyboard = None


    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'n' or keycode[1] == 'т':
            self.name_text_input.focus = True
        elif keycode[1] == 'k' or keycode[1] == 'л':
            self.keywords_text_input.focus = True
        elif keycode[1] == 'f' or keycode[1] == 'а':
            self.file_or_dir_button.file_button.state = 'down'
        elif keycode[1] == 'd' or keycode[1] == 'в':
            self.file_or_dir_button.dir_button.state = 'down'
        elif keycode[1] == 'escape':
            self.escape()
        return True


    def add_new_record(self, record_name: str, keywords_str: str, is_file: bool) -> bool:
        if is_record_exist(record_name):
            send_record_exist_msg()
            return False

        # Name and keywords are separated by spaces and used as keywords of record(file/dir)
        full_keywords_str = record_name + ' ' + keywords_str
        keywords = get_keywords_from_string(full_keywords_str)

        create_record(record_name, keywords, is_file, self.scr_manager.current_dir)

        print(f"Keywords: {keywords}")
        print(f"Is file: {is_file}")
        self.escape()

        self.name_text_input.text = ""
        self.keywords_text_input.text = ""

        return True


    def escape(self):
        open_window(self.scr_manager, MAIN_WINDOW)