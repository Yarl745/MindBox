from random import randint

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import ScreenManager, WipeTransition
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput

from mindbox.jarvis_db import is_record_exist, create_record
from mindbox.widgets.data_rv import DataRV
from mindbox.widgets.textinputs import TextButton
from mindbox.windows.create_window import CreateWindow
from mindbox.windows.main_window import MainWindow
from mindbox.windows.update_window import UpdateWindow




class WindowManager(ScreenManager):
	MODE_NORMAL = 'MODE_NORMAL'
	MODE_UPDATE = 'MODE_UPDATE'
	MODE_DELETE = 'MODE_DELETE'
	# MODE_SEARCH = 'MODE_SEARCH'


	# def __new__(cls, *args, **kwargs):
	# 	if not is_record_exist('ROOT'):
	# 		create_record('ROOT', [], False, 'ROOT')


	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.current_record = None
		self.mode = self.MODE_NORMAL
		self.deleting_records = dict()

		self.__current_dir = 'ROOT'
		self.__current_search = None
		self.__is_search = False


	@property
	def current_search(self):
		return self.__current_search


	@current_search.setter
	def current_search(self, search: str):
		self.__current_search = search
		self.__is_search = True
		self.ids.main_window.create_button.disabled = True


	@property
	def current_dir(self):
		return self.__current_dir


	@current_dir.setter
	def current_dir(self, dir: str):
		self.__current_dir = dir
		self.__current_search = None
		self.__is_search = False
		self.ids.main_window.create_button.disabled = False


	@property
	def is_search(self):
		return self.__is_search


	@is_search.setter
	def is_search(self, search: bool):
		if search is False:
			self.ids.main_window.create_button.disabled = False
		self.__is_search = search


class MindBoxApp(App):
	def build(self):
		return WindowManager()


if __name__ == '__main__':
	MindBoxApp().run()