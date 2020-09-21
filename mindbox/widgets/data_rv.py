from random import randint

from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

from mindbox.jarvis_db import get_children


class DataRV(RecycleView):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		child_names = get_children('ROOT')
		self.data = [{'text': record_name} for record_name in child_names]
