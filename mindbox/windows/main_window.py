from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from mindbox.jarvis_db import find_records_by_keywords, get_exist_keywords, \
    get_children, get_parent, is_record_exist, first_db_create, big_delete, del_records_from_parent, \
    del_record_from_parent
from mindbox.open_commands import open_window

from mindbox.string_operation import get_keywords_from_string
from mindbox.windows.window_names import CREATE_WINDOW, UPDATE_WINDOW


class MainWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        # First DB create
        if not is_record_exist('ROOT'):
            first_db_create()

        self.search_text_input = ObjectProperty()
        self.data_rv = ObjectProperty()
        self.scr_manager = ObjectProperty()
        self.label_mode = ObjectProperty()
        self.is_agree_to_del_msg = ObjectProperty()
        self.create_button = ObjectProperty()

        self.data_rv_record_names = get_children('ROOT')


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
        if keycode[1] == 's' or keycode[1] == 'ы':
            # show_search_text_input()
            self.search_text_input.focus = True
        elif keycode[1] == 'c' or keycode[1] == 'с':
            self.goto_create_window()
        elif keycode[1] == 'u' or keycode[1] == 'г':
            self.small_update()
            self.set_mode_update()
        elif keycode[1] == 'd' or keycode[1] == 'в':
            self.small_update()
            self.set_mode_delete()
        elif keycode[1] == 'n' or keycode[1] == 'т':
            self.small_update()
            self.set_mode_normal()
        elif keycode[1] == 'numpaddecimal':
            count_deleting = len(self.scr_manager.deleting_records)
            if self.scr_manager.mode == self.scr_manager.MODE_DELETE and count_deleting > 0:
                self.is_agree_to_del_msg.count_deleting = count_deleting
                self.is_agree_to_del_msg.open()
        elif keycode[1] == 'escape':
            if self.scr_manager.current_search is not None:
                self.scr_manager.is_search = False
                self.big_update()
            elif self.scr_manager.mode == self.scr_manager.MODE_NORMAL and self.scr_manager.current_dir != 'ROOT':
                parent_name = get_parent(self.scr_manager.current_dir)
                self.scr_manager.current_dir = parent_name
                self.big_update()
            elif self.scr_manager.mode == self.scr_manager.MODE_DELETE:
                self.small_update()
        elif keycode[1] == 'enter':
            if len(self.search_text_input.text) > 0:
                self.search_records(self.search_text_input.text)
        return True


    def set_mode_normal(self):
        self.label_mode.text = 'Normal'
        self.label_mode.color = (1, 1, 1, 1)
        self.scr_manager.mode = self.scr_manager.MODE_NORMAL


    def set_mode_delete(self):
        self.label_mode.text = 'Delete'
        self.label_mode.color = (.7, 0, 0, 1)
        self.scr_manager.mode = self.scr_manager.MODE_DELETE


    def set_mode_update(self):
        self.label_mode.text = 'Update'
        self.label_mode.color = (0, .7, 0, 1)
        self.scr_manager.mode = self.scr_manager.MODE_UPDATE


    def big_update(self):
        self.scr_manager.deleting_records.clear()

        if self.scr_manager.is_search:
            self.search_records(self.scr_manager.current_search)

        else:
            if not is_record_exist(self.scr_manager.current_dir):
                self.scr_manager.current_dir = 'ROOT'

            child_names = get_children(self.scr_manager.current_dir)

            self.data_rv_record_names = child_names
            self.data_rv.data = [{'text': record_name} for record_name in self.data_rv_record_names]

            self.data_rv.refresh_from_data()
            self.data_rv.refresh_from_viewport()
        

    def small_update(self):
        self.scr_manager.deleting_records.clear()
        self.data_rv.data = [{'text': record_name} for record_name in self.data_rv_record_names]

        self.data_rv.refresh_from_data()
        self.data_rv.refresh_from_viewport()


    def search_records(self, query: str):
        keywords = get_keywords_from_string(query)
        exist_keywords = get_exist_keywords(keywords)

        self.scr_manager.current_search = query

        if len(exist_keywords) > 0:
            found_records = find_records_by_keywords(exist_keywords)
            self.show_records(found_records)
            self.search_text_input.hint_text = 'Search...'
        else:
            self.search_text_input.text = ''
            self.search_text_input.hint_text = 'Undefined keywords...'
            self.show_records([])


    def show_records(self, record_names: list):
        self.data_rv_record_names = record_names
        self.data_rv.data = [{"text": record_name} for record_name in self.data_rv_record_names]

        self.data_rv.refresh_from_data()
        self.data_rv.refresh_from_viewport()


    def del_records(self) -> bool:
        if self.scr_manager.is_search:
            for children_name in self.scr_manager.deleting_records.keys():
                del_record_from_parent(children_name)
        else:
            # Del selected children from parent.
            # Use list(...) -> dict().keys() don't give list object.
            del_records_from_parent(list(self.scr_manager.deleting_records))

        for deleting_record_name in self.scr_manager.deleting_records.keys():
            big_delete(deleting_record_name)
            self.data_rv_record_names.remove(deleting_record_name)

        self.set_mode_normal()

        # Update Main window after deleting records.
        self.big_update()

        return True


    def goto_create_window(self):
        open_window(self.scr_manager, CREATE_WINDOW)


    def goto_update_window(self):
        open_window(self.scr_manager, UPDATE_WINDOW)