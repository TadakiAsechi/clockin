# coding: utf-8

import tkinter as tk
import test_logic as logi

root = tk.Tk()
root.geometry("250x100")

run_button = tk.Button(root, text="Run", command=logi.hello)
run_button.place(x=90,y=30)

root.mainloop()
