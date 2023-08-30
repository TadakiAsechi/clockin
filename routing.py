# coding: utf-8

import string
import os
from datetime import datetime

from tkinter import messagebox

import logic
from conf import Message, APP, MailResult


def clock_in(self):

    time = logic.get_quartered_time()
    origin_sbj, origin_msg = logic.get_message(Message.IN)

    # メッセージに文言を埋め込む
    self.mail_sbj = string.Template(origin_sbj).safe_substitute({"me": self.me})
    self.mail_msg = string.Template(origin_msg).safe_substitute({"boss": self.boss, "me": self.me, "time": time})

    self.create_checktext_widget(app=APP.MAIN)
    self.frame_checktext.tkraise()


def clock_out(self):

    time = logic.get_quartered_time()
    origin_sbj, origin_msg = logic.get_message(Message.OUT)

    # メッセージに文言を埋め込む
    self.mail_sbj = string.Template(origin_sbj).safe_substitute({"me": self.me})
    self.mail_msg = string.Template(origin_msg).safe_substitute({"boss": self.boss, "me": self.me, "time": time})

    self.create_checktext_widget(app=APP.MAIN)
    self.frame_checktext.tkraise()


def apply_off(self, dates):
    # メッセージに埋め込む文言を準備
    origin_sbj, origin_msg = logic.get_message(Message.OFF)
    term = "\n".join(date_entry.get() for date_entry in dates)

    # メッセージに文言を埋め込む
    self.mail_sbj = string.Template(origin_sbj).safe_substitute({"me": self.me})
    self.mail_msg = string.Template(origin_msg).safe_substitute({"boss": self.boss, "me": self.me, "term": term})

    # 本文確認画面にウィジェットを配置し遷移する
    self.create_checktext_widget(app=APP.OFF)
    self.frame_checktext.tkraise()


def send_mail(self, sbj, msg):
    """
    受け取った修正済みのメッセージでメール送信ロジックを呼び出す。

    :param self:
    :param sbj:
    :param msg:
    :return:
    """
    ret_val = logic.send_email(sbj, msg)
    message = ret_val.value[1]
    self.mail_sbj = ""
    self.mail_msg = ""
    messagebox.showinfo("送信結果", message)

    if ret_val == MailResult.SUCCESS:
        #TODO:  成功時はExcelに記録を行う
        pass
    else:
        pass

    #メイン画面に戻る
    change_app(self, APP.MAIN)


def change_app(self, app):
    """
    受け取ったアプリケーションタイプに合わせて単純な画面遷移を行う

    :param self:
    :param app:
    :return:
    """
    match app:
        case APP.MAIN:
            self.frame.tkraise()
        case APP.OFF:
            self.frame_applyoff.tkraise()
        case APP.CHECK:
            self.frame_checktext.tkraise()

