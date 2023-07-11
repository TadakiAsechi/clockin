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
        self.frame_checkmail = ttk.Frame(self.root)
        self.frame_checkmail.grid(row=0, column=0, sticky="nsew", pady=20)


    def show_window(self):
        # 後で各パーツをクラス化する

        # ---メインフレーム---
        # 挨拶を作成
        greeting = logic.greet()

        # ウィジェットの作成
        label_main = ttk.Label(self.frame, text=greeting)
        # entry_main = ttk.Entry(self.frame)
        clock_in = tk.Button(self.frame, text="出勤", command=route.clock_in)
        clock_out = tk.Button(self.frame, text="退勤", command=route.clock_out)
        clock_off = tk.Button(self.frame, text="有給申請", command=lambda: route.change_app(self, APP.OFF))

        # ウィジェットの設置
        label_main.pack()
        # entry_main.pack()
        clock_in.place(x=100, y=100)
        clock_out.place(x=330, y=100)
        clock_off.place(x=310, y=200)

        # ---有給申請フレーム---
        # ウィジェットの作成
        label_applyoff = ttk.Label(self.frame_applyoff, text="有給休暇を申請します")
        label_from = ttk.Label(self.frame_applyoff, text="から")
        label_to = ttk.Label(self.frame_applyoff, text="まで")
        # TODO: 任意で複数の日付を選択できるように変更（+ボタンでカレンダーを3~4個まで追加？）
        date1 = DateEntry(self.frame_applyoff, width=12, background="blue", foreground="white", borderwidth=2)
        date2 = DateEntry(self.frame_applyoff, width=12, background="blue", foreground="white", borderwidth=2)
        dates = [date1, date2]
        button_main = tk.Button(
            self.frame_applyoff, text="戻る",
            command=lambda: route.change_app(self, APP.MAIN))
        button_applyoff = tk.Button(
            self.frame_applyoff, text="申請する",
            command=lambda: route.apply_off(self, dates))

        # ウィジェットを配置
        label_applyoff.pack()
        date1.place(x=40, y=100)
        label_from.place(x=170, y=100)
        date2.place(x=210, y=100)
        label_to.place(x=340, y=100)
        button_applyoff.place(x=380, y=95)
        button_main.place(x=400, y=200)




        # frameを前面にする
        self.frame.tkraise()

        # 表示
        self.root.mainloop()


if __name__=="__main__":
    window = Window()
    window.show_window()