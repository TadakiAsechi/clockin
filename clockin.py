# coding: utf-8

import tkinter as tk
import logic
import routing as route

# Tkクラスを作成
root = tk.Tk()
root.geometry("500x300")

# タイトルを作成
root.title("clockin")

# 挨拶を作成
greeting = logic.greet()
label = tk.Label(root, text=greeting)
label.pack()

# 出勤ボタンを作成
clock_in = tk.Button(root, text="出勤", command=route.clock_in)
clock_in.place(x=100, y=120)

# 退勤ボタンを作成
clock_out = tk.Button(root, text="退勤", command=route.clock_out)
clock_out.place(x=300, y=120)

# 表示
root.mainloop()
