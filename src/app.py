from api import WebServerAccess
from cache import Cache
from interactable import InteractableIcon
import math
import tkinter.ttk as ttk
from ttkthemes import ThemedTk


class BoxApp:
    def __init__(self):
        self.api = WebServerAccess()
        self.cache = Cache()
        self.data = {}
        self.root = ThemedTk(theme="arc")
        self.root.title("Global Box")
        main_frame = ttk.Frame(self.root, height=720, width=960)
        main_frame.pack()
        self.left_frame = ttk.Frame(main_frame)
        self.left_frame.place(relx=0.05, rely=0.05, relheight=0.9, relwidth=0.6)
        right_frame = ttk.Frame(main_frame)
        right_frame.place(relx=0.71, rely=0.05, relheight=0.9, relwidth=0.24)
        separator = ttk.Separator(main_frame, orient="vertical")
        separator.place(relx=0.68, rely=0.05, relheight=0.9, relwidth=0.03)
        refresh_button = ttk.Button(right_frame, text="Refresh", command=self.refresh)
        refresh_button.place(relx=0.35, rely=0.05, relheight=0.05, relwidth=0.3)
        self.log = ttk.Label(right_frame, text="Welcome!")
        self.log.place(relx=0.1, rely=0.2, relheight=0.7, relwidth=0.8)
        self.root.mainloop()

    def refresh(self):
        raw = self.api.read_call()
        for mon in raw:
            mon_id = mon.pop("id")
            self.data[mon_id] = mon
        self.log.config(text="Refresh successful")
        self.update_box()

    def update_box(self):
        avail_dict = {k: v for k, v in self.data.items()if v["available"] == 1}
        display_width = math.ceil(math.sqrt(len(avail_dict)))

        for i in self.left_frame.winfo_children():
            i.destroy()

        p = 0
        q = display_width
        for r in range(q):
            for c in range(q):
                key = list(avail_dict.keys())[p]
                InteractableIcon(self.left_frame, self.data[key], self.log, self.cache).grid(row=r, column=c)
                p += 1
                if p == len(avail_dict):
                    return



