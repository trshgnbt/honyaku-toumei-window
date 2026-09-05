#共通で使えるかもしれないボタン
import tkinter as tk

class CloseButton(tk.Button):
    """× で閉じるボタン。command未指定ならmaster.destroyを使う"""
    def __init__(self, master, command=None, **kwargs):
        default_style = {
            "text": " × ",
            "fg": "white",
            "bg": "#2c3e50",
            "activebackground": "#e74c3c",
            "activeforeground": "white",
            "bd": 3,
            "font": ("Arial", 12),
        }
        default_style.update(kwargs)
        super().__init__(master, command=command or master.destroy, **default_style)

class DragHandle(tk.Label):
    """掴んで移動するためのラベル。バインド先はtarget_window(省略時はmaster)"""
    def __init__(self, master, target_window=None, text=" ☰ 掴んで移動 ", **kwargs):
        default_style = {
            "fg": "white",
            "bg": "#34495e",
            "bd": 3,
            "relief": "raised",
            "font": ("Arial", 10),
        }
        default_style.update(kwargs)
        super().__init__(master, text=text, **default_style)

        self.target_window = target_window or master
        self.bind("<Button-1>", self._start_move)
        self.bind("<B1-Motion>", self._do_move)

    def _start_move(self, event):
        self._click_x = event.x
        self._click_y = event.y

    def _do_move(self, event):
        delta_x = event.x - self._click_x
        delta_y = event.y - self._click_y
        new_x = self.target_window.winfo_x() + delta_x
        new_y = self.target_window.winfo_y() + delta_y
        self.target_window.geometry(f"+{new_x}+{new_y}")

class MinimizeButton(tk.Button):
    def __init__(self,master, **kwargs):
        default_style = {
            "text": " - ",
            "fg": "white",
            "bg": "#2c3e50",
            "activebackground": "#3c3fe7",
            "activeforeground": "white",
            "bd": 3,
            "font": ("Arial", 12),
        }
        default_style.update(kwargs)
        self.master=master 

        super().__init__(master,command=self._minimize, **default_style)

    def _minimize(self):
        
