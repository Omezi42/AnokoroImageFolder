import os
from PIL import Image
from tqdm import tqdm
import rembg

# --- 設定項目 ---
# クロップ済みの画像があるフォルダ（今回は _add 側をデフォルトにしています）
INPUT_DIR = os.path.join("images", "cropped_cards_add")
OUTPUT_DIR = os.path.join("images", "transparent_cards_add")
FAILED_DIR = os.path.join("images", "failed_transparent_cards")

def main():
    # フォルダが存在しない場合は作成
    for directory in [OUTPUT_DIR, FAILED_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # 処理対象のファイルリストを取得
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.png')]
    if len(files) == 0:
        print(f"📂 {INPUT_DIR} に画像が見つかりません。")
        return

    print(f"--- Step 3: Remove Background using rembg ({len(files)} files) ---")

    # tqdmでプログレスバーを表示しながら処理
    for filename in tqdm(files):
        input_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, filename)

        # 既に処理済みの場合はスキップ
        if os.path.exists(output_path):
            continue

        try:
            # 元画像を読み込み、rembgで背景を透過
            with Image.open(input_path) as img:
                result_img = rembg.remove(img)
                result_img.save(output_path)
                
        except Exception as e:
            print(f"\n⚠️ 透過処理エラー {filename}: {e}")
            # 失敗した場合は failed フォルダに元の画像をコピーしておき、後で temp_fade.py で処理できるようにする
            failed_path = os.path.join(FAILED_DIR, filename)
            try:
                with Image.open(input_path) as img:
                    img.save(failed_path)
            except:
                pass

    print("✅ 透過処理が完了しました！")

if __name__ == "__main__":
    main()
