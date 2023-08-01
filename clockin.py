# coding: utf-8

import os
import time
from datetime import datetime
import threading

import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import DateEntry

import logic
import routing as route
from conf import APP


class Window:
    def __init__(self):
        # メインウィンドウを設定
        self.root = tk.Tk()
        self.root.geometry("500x300")
        self.root.title("clockin")

        # メインウィンドウのグリッドを1x1にする
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # メインフレーム
        self.frame = ttk.Frame(self.root)
        self.frame.grid(row=0, column=0, sticky="nsew", pady=20)

        # 有給申請画面
        self.frame_applyoff = ttk.Frame(self.root)
        self.frame_applyoff.grid(row=0, column=0, sticky="nsew", pady=20)

        # 本文確認画面
        self.frame_checktext = ttk.Frame(self.root)
        self.frame_checktext.grid(row=0, column=0, sticky="nsew", pady=20)

        self.greeting_var = tk.StringVar()

        # List to keep track of the date pickers
        self.date_entries = []

        # Initialize y position for date picker placement
        self.date_entry_y = 100

        self.boss = os.environ["CLOCKIN_BOSS"]
        self.me = os.environ["CLOCKIN_ME"]

        self.mail_msg = ""
        self.mail_sbj = ""

        self.last_message_time = None
        self.thread = threading.Thread(target=self.update_message)
        self.thread.start()

    def add_date_entry(self):
        """最大5個まで、日時選択ウィジェットを追加する

        :return:
        """
        # 日時選択ウィジェットのリストの長さを確認する
        if len(self.date_entries) < 5:

            # 日時選択ウィジェットを作成・設置
            date_entry = DateEntry(self.frame_applyoff, width=12, background="blue", foreground="white", borderwidth=2)
            date_entry.place(x=40, y=self.date_entry_y)

            # 次のウィジェットの位置を下にずらす
            self.date_entry_y += 30

            # 日時選択ウィジェットをリストに入れる
            self.date_entries.append(date_entry)

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def create_main_frame_widgets(self):
        """メインフレームにウィジェットを配置する。

        :return:
        """
        # ウィジェットの作成
        self.greeting_var.set(logic.generate_message())
        label_main = ttk.Label(self.frame, wraplength=350, textvariable=self.greeting_var)
        self.last_message_time = datetime.now()

        clock_in = tk.Button(self.frame, text="出勤", command=lambda: route.clock_in(self))
        clock_out = tk.Button(self.frame, text="退勤", command=lambda: route.clock_out(self))
        clock_off = tk.Button(self.frame, text="有給申請", command=lambda: route.change_app(self, APP.OFF))

        # ウィジェットの設置
        label_main.pack()
        clock_in.pack()
        clock_out.pack()
        clock_off.pack()

    def create_applyoff_frame_widgets(self):
        """有給申請フレームにウィジェットを配置する

        :return:
        """
        # 日時選択ウィジェット追加ボタンを作成・配置
        add_date_entry_button = tk.Button(self.frame_applyoff, text="+", command=self.add_date_entry)
        add_date_entry_button.pack()

        # 一つ目の日時選択ウィジェットを配置する
        self.add_date_entry()

        # ウィジェットの作成
        label_applyoff = ttk.Label(self.frame_applyoff, text="有給休暇を申請します")
        button_main = tk.Button(
            self.frame_applyoff, text="戻る",
            command=lambda: route.change_app(self, APP.MAIN))
        button_applyoff = tk.Button(
            self.frame_applyoff, text="申請する",
            command=lambda: route.apply_off(self, self.date_entries))

        # ウィジェットを配置
        label_applyoff.pack()
        button_applyoff.pack()
        button_main.pack()

    def create_checktext_widget(self, app):
        self.clear_frame(self.frame_checktext)

        button_main = tk.Button(
            self.frame_checktext, text="戻る",
            command=lambda: route.change_app(self, app))
        button_send = tk.Button(
            self.frame_checktext, text="送信",
            command=lambda: route.send_mail(self,
                                            text_sbj.get("1.0", "end").strip(),
                                            text_msg.get("1.0", "end").strip()))

        # ------------------------- #
        # 件名用のテキストウィジェットを作成 #
        # ------------------------- #
        # テキストウィジェットを作る
        text_sbj = tk.Text(self.frame_checktext, wrap=tk.WORD, height=1)
        text_sbj.insert(tk.END, self.mail_sbj)

        # ------------------------- #
        # 本文用のテキストフレームを作成 #
        # ------------------------- #
        # フレームをインスタンス化
        text_frame = ttk.Frame(self.frame_checktext)
        # スクロールバーを作成
        scrollbar = tk.Scrollbar(text_frame)
        # Create a Text widget with a vertical scrollbar
        text_msg = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, height=15)
        text_msg.insert(tk.END, self.mail_msg)
        text_msg.pack()
        # Configure the scrollbar to scroll the Text widget
        scrollbar.config(command=text_msg.yview)

        # ------------------------- #
        #  フレーム・ウィジェットを配置  #
        # ------------------------- #
        text_sbj.grid(row=0, column=0, sticky='w')
        text_frame.grid(row=1, column=0, sticky='nsew')
        text_msg.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        button_main.grid(row=2, column=0, pady=10)
        button_send.grid(row=3, column=0)

        # Configure grid to be flexible
        self.frame_checktext.grid_columnconfigure(0, weight=1)
        self.frame_checktext.grid_rowconfigure(1, weight=1) # Only the text_frame should expand

    def show_window(self):

        self.create_main_frame_widgets()
        self.create_applyoff_frame_widgets()

        # frameを前面にする
        self.frame.tkraise()

        # 表示
        self.root.mainloop()

    def update_message(self):
        while True:
            if self.last_message_time is not None and (datetime.now() - self.last_message_time).seconds >= 600:
                self.greeting_var.set(logic.generate_message())
                print(self.greeting_var)
                self.last_message_time = datetime.now()

            time.sleep(60)


if __name__ == "__main__":
    window = Window()
    window.show_window()
