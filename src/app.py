import asyncio
from api import WebServerAccess
from cache import Cache
from interactable import InteractableIcon
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from async_tkinter_loop import async_handler, async_mainloop


class BoxApp:
    def __init__(self):
        self.api = WebServerAccess()
        self.cache = Cache()
        self.data = {}
        self.to_game_path = "to_game.txt"

        self.root = ThemedTk(theme="arc")
        self.root.title("Global Box")
        main_frame = ttk.Frame(self.root, height=720, width=960)
        main_frame.pack()
        self.left_frame = ttk.Frame(main_frame)
        self.left_frame.place(relx=0.05, rely=0.05, relheight=0.9, relwidth=0.6)
        right_frame = ttk.Frame(main_frame)
        right_frame.place(relx=0.63, rely=0.05, relheight=0.9, relwidth=0.32)
        sep1 = ttk.Separator(main_frame, orient="vertical")
        sep1.place(relx=0.60, rely=0, relheight=1, relwidth=0.03)
        refresh_button = ttk.Button(right_frame, text="Refresh", command=self.refresh)
        refresh_button.place(relx=0.35, rely=0.05, relheight=0.05, relwidth=0.3)
        self.log = ttk.Label(right_frame, text="Welcome!")
        self.log.place(relx=0.1, rely=0.2, relheight=0.5, relwidth=0.8)
        self.export_frame = ttk.Frame(right_frame)
        self.export_frame.place(relx=0.1, rely=0.73, relwidth=0.8, relheight=0.2)
        sep2 = ttk.Separator(right_frame, orient="horizontal")
        sep2.place(relx=0, rely=0.6, relheight=0.03, relwidth=1)
        async_mainloop(self.root)

    def refresh(self):
        raw = self.api.read_call()
        for mon in raw:
            self.data[mon['id']] = mon
        self.log.config(image="", text="Refresh successful")
        self.update_box()

    def update_box(self):
        avail_dict = {k: v for k, v in self.data.items()if v["available"] == 1}

        for i in self.left_frame.winfo_children():
            i.destroy()

        canvas = tk.Canvas(self.left_frame, width=540, height=600)
        canvas.grid(row=0, column=0)
        scroll = ttk.Scrollbar(self.left_frame, orient="vertical", command=canvas.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        box_frame = ttk.Frame(canvas)

        p = 0
        for i in range(len(avail_dict)):
            key = list(avail_dict.keys())[p]
            InteractableIcon(box_frame, self, self.data[key], self.log, self.export_frame).grid(row=i//6, column=i % 6)
            p += 1

        canvas.create_window((0, 0), window=box_frame, anchor="nw")
        box_frame.update_idletasks()

        canvas.config(yscrollcommand=scroll.set, scrollregion=canvas.bbox(tk.ALL))



