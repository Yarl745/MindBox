from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.textinput import TextInput

# from mindbox.main import WindowManager
from mindbox.jarvis_db import record_is_file


class TextButton(TextInput):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.main_window = self.parent.parent.parent.parent
            self.scr_manager = self.main_window.parent

            record_name = self.text

            if self.scr_manager.mode == self.scr_manager.MODE_NORMAL:
                if record_is_file(record_name):
                    print(f"record - {record_name} - is file")
                else:
                    self.scr_manager.current_dir = record_name
                    self.main_window.big_update()

            elif self.scr_manager.mode == self.scr_manager.MODE_DELETE:
                if record_name in self.scr_manager.deleting_records:
                    self.scr_manager.deleting_records.pop(record_name)
                    self.background_color = (0, 0, 0, 1)
                else:
                    self.scr_manager.deleting_records.update({record_name: True})
                    self.background_color = (.5, 0, 0, 1)

                # self.main_window.data_rv.refresh_view_attrs()

                print(self.scr_manager.deleting_records)

            elif self.scr_manager.mode == self.scr_manager.MODE_UPDATE:
                self.scr_manager.current_record = record_name
                self.main_window.goto_update_window()

            touch.grab(self)
            return True
        else:
            return super().on_touch_down(touch)


class CustomTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(focus=self.on_focus)


    def on_focus(self, instance, value):
        pass
