import logic
from conf import Message, APP


def clock_in():
    print("you're in!")
    sbj, msg = logic.get_message(Message.IN)
    logic.send_email(sbj, msg)
    print("done!")


def clock_out():
    print("you are out!")
    sbj, msg = logic.get_message(Message.OUT)
    logic.send_email(sbj, msg)
    print("Goodbye!")


def apply_off():
    print("I\'m applying off !")
    sbj, msg = logic.get_message(Message.OFF)
    logic.send_email(sbj, msg)
    print("applied!")


def change_app(self, app):
    match app:
        case APP.MAIN:
            self.frame.tkraise()
        case APP.OFF:
            self.frame_applyoff.tkraise()
