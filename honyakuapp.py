import tkinter as tk
from tkinter import ttk
import easyocr
from deep_translator import GoogleTranslator
import pyautogui
import numpy as np
from typing import Final

from button_commons import CloseButton, DragHandle, MinimizeButton

class Honyaku(tk.Tk):
    TOUMEI_IRO: Final = "#124356"
    
    def __init__(self):
        super().__init__()

        self._is_minimized = False
       
        self.title("タイトル")
        self.geometry("400x300+200+100")
        self.wm_attributes("-topmost", True)#最前面
        self.overrideredirect(True)#枠非表示
        self.attributes("-transparentcolor", Honyaku.TOUMEI_IRO)#透明にする色を指定
        self.configure(bg=Honyaku.TOUMEI_IRO)  # ウィンドウ自体の背景を透明色にする

        #枠線
        self.main_border = tk.Frame(self, bg="#00ff00", bd=3)
        self.main_border.place(x=0, y=30, relwidth=1.0, relheight=1.0, height=-30)

        # 閉じるボタン (×)
        self.close_button = CloseButton(self)
        self.close_button.place(relx=1.0, y=30, anchor="se")
        
        #移動つまみ
        self.idou_tumami = DragHandle(self)
        self.idou_tumami.place(relx=1.0, x=-80, y=30, anchor="se", width=100, height=30)

        #最小化ボタン
        self.saisyouka_button = tk.Button(
            self,
            text =" - ",
            fg = "white",
            bg= "#2c3e50",
            activebackground= "#3c3fe7",
            activeforeground= "white",
            bd= 3,
            font= ("Arial", 12),
            command=self.saisyouka
        )
        self.saisyouka_button.place(relx=1.0, x=-40, y=30, anchor="se", height=30)

        # Sizegrip
        self.sizegrip = ttk.Sizegrip(self)
        self.sizegrip.pack(anchor='se',side='right')

        #透明部分
        self.toumei_frame = tk.Frame(self.main_border,bg=Honyaku.TOUMEI_IRO)
        self.toumei_frame.pack(fill='both', expand=True)

        #スクリーンショットボタン
        self.sukusyo_button = tk.Button(self.main_border,text="スクリーンショット",command=self.sukusyo)
        self.sukusyo_button.pack()

        #最小化から戻した時に検知
        self.bind("<Map>", self.on_deiconify)


    #最小化から戻した時の処理
    def on_deiconify(self, event=None):
        if event is not None and event.widget != self:
            return
        if self._is_minimized and self.state() == 'normal':
            self._is_minimized = False  # 先にフラグを倒す→再帰呼び出しを弾く
            self.overrideredirect(True)

    #最小化させる処理
    def saisyouka(self):
        self._is_minimized = True
        self.overrideredirect(False)
        self.iconify()

    #スクリーンショットボタンの処理
    def sukusyo(self):
        width = self.winfo_width()
        height = self.winfo_height() -30
        x = self.winfo_x()
        y = self.winfo_y() +30
        img = pyautogui.screenshot('temp.png', region=(x, y, width, height))

        #numpy配列に変換する
        img_np = np.array(img)
        #OCR
        ocr_reader = easyocr.Reader(['en'])
        ocr_result = ocr_reader.readtext(img_np)

        #翻訳する
        translator = GoogleTranslator(source='en', target='ja')
        for bbox, text in ocr_result:                
            # 1行ずつ翻訳する
            translated_text = translator.translate(text)
            
            # 元の英語と、翻訳した日本語を表示
            print(f"元データ: {text}")
            print(f"翻訳結果: {translated_text}")
            print("-" * 30)

        print("翻訳完了")


if __name__ == "__main__":    
    app = Honyaku()
    app.mainloop()