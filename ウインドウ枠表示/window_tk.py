import tkinter as tk
from tkinter import ttk

class Honyaku(tk.Tk):
    def __init__(self):
        super().__init__()
       
        self.title("タイトル")
        self.geometry("400x300")
        self.wm_attributes("-topmost", True)#最前面
        
        #背景を透明にする設定
        transparent_color = "#124356"
        self.attributes("-transparentcolor", transparent_color)
        toumei_frame = tk.Frame(self,bg=transparent_color)
        toumei_frame.pack(fill='both', expand=True)
                
        #ウィンドウが動いたりサイズが変わったりしたときのイベントを登録
        self.bind("<Configure>", self.on_resize)
        #位置表示ラベル
        self.iti = tk.Label(self, text="あああああ")
        self.iti.pack()

        # Sizegrip
        sizegrip = ttk.Sizegrip(self)
        sizegrip.pack(anchor='se',side='right')

    def on_resize(self,event):
        width = self.winfo_width()
        height = self.winfo_height()
        x = self.winfo_x()
        y = self.winfo_y()
        #表示を変える
        self.iti.config(text=f'x:{x}, y:{y}, 高さ:{height}, 幅:{width}')

if __name__ == "__main__":    
    app = Honyaku()
    app.mainloop()