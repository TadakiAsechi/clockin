# coding: utf-8

import tkinter as tk
import tkinter.ttk as ttk

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

    def show_window(self):

        # ---メインフレーム---
        # 挨拶を作成
        greeting = logic.greet()
        # ウィジェットの作成・設置
        label_main = ttk.Label(self.frame, text=greeting)
        label_main.pack()
        # entry_main = ttk.Entry(self.frame)
        # entry_main.pack()

        # 出勤ボタンを作成
        clock_in = tk.Button(self.frame, text="出勤", command=route.clock_in)
        clock_in.place(x=100, y=120)

        # 退勤ボタンを作成
        clock_out = tk.Button(self.frame, text="退勤", command=route.clock_out)
        clock_out.place(x=300, y=120)

        # 有給申請ボタンを作成
        clock_off = tk.Button(self.frame, text="有給申請", command=lambda:route.change_app(self, APP.OFF))
        clock_off.place(x=300, y=220)

        # ---有給申請フレーム---
        # ウィジェットの作成・設置
        label_applyoff = ttk.Label(self.frame_applyoff, text="有給休暇を申請します")
        entry_applyoff = ttk.Entry(self.frame_applyoff)
        label_applyoff.pack()
        entry_applyoff.pack()

        # 有給申請フレームにボタンを作成
        clock_main = tk.Button(self.frame_applyoff, text="戻る", command=lambda:route.change_app(self, APP.MAIN))
        clock_main.place(x=300, y=220)

        # frameを前面にする
        self.frame.tkraise()

        # 表示
        self.root.mainloop()


if __name__=="__main__":
    window = Window()
    window.show_window()