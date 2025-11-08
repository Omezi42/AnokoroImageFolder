import os
import time
from datetime import datetime
from PIL import ImageGrab
import keyboard
import pyautogui
import easyocr
import re

# --- 設定項目 ---
CARD_CROP_REGION = (293, 175, 770, 840)
NAME_CROP_REGION = (983, 183, 1574, 252)
NEXT_BUTTON_POS = (1708, 1003)
CAPTURE_LIMIT = 594
WAIT_TIME = 2.0  # 撮影だけなら短くても大丈夫かも
OUTPUT_DIR = os.path.join("images", "captured_cards")

# OCRリーダーの初期化
print("OCRモデルを読み込んでいます...")
reader = easyocr.Reader(['ja', 'en'], gpu=False)
print("OCRモデルの読み込み完了！")

def sanitize_filename(filename):
    return re.sub(r'[\\|/|:|?|.|"|<|>|\|]', '_', filename)

def get_card_name():
    try:
        name_img = ImageGrab.grab(bbox=NAME_CROP_REGION)
        temp_path = "temp_name.png"
        name_img.save(temp_path)
        result = reader.readtext(temp_path, detail=0)
        if os.path.exists(temp_path): os.remove(temp_path)
        if result:
            return "".join(result).replace(" ", "").strip()
    except:
        pass
    return None

def capture():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    card_name = get_card_name()
    if card_name:
        base_name = sanitize_filename(card_name)
        filename = os.path.join(OUTPUT_DIR, f"{base_name}.png")
        counter = 1
        while os.path.exists(filename):
            filename = os.path.join(OUTPUT_DIR, f"{base_name}_{counter}.png")
            counter += 1
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(OUTPUT_DIR, f"card_{timestamp}.png")

    ImageGrab.grab(bbox=CARD_CROP_REGION).save(filename)
    print(f"📷 Saved: {os.path.basename(filename)}")

def main():
    print(f"--- Step 1: Capture (Save to {OUTPUT_DIR}) ---")
    print("[F6]: Single Shot / [F7]: Auto Mode / [Esc]: Stop Auto")
    
    while True:
        if keyboard.is_pressed('f6'):
            capture()
            time.sleep(0.5)
        elif keyboard.is_pressed('f7'):
            print("🚀 Auto mode started.")
            count = 0
            while True:
                if keyboard.is_pressed('esc'):
                     print("🛑 Stopped.")
                     break
                capture()
                count += 1
                if CAPTURE_LIMIT > 0 and count >= CAPTURE_LIMIT:
                    print("✅ Limit reached.")
                    break
                pyautogui.click(NEXT_BUTTON_POS)
                time.sleep(WAIT_TIME)
            break # 自動モード終了後はメインループも抜けるならbreak, 戻るならコメントアウト
        time.sleep(0.1)

if __name__ == "__main__":
    main()