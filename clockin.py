# coding: utf-8

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

        self.mail_msg = ""
        self.mail_sbj = ""


    def add_date_entry(self):
        # Check if we already have the maximum number of date pickers
        if len(self.date_entries) < 5:
            # Create a new date picker
            date_entry = DateEntry(self.frame_applyoff, width=12, background="blue", foreground="white", borderwidth=2)
            date_entry.place(x=40, y=self.date_entry_y)
            # Increment y position for next date picker
            self.date_entry_y += 30

            # Add the date picker to the list
            self.date_entries.append(date_entry)

    def create_main_frame_widgets(self):
        """Create widgets for the main frame."""
        # ウィジェットの作成
        self.greeting_var.set(logic.greet())
        label_main = ttk.Label(self.frame, textvariable=self.greeting_var)
        clock_in = tk.Button(self.frame, text="出勤", command=route.clock_in)
        clock_out = tk.Button(self.frame, text="退勤", command=route.clock_out)
        clock_off = tk.Button(self.frame, text="有給申請", command=lambda: route.change_app(self, APP.OFF))

        # ウィジェットの設置
        label_main.pack()
        clock_in.pack()
        clock_out.pack()
        clock_off.pack()

    def create_applyoff_frame_widgets(self):
        """Create widgets for the applyoff frame."""
        # ウィジェットの作成
        label_applyoff = ttk.Label(self.frame_applyoff, text="有給休暇を申請します")
        button_main = tk.Button(
            self.frame_applyoff, text="戻る",
            command=lambda: route.change_app(self, APP.MAIN))
        button_applyoff = tk.Button(
            self.frame_applyoff, text="申請する",
            command=lambda: route.apply_off(self, self.date_entries))

        # Add date picker addition button
        add_date_entry_button = tk.Button(self.frame_applyoff, text="+", command=self.add_date_entry)
        add_date_entry_button.pack()

        # Create initial date entry
        self.add_date_entry()

        # ウィジェットを配置
        label_applyoff.pack()
        button_applyoff.pack()
        button_main.pack()

    def create_checktext_widget(self):
        label_sbj = ttk.Label(self.frame_checktext, text="sbj:" + self.mail_sbj)
        label_msg = ttk.Label(self.frame_checktext, text="msg:" + self.mail_msg)

        label_sbj.pack()
        label_msg.pack()

    def show_window(self):
        """Show the window and create the widgets."""
        self.create_main_frame_widgets()
        self.create_applyoff_frame_widgets()

        # frameを前面にする
        self.frame.tkraise()

        # 表示
        self.root.mainloop()


if __name__ == "__main__":
    window = Window()
    window.show_window()