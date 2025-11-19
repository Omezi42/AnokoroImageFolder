import os
from PIL import Image
from tqdm import tqdm # 進捗表示用（pip install tqdm が必要。なければprintでも可）

# --- 設定項目 ---
# カード画像内でのイラスト位置（相対座標）
# 元のスクリーンショット(CARD_CROP_REGION)の左上を(0,0)としたときの座標です。
# CARD_CROP_REGION = (293, 175, 770, 840)  幅=477, 高さ=665
# ILLUST_CROP_REGION = (315, 261, 738, 484)
# 相対座標 = (315-293, 261-175, 738-293, 484-175) = (22, 86, 445, 309)
RELATIVE_ILLUST_REGION = (22, 86, 445, 309)

INPUT_DIR = os.path.join("images", "captured_cards_add")
OUTPUT_DIR = os.path.join("images", "cropped_cards_add")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.png')]
    print(f"--- Step 2: Crop ({len(files)} files) ---")

    # tqdmを使うとプログレスバーが出ます。使わない場合は通常のforループでOK
    for filename in tqdm(files):
        input_path = os.path.join(INPUT_DIR, filename)
        output_filename = f"{os.path.splitext(filename)[0]}_cropped.png"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        # 既に存在する場合はスキップ（高速化のため）
        if os.path.exists(output_path):
            continue

        try:
            with Image.open(input_path) as img:
                cropped_img = img.crop(RELATIVE_ILLUST_REGION)
                cropped_img.save(output_path)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print("✅ Cropping completed!")

if __name__ == "__main__":
    main()