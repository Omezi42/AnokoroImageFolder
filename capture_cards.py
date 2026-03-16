import os
import time
import keyboard
import pyautogui
import easyocr
import numpy as np
from PIL import Image
import difflib

# --- 設定項目 ---
# キャプチャする画面全体の領域 (left, top, right, bottom) -> pyautoguiのregionは (left, top, width, height)
# temp_crop.py の CARD_CROP_REGION = (293, 175, 770, 840) に基づく
CARD_LEFT = 293
CARD_TOP = 175
CARD_RIGHT = 770
CARD_BOTTOM = 840
CARD_WIDTH = CARD_RIGHT - CARD_LEFT
CARD_HEIGHT = CARD_BOTTOM - CARD_TOP
CARD_REGION = (CARD_LEFT, CARD_TOP, CARD_WIDTH, CARD_HEIGHT)

# OCRで名前を読み取る相対領域 (カード左上を原点として、カード名が書かれていると推測される領域)
# 左端 (0)、上端 (0)、右端 (477)、下端 (80) と仮定
NAME_REGION_TOP = 0
NAME_REGION_BOTTOM = 85

OUTPUT_DIR = os.path.join("images", "captured_cards_add")
CARD_NAMES_FILE = "all_card_names.txt"
MISSING_CARDS_FILE = "missing_cards.txt"

# ショートカットキー
CAPTURE_KEY = 'f2'
QUIT_KEY = 'esc'

def load_card_names():
    names = []
    if os.path.exists(CARD_NAMES_FILE):
        with open(CARD_NAMES_FILE, 'r', encoding='utf-8') as f:
            names = [line.strip() for line in f if line.strip()]
    return names

def get_best_match(ocr_text, names_list):
    # OCR結果から不要な空白を削除
    ocr_text = ocr_text.replace(" ", "").replace("　", "")
    # ディフマッチングを使用して最も近いカード名を探す
    matches = difflib.get_close_matches(ocr_text, names_list, n=1, cutoff=0.4)
    if matches:
        return matches[0]
    return ocr_text if ocr_text else f"Unknown_{int(time.time())}"

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"📁 {OUTPUT_DIR} を作成しました。")

    print("📚 カード名のリストを読み込んでいます...")
    card_names = load_card_names()
    print(f"✅ {len(card_names)} 件のカード名を読み込みました。")

    print("🔍 OCRエンジンを初期化しています (初回は少し時間がかかります)...")
    reader = easyocr.Reader(['ja', 'en'])
    print(f"\n=========================================")
    print(f"🎯 準備完了！")
    print(f"・【 {CAPTURE_KEY.upper()} 】キーを押すと、現在の画面座標からカードをキャプチャします。")
    print(f"・【 {QUIT_KEY.upper()} 】キーを押すと終了します。")
    print(f"=========================================\n")

    while True:
        try:
            if keyboard.is_pressed(CAPTURE_KEY):
                print("📸 キャプチャ中...")
                # 1. 画面の指定領域をキャプチャ
                # region=(left, top, width, height)
                screenshot = pyautogui.screenshot(region=CARD_REGION)
                
                # 2. OCR用に名前部分だけを切り抜く
                name_img = screenshot.crop((0, NAME_REGION_TOP, CARD_WIDTH, NAME_REGION_BOTTOM))
                
                # Pillow Image -> NumPy 形式へ変換してEasyOCRへ渡す
                name_np = np.array(name_img)
                results = reader.readtext(name_np, detail=0) # テキストのみ抽出
                
                # 3. 検出されたテキストを結合して照合
                detected_text = "".join(results)
                print(f"🔍 OCR検出文字: {detected_text}")
                
                matched_name = get_best_match(detected_text, card_names)
                # ファイル名に使えない文字を置換
                safe_name = matched_name.replace("/", "／").replace(":", "：").replace("*", "＊").replace("?", "？").replace("\"", "”").replace("<", "＜").replace(">", "＞").replace("|", "｜").replace("\\", "＼")
                
                # 4. 画像を保存
                save_path = os.path.join(OUTPUT_DIR, f"{safe_name}.png")
                
                # 万が一同じファイル名がある場合は連番を付ける
                counter = 1
                original_save_path = save_path
                while os.path.exists(save_path):
                    save_path = os.path.join(OUTPUT_DIR, f"{safe_name}_{counter}.png")
                    counter += 1

                screenshot.save(save_path)
                print(f"💾 保存しました: {save_path}\n")
                
                # 連続キャプチャ防止のためのウェイト
                time.sleep(1)

            elif keyboard.is_pressed(QUIT_KEY):
                print("👋 終了します。")
                break
                
            time.sleep(0.05)
            
        except Exception as e:
            print(f"⚠️ エラーが発生しました: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
