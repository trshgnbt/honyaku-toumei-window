from typing import Final, List
import warnings
import os
import tkinter as tk
from tkinter import ttk
import easyocr
import pyautogui
import numpy as np
import argostranslate.translate

from button_commons import CloseButton, DragHandle

class Honyaku(tk.Tk):
    TOUMEI_IRO: Final = "#124356"
    
    def __init__(self):
        super().__init__()

        self._is_minimized = False
        # 表示した翻訳ラベルを管理するリスト（次回実行時に消去するため）
        self.translation_labels: List[tk.Label] = []
       
        self.title("翻訳")
        self.geometry("400x300+200+100")
        self.wm_attributes("-topmost", True)#最前面
        self.overrideredirect(True)#枠非表示
        self.attributes("-transparentcolor", Honyaku.TOUMEI_IRO)#透明にする色を指定
        self.configure(bg=Honyaku.TOUMEI_IRO)  # ウィンドウ自体の背景を透明色にする

        #枠線
        self.main_border = tk.Frame(self, bg="#0c490c", bd=3)
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
        #スクショ前に翻訳結果ラベルを消す
        for label in self.translation_labels:
            label.destroy()
        self.translation_labels.clear()

        #スクショする
        width = self.winfo_width()
        height = self.winfo_height() -55
        x = self.winfo_x()
        y = self.winfo_y() +30
        img = pyautogui.screenshot('temp.png', region=(x, y, width, height))

        #numpy配列に変換する
        img_np = np.array(img)
        #OCR
        ocr_reader = easyocr.Reader(['en'])
        ocr_results = ocr_reader.readtext(img_np)

        for box, text, confidence  in ocr_results:
            text_clean = text.strip()
            #OCRの確信度が低いものはスキップする
            if not text_clean or len(text_clean) < 2 or confidence < 0.3: # type: ignore
                continue

            #argoで翻訳する
            try:
                honyakukekka = argostranslate.translate.translate(text_clean, "en", "ja")
            except Exception as e:
                print(f"翻訳エラー: {e}")
                continue

            #翻訳結果を表示する
            # boxは [[左上x, 左上y], [右上x, 右上y], [右下x, 右下y], [左下x, 左下y]]という構造になっている
            x_min = int(box[0][0])
            y_min = int(box[0][1])
            x_max = int(box[2][0])
            y_max = int(box[2][1])

            box_width = x_max - x_min
            box_height = y_max - y_min

            #元の英文の上に重なるように日本語のLabelを配置
            font_size = max(9, int(box_height * 0.6))
            lbl = tk.Label(
                self.toumei_frame,
                text=honyakukekka,
                bg="black",
                fg="white",
                font=("MS Gothic", font_size),
                wraplength=box_width, # ラベル幅に合わせて自動改行
                justify="left"
            )
            #配置
            lbl.place(x=x_min, y=y_min, width=box_width, height=box_height)           


if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=UserWarning)
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    app = Honyaku()
    app.mainloop()