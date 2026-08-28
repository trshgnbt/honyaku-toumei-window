import tkinter as tk
from tkinter import ttk
from PIL import ImageGrab
from deep_translator import GoogleTranslator
import pyautogui
from typing import Final

class Honyaku(tk.Tk):
    TOUMEI_IRO: Final = "#124356"
    
    def __init__(self):
        super().__init__()
       
        self.title("タイトル")
        self.geometry("400x300+200+100")
        self.wm_attributes("-topmost", True)#最前面
        self.overrideredirect(True)
        self.attributes("-transparentcolor", Honyaku.TOUMEI_IRO)#透明にする色を指定
        self.configure(bg=Honyaku.TOUMEI_IRO)  # ウィンドウ自体の背景を透明色にする


        #枠線
        self.main_border = tk.Frame(self, bg="#00ff00", bd=3)
        self.main_border.place(x=0, y=30, relwidth=1.0, relheight=1.0, height=-30)

        # 閉じるボタン (×)
        self.close_button = tk.Button(self.main_border, text=" × ", fg="white", bg="#2c3e50", activebackground="#e74c3c", activeforeground="white", bd=3, font=("Arial", 12), command=self.destroy)
        self.close_button.place(relx=1.0, y=0, anchor="se")

        # Sizegrip
        self.sizegrip = ttk.Sizegrip(self.main_border)
        self.sizegrip.pack(anchor='se',side='right')

        #移動用つまみ
        self.idou_tumami = 1

        #透明部分
        self.toumei_frame = tk.Frame(self.main_border,bg=Honyaku.TOUMEI_IRO)
        self.toumei_frame.pack(fill='both', expand=True)

        #スクリーンショットボタン
        self.sukusyo_button = tk.Button(self.main_border,text="スクリーンショット",command=self.sukusyo)
        self.sukusyo_button.pack()
                
        #ウィンドウが動いたりサイズが変わったりしたときのイベントを登録
        self.bind("<Configure>", self.on_resize)
        #位置表示ラベル
        self.iti = tk.Label(self.main_border)
        self.iti.pack()

    def on_resize(self,event):
        width = self.winfo_width()
        height = self.winfo_height()
        x = self.winfo_x()
        y = self.winfo_y()
        #表示を変える
        self.iti.config(text=f'x:{x}, y:{y}, 高さ:{height}, 幅:{width}')

    #スクリーンショットボタンの処理
    def sukusyo(self):
        width = self.winfo_width()
        height = self.winfo_height()
        x = self.winfo_x()
        y = self.winfo_y()
        img = pyautogui.screenshot('temp.png', region=(x, y, width, height))

if __name__ == "__main__":    
    app = Honyaku()
    app.mainloop()