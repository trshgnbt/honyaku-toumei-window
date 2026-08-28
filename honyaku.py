import easyocr
from PIL import ImageGrab
from deep_translator import GoogleTranslator

# --- 1. スクショを取得 ---
print("画面を撮影中...")
screenshot = ImageGrab.grab()
image_path = "temp_screenshot.png"
screenshot.save(image_path)

# --- 2. 文字認識（OCR） ---
print("文字を認識中...")
# 今回は英語の画面を読み取る想定で、英語（'en'）を指定
reader = easyocr.Reader(['en'])
result = reader.readtext(image_path)

# --- 3. 翻訳して表示 ---
print("\n=== 翻訳結果 ===")

# 翻訳エンジンを設定（自動判定 'auto' から 日本語 'ja' へ翻訳）
translator = GoogleTranslator(source='auto', target='ja')

for box, text, confidence in result:
    # 信頼度の低い（見間違いっぽい）文字はパスする（例: 0.3以下）
    if confidence < 0.3:
        continue
        
    # 1行ずつ翻訳する
    translated_text = translator.translate(text)
    
    # 元の英語と、翻訳した日本語を表示
    print(f"元データ: {text}")
    print(f"翻訳結果: {translated_text}")
    print("-" * 30)
