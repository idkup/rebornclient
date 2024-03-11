import tkinter.ttk as ttk
from PIL import ImageTk


class InteractableIcon(ttk.Button):
    def __init__(self, parent, data, display, cache):
        self.cache = cache
        self.data = data
        self.display = display
        self.icon = ImageTk.PhotoImage(file=f"graphics/{self.data['species']}.png")
        super().__init__(parent, image=self.icon, command=self.display_info)

    def display_info(self):
        self.display.config(image=self.icon, text=str(self), compound='top')

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
