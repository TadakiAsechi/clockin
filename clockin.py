# coding: utf-8

import tkinter as tk
import test_logic as logi
import routing as route

# Tkクラスを作成
root = tk.Tk()
root.geometry("300x200")

# タイトルを作成
root.title("clockin")

# 出勤ボタンを作成
clock_in = tk.Button(root, text="出勤", command=route.clock_in)
clock_in.place(x=40, y=30)

# 退勤ボタンを作成
clock_out = tk.Button(root, text="退勤", command=route.clock_out)
clock_out.place(x=160, y=30)

# 表示
root.mainloop()
