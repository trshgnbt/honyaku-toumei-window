import tkinter as tk
from tkinter import ttk
import easyocr
from deep_translator import GoogleTranslator
import pyautogui
import numpy as np
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
        self.close_button = tk.Button(self, text=" × ", fg="white", bg="#2c3e50", activebackground="#e74c3c", activeforeground="white", bd=3, font=("Arial", 12), command=self.destroy)
        self.close_button.place(relx=1.0, y=30, anchor="se")

        # Sizegrip
        self.sizegrip = ttk.Sizegrip(self.main_border)
        self.sizegrip.pack(anchor='se',side='right')

        #移動つまみ
        self.idou_tumami =  tk.Label(self, text=" ☰ 掴んで移動 ", fg="white", bg="#34495e", bd=3, relief="raised", font=("Arial", 10))
        self.idou_tumami.place(relx=1.0, x=-40, y=30, anchor="se", width=100, height=28)
        # つまみにマウスイベントをバインド（紐付け）
        self.idou_tumami.bind("<Button-1>", self.start_move)
        self.idou_tumami.bind("<B1-Motion>", self.do_move)

        #透明部分
        self.toumei_frame = tk.Frame(self.main_border,bg=Honyaku.TOUMEI_IRO)
        self.toumei_frame.pack(fill='both', expand=True)

        #スクリーンショットボタン
        self.sukusyo_button = tk.Button(self.main_border,text="スクリーンショット",command=self.sukusyo)
        self.sukusyo_button.pack()


    #移動つまみの処理
    # 【クリックした瞬間のマウス座標を記録】
    def start_move(self, event):
        self.click_x = event.x
        self.click_y = event.y
        
    def do_move(self, event):
        # 現在のマウス位置と、クリックした位置の「差分（移動量）」を計算
        delta_x = event.x - self.click_x
        delta_y = event.y - self.click_y
        
        # 現在のウィンドウの左上座標を取得して、差分を足す
        new_x = self.winfo_x() + delta_x
        new_y = self.winfo_y() + delta_y
        
        # 新しい座標にウィンドウを移動（現在の幅と高さは維持）
        self.geometry(f"+{new_x}+{new_y}")

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
        for box, text, confidence in ocr_result:                
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