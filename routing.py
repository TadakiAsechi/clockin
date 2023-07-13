import string
import os

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


def apply_off(self, dates):
    print("I\'m applying off !")
    origin_sbj, origin_msg = logic.get_message(Message.OFF)
    boss = os.environ["CLOCKIN_BOSS"]
    me = os.environ["CLOCKIN_ME"]
    term = "\n".join(date_entry.get() for date_entry in dates)
    self.mail_sbj = string.Template(origin_sbj).safe_substitute({"me": me})
    self.mail_msg = string.Template(origin_msg).safe_substitute({"boss": boss, "me": me, "term": term})

    self.create_checktext_widget()

    change_app(self, APP.CHECK)


def check_text(self):

    logic.send_email(self.mail_sbj, self.mail_msg)

    pass


def change_app(self, app):
    match app:
        case APP.MAIN:
            self.frame.tkraise()
        case APP.OFF:
            self.frame_applyoff.tkraise()
        case APP.CHECK:
            self.frame_checktext.tkraise()

