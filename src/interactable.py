import tkinter.ttk as ttk
import os
from pathlib import Path
from PIL import ImageTk
import sys


def get_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return filename


class InteractableIcon(ttk.Button):
    def __init__(self, parent, app, data, display, export):
        self.api = app.api
        self.app = app
        self.cache = app.cache
        self.data = data
        self.display = display
        self.export = export
        iconpath = get_path(f"graphics/{self.data['species']}.png")
        self.icon = ImageTk.PhotoImage(file=iconpath)
        super().__init__(parent, image=self.icon, command=self.on_click)

    def display_info(self):
        self.display.config(image=self.icon, text=str(self), compound='top')

    def export_and_query(self):
        d = self.data
        internal_id = d['id']
        if self.api.export_call(internal_id) != 200:
            self.app.refresh()
            self.app.log.config(text="Something went wrong.")
            return
        fn = Path(self.app.to_game_path)
        fn.touch(exist_ok=True)
        fp = get_path(self.app.to_game_path)
        export_str = f"{d['name']}|{d['species']}|{d['lvl']}|{d['ability']}|{d['nature']}|{d['moves']}|{d['ivs']}|{d['evs']}|{d['shiny']}|{d['ot']}|{d['gender']}|{d['caughtloc']}|{d['form']}\n"
        with open(fp, "a") as f:
            f.write(export_str)
            f.close()
        self.app.refresh()
        self.display.config(image=self.icon, text=f"{d['name']} downloaded from box!\nImport from Tools menu!")
        for i in self.export.winfo_children():
            i.destroy()

    def on_click(self):
        self.display_info()
        for i in self.export.winfo_children():
            i.destroy()
        button = ttk.Button(self.export, text="Export", command=self.export_and_query)
        button.pack()

    def __str__(self):
        d = self.data
        try:
            abilstring = self.cache.abilities[str(d['ability'])]
        except KeyError:
            abilstring = "Unrecognized"
        movestring = ""
        for move in d['moves'].split(','):
            if move != '0':
                try:
                    movestring += f"- {self.cache.moves[move]}\n"
                except KeyError:
                    movestring += "- Unrecognized\n"
        return f"""{d['name']} ({'Shiny ' if d['shiny'] else ''}{d['speciesname']} Lvl {d['lvl']})
OT: {d['ot']}
{abilstring}
{movestring}"""
