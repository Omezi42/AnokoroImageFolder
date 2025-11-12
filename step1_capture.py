import os
import time
from datetime import datetime
from PIL import ImageGrab
import keyboard
import pyautogui
import easyocr
import re
import difflib  # 文字列の類似度比較のために追加
import numpy as np # PIL ImageをNumpy配列に変換するために追加

# --- 設定項目 ---
CARD_CROP_REGION = (293, 175, 770, 840)
NAME_CROP_REGION = (983, 183, 1574, 252)
NEXT_BUTTON_POS = (1708, 1003)
CAPTURE_LIMIT = 594
WAIT_TIME = 0.1  # 次のカードへの待機時間
OUTPUT_DIR = os.path.join("images", "captured_cards")
CARD_LIST_FILE = "all_card_names.txt" # カード名リストのファイルパス
SIMILARITY_THRESHOLD = 0.6  # 類似度のしきい値。これ未満の場合は「不明」とみなす

# OCRリーダーの初期化
print("OCRモデルを読み込んでいます...")
reader = easyocr.Reader(['ja', 'en'], gpu=False)
print("OCRモデルの読み込み完了！")

# カード名リストの読み込み
all_card_names = []
if os.path.exists(CARD_LIST_FILE):
    try:
        # UTF-8でファイルを開く
        with open(CARD_LIST_FILE, 'r', encoding='utf-8') as f:
            # 各行の空白文字（改行コードなど）を除去してリストに追加
            all_card_names = [line.strip() for line in f if line.strip()]
        print(f"'{CARD_LIST_FILE}'から{len(all_card_names)}件のカード名を読み込みました。")
    except Exception as e:
        print(f"警告: '{CARD_LIST_FILE}'の読み込みに失敗しました。 {e}")
else:
    print(f"警告: '{CARD_LIST_FILE}'が見つかりません。OCR結果をそのまま使用するモードになります。")

def sanitize_filename(filename):
    """ファイル名として使えない文字を'_'に置き換える"""
    return re.sub(r'[\\|/|:|?|.|"|<|>|\|]', '_', filename)

def get_ocr_result():
    """指定領域からOCRでテキストを抽出する"""
    try:
        # 1. 領域をキャプチャ
        name_img = ImageGrab.grab(bbox=NAME_CROP_REGION)
        
        # 2. PIL ImageをNumpy配列に変換（EasyOCRが直接扱える形式）
        name_img_np = np.array(name_img)
        
        # 3. OCR実行
        result = reader.readtext(name_img_np, detail=0)
        
        if result:
            # 4. OCR結果が複数ブロックの場合があるので連結し、空白を除去
            return "".join(result).replace(" ", "").strip()
    except Exception as e:
        print(f"OCR実行中にエラー: {e}")
    return None

def find_closest_card_name(ocr_name):
    """OCR結果（ocr_name）に最も近いカード名をall_card_namesリストから探す"""
    
    # カード名リストが空か、OCR結果がなければ処理終了
    if not all_card_names or not ocr_name:
        return None # OCR結果がそのまま使われる（リストがない場合）か、None（OCR失敗）
        
    best_match = None
    highest_ratio = 0.0
    
    # difflib.SequenceMatcherを使って最も類似度が高いものを探す
    for card_name in all_card_names:
        # 類似度を計算
        ratio = difflib.SequenceMatcher(None, ocr_name, card_name).ratio()
        
        # これまでで一番高い類似度なら更新
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = card_name
            
    # 最も高かった類似度が、設定したしきい値（例: 0.6）以上の場合
    if highest_ratio >= SIMILARITY_THRESHOLD:
        print(f"OCR: '{ocr_name}' -> 候補: '{best_match}' (類似度: {highest_ratio:.2f})")
        return best_match # 最も近かったカード名を返す
    else:
        # しきい値未満の場合は、一致するものがなかったとみなす
        print(f"OCR: '{ocr_name}' -> 一致候補なし (最高: '{best_match}' {highest_ratio:.2f})")
        return None 

def capture():
    """カード画像のキャプチャと保存を行う"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    # 1. OCRでカード名を取得
    ocr_result = get_ocr_result()
    
    # 2. OCR結果を元に、カード名リストから最も近い名前を探す
    card_name = None
    if all_card_names:
        # カードリストがある場合は、最も近い名前を探す
        card_name = find_closest_card_name(ocr_result)
    elif ocr_result:
        # カードリストがない場合は、OCR結果をそのまま（サニタイズして）使う
        print(f"OCR: '{ocr_result}' (リスト照合なし)")
        card_name = ocr_result
    
    # 3. ファイル名を決定
    if card_name:
        # 候補が見つかった（またはOCR結果をそのまま使う）場合
        base_name = sanitize_filename(card_name)
        filename = os.path.join(OUTPUT_DIR, f"{base_name}.png")
        counter = 1
        # ファイル名の重複チェック
        while os.path.exists(filename):
            filename = os.path.join(OUTPUT_DIR, f"{base_name}_{counter}.png")
            counter += 1
    else:
        # 候補が見つからなかった（OCR失敗または類似度不足）場合
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(OUTPUT_DIR, f"card_{timestamp}.png")
        if ocr_result: # OCR結果はあったが候補がなかった場合、ログに残す
            print(f"（保存: card_{timestamp}.png / OCR元: '{ocr_result}'）")

    # 4. カード領域の画像を保存
    ImageGrab.grab(bbox=CARD_CROP_REGION).save(filename)
    print(f"📷 Saved: {os.path.basename(filename)}")

def show_mouse_position():
    """現在のマウス位置を表示する"""
    try:
        x, y = pyautogui.position()
        print(f"📍 現在のマウス位置: ({x}, {y})")
    except Exception as e:
        print(f"マウス位置の取得に失敗: {e}")

def main():
    print(f"--- Step 1: Capture (Save to {OUTPUT_DIR}) ---")
    print(f"カード名リスト: '{CARD_LIST_FILE}' ({'ロード済' if all_card_names else '未ロード/見つかりません'})")
    print(f"類似度しきい値: {SIMILARITY_THRESHOLD}")
    print("[F2] : 現在のマウスカーソル位置を表示（座標確認用）")
    print("[F6] : 1枚撮影 (Single Shot)")
    print("[F7] : 自動撮影モード (Auto Mode) / [Esc]で停止")
    
    while True:
        try:
            if keyboard.is_pressed('f2'):
                show_mouse_position()
                time.sleep(0.3) # 連打防止
            elif keyboard.is_pressed('f6'):
                print("\n--- Single Shot ---")
                capture()
                time.sleep(0.5) # 連打防止
            elif keyboard.is_pressed('f7'):
                print("\n--- Auto Mode ---")
                print("🚀 自動撮影を開始します。[Esc]キーで停止します。")
                count = 0
                while True:
                    if keyboard.is_pressed('esc'):
                         print("🛑 自動撮影を停止しました。")
                         break
                    
                    capture()
                    count += 1
                    
                    if CAPTURE_LIMIT > 0 and count >= CAPTURE_LIMIT:
                        print(f"✅ 撮影枚数が上限 ({CAPTURE_LIMIT}枚) に達しました。")
                        break
                        
                    pyautogui.click(NEXT_BUTTON_POS)
                    time.sleep(WAIT_TIME) # 次のカードが表示されるのを待つ
                
                # 自動モードが終了したら、キー入力待ちに戻る
                print("キー入力待機状態に戻ります。[F6] / [F7] / [F2]")

        except Exception as e:
            print(f"メインループでエラーが発生しました: {e}")
            print("5秒後に再試行します...")
            time.sleep(5)
            
        time.sleep(0.05) # CPU負荷軽減

if __name__ == "__main__":
    main()