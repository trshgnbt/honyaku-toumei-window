from typing import Final, List
import warnings
import tkinter as tk
from tkinter import ttk
import easyocr
import pyautogui
import numpy as np
import math
import argostranslate.translate

from button_commons import CloseButton, DragHandle

class Honyaku(tk.Tk):
    TOUMEI_IRO: Final = "#124356"
    
    def __init__(self):
        super().__init__()

        self._is_minimized = False
        # 表示した翻訳ラベルを管理するリスト（次回実行時に消去するため）
        self.translation_labels: List[tk.Label] = []
        #あらかじめ呼び出しておく
        self.ocr_reader = easyocr.Reader(['en','ja'])
        self.transtator = argostranslate.translate
       
        self.title("翻訳")
        self.geometry("400x300+200+100")
        self.wm_attributes("-topmost", True)#最前面
        self.overrideredirect(True)#枠非表示
        self.attributes("-transparentcolor", Honyaku.TOUMEI_IRO)#透明にする色を指定
        self.configure(bg=Honyaku.TOUMEI_IRO)  # ウィンドウ自体の背景を透明色にする

        #枠線
        self.main_border = tk.Frame(self, bg="#066322", bd=3)
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

    # スクリーンショットボタンの処理
    def sukusyo(self):
        """
        透明フレーム範囲のスクリーンショットを撮影し、OCRで文字認識を行い、英語から日本語に翻訳して表示する。

        処理の流れ:
        1. 前回の翻訳ラベルをクリア
        2. 透明フレームの範囲をスクリーンショット
        3. EasyOCRで文字認識（段落単位）
        4. Argos Translateで英日翻訳
        5. 重なりを避けて翻訳結果をラベル表示
        """
        # 1. 前回表示した翻訳ラベルをすべて削除して画面をクリア
        for label in self.translation_labels:
                label.destroy()       # パーツ自体を完全に破棄する
        self.translation_labels.clear()
        self.update()
        
        # 2. スクショする範囲の計算
        width = self.toumei_frame.winfo_width()
        height = self.toumei_frame.winfo_height()
        x = self.toumei_frame.winfo_rootx()
        y = self.toumei_frame.winfo_rooty()
        # スクリーンショットを取得
        img = pyautogui.screenshot(region=(x, y, width, height))

        # numpy配列に変換する
        img_np = np.array(img)
        
        # 3. EasyOCRの実行（paragraph=True）
        ocr_results = self.ocr_reader.readtext(img_np, paragraph=True)

        # 配置済みのラベルの位置を記録するリスト
        placed_rects = []

        # ★★★ 文字サイズと「1行あたり」の基本設定 ★★★
        FIXED_FONT_SIZE = 11
        LINE_HEIGHT = 24  # 1行あたりの高さ（ピクセル）

        # 4. 検出された文字（段落ごと）に処理をする
        for box, text in ocr_results:
            #マルチバイト文字を除去する
            text_clean = text.encode('ascii', 'ignore').decode('ascii')
            if not text_clean or len(text_clean) < 2:
                continue

            # 5. Argos Translateで翻訳
            try:
                honyakukekka = self.transtator.translate(text_clean, "en", "ja")
            except Exception as e:
                print(f"翻訳エラー: {e}")
                continue

            # 6. 位置と幅の計算
            x_min = int(box[0][0])
            y_min = int(box[0][1])
            x_max = int(box[1][0])
            
            box_width = max(50, x_max - x_min)

            # 【重要】翻訳後の日本語が何行になるかを簡易計算して高さを動的に決める
            # フォントサイズ11の場合、日本語1文字あたり約11〜12ピクセルの幅を使います
            chars_per_line = max(1, box_width // 12)  # 1行に入る文字数
            
            # 全体の文字数から必要行数を計算（端数切り上げ）
         
            estimated_lines = math.ceil(len(honyakukekka) / chars_per_line)
            
            # 高さを「行数 × 24ピクセル」にする（複数行に自動拡張）
            box_height = estimated_lines * LINE_HEIGHT

            # 7. 【重なり防止アルゴリズム】
            # 高さが可変になったため、大きくなったラベル同士もこれで綺麗に押し下げられます
            shift_padding = 2
            overlap = True
            while overlap:
                overlap = False
                current_x1 = x_min
                current_y1 = y_min
                current_x2 = x_min + box_width
                current_y2 = y_min + box_height
                
                for px1, py1, px2, py2 in placed_rects:
                    if not (current_x2 <= px1 or current_x1 >= px2 or 
                            current_y2 <= py1 or current_y1 >= py2):
                        y_min = py2 + shift_padding
                        overlap = True
                        break

            # 最終的な位置を記録
            placed_rects.append((x_min, y_min, x_min + box_width, y_min + box_height))

            # 8. 計算した動的な高さで日本語のLabelを配置
            lbl = tk.Label(
                self.toumei_frame,
                text=honyakukekka,
                bg="black",
                fg="white",
                font=("MS Gothic", FIXED_FONT_SIZE),
                wraplength=box_width,  # ラベル幅に合わせて自動改行
                justify="left",
                anchor="nw"            # 複数行の時は左上（NorthWest）基準で綺麗に詰める
            )
            lbl.place(x=x_min, y=y_min, width=box_width, height=box_height)
            self.translation_labels.append(lbl)


if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=UserWarning)

    app = Honyaku()
    app.mainloop()