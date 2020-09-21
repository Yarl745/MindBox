from kivy.properties import BooleanProperty
from kivy.uix.popup import Popup


def send_record_exist_msg():
    print('Message is exist')

class IsAgreeToDelMsg(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_agree = BooleanProperty(False)