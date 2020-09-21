from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from mindbox.jarvis_db import is_record_exist, create_record, get_record_keywords, create_empty_record, copy_record_data, \
    del_record, change_record_keywords, del_record_from_keywords, add_record_to_keywords
from mindbox.widgets.messages import send_record_exist_msg
from mindbox.open_commands import open_window
from mindbox.string_operation import get_keywords_from_string
from mindbox.transformer import transform_list_to_truedict
from mindbox.windows.window_names import MAIN_WINDOW


class UpdateWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name_text_input = ObjectProperty()
        self.keywords_text_input = ObjectProperty()
        self.scr_manager = ObjectProperty()
        self.keyboard = None


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
        elif keycode[1] == 'escape':
            self.escape()
        return True


    def upload_record_data(self):
        record_name = self.scr_manager.current_record
        record_keywords = get_record_keywords(record_name)

        self.name_text_input.text = record_name
        self.keywords_text_input.text = ' '.join(record_keywords)


    def update_record(self) -> bool:
        old_record_name = self.scr_manager.current_record
        old_record_keywords = get_record_keywords(old_record_name)

        new_record_name = self.name_text_input.text
        new_record_keywords = transform_list_to_truedict(get_keywords_from_string(self.keywords_text_input.text))

        if is_record_exist(new_record_name) and new_record_name != old_record_name:
            send_record_exist_msg()
            return False
        elif new_record_name != old_record_name:
            create_empty_record(new_record_name)

        if new_record_name != old_record_name:
            keywords_from_old_name = transform_list_to_truedict(get_keywords_from_string(old_record_name))
            keywords_from_new_name = transform_list_to_truedict(get_keywords_from_string(new_record_name))

            old_record_keywords.update(keywords_from_old_name)
            new_record_keywords.update(keywords_from_new_name)

            copy_record_data(from_record=old_record_name, to_record=new_record_name)
            del_record(old_record_name)

            change_record_keywords(new_record_name, new_record_keywords)

            del_record_from_keywords(record_name=old_record_name, from_keywords=old_record_keywords)

            add_record_to_keywords(record_name=new_record_name, to_keywords=new_record_keywords)

        else:
            record_name = old_record_name = new_record_name

            old_keywords = list(old_record_keywords.keys())

            unchanged_records = dict()

            for old_record_keyword in old_keywords:
                if old_record_keyword in new_record_keywords:
                    del old_record_keywords[old_record_keyword]
                    del new_record_keywords[old_record_keyword]
                    unchanged_records.update({old_record_keyword: True})

            del_record_from_keywords(record_name=record_name, from_keywords=old_record_keywords)

            add_record_to_keywords(record_name=record_name, to_keywords=new_record_keywords)

            keywords_from_record_name = transform_list_to_truedict(get_keywords_from_string(record_name))
            new_record_keywords.update(keywords_from_record_name)
            new_record_keywords.update(unchanged_records)

            change_record_keywords(record_name, new_record_keywords)

        self.escape()

        return True


    def add_new_record(self, record_name: str, keywords_str: str, is_file: bool) -> bool:
        if is_record_exist(record_name):
            # send_record_exist_msg()
            return False

        # Name and keywords are separated by spaces and used as keywords of record(file/dir)
        full_keywords_str = record_name + ' ' + keywords_str
        keywords = get_keywords_from_string(full_keywords_str)

        create_record(record_name, keywords, is_file, "PARENT")

        print(f"Keywords: {keywords}")
        print(f"Is file: {is_file}")
        self.escape()

        self.name_text_input.text = ""
        self.keywords_text_input.text = ""

        return True


    def escape(self):
        open_window(self.scr_manager, MAIN_WINDOW)