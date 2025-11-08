import os
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from tqdm import tqdm

# --- 設定項目 ---
IMAGES_DIR = "images"
FAILED_DIR = os.path.join(IMAGES_DIR, "failed_transparent_cards")
CROPPED_DIR = os.path.join(IMAGES_DIR, "cropped_cards")
TRANSPARENT_DIR = os.path.join(IMAGES_DIR, "transparent_cards")

# ぼかし（フェード）をかける幅（ピクセル）
FADE_WIDTH = 20
# 角丸の半径（ピクセル）
CORNER_RADIUS = 30

def fade_edges(img, fade_width, corner_radius):
    """
    画像の四隅を角丸かつグラデーションで透過させる
    """
    img = img.convert("RGBA")
    width, height = img.size
    
    # マスクを作成（最初は真っ黒＝完全透過）
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    
    # 角丸の長方形を描画（内側を白く塗りつぶす＝不透明）
    # 四隅から fade_width 分だけ内側の領域を指定
    draw.rounded_rectangle(
        (fade_width, fade_width, width - fade_width, height - fade_width),
        radius=corner_radius,
        fill=255
    )
    
    # マスクをぼかす
    mask_blurred = mask.filter(ImageFilter.GaussianBlur(fade_width / 2))
    
    # 新しいマスクを適用する
    img.putalpha(mask_blurred)
    
    return img

def cleanup_double_transparent_files():
    """
    _transparent_transparent.png ファイルを削除する
    """
    print("🧹 クリーンアップを開始します...")
    removed_count = 0
    if os.path.exists(TRANSPARENT_DIR):
        for filename in os.listdir(TRANSPARENT_DIR):
            if filename.endswith("_transparent_transparent.png"):
                file_path = os.path.join(TRANSPARENT_DIR, filename)
                try:
                    os.remove(file_path)
                    removed_count += 1
                except Exception as e:
                    print(f"⚠️ 削除失敗: {filename} ({e})")
    print(f"✅ {removed_count} 個の不要なファイルを削除しました。")

def main():
    # 1. まずは不要ファイルの掃除
    cleanup_double_transparent_files()

    if not os.path.exists(FAILED_DIR):
        print(f"❌ エラー: 失敗画像フォルダが見つかりません: {FAILED_DIR}")
        return

    failed_files = [f for f in os.listdir(FAILED_DIR) if f.lower().endswith('.png')]
    print(f"\n--- Step 3.5: Fix Failed Cards ({len(failed_files)} files) ---")

    for failed_filename in tqdm(failed_files):
        # 失敗したファイル名から元のカード名を推測
        base_name = failed_filename.replace("_transparent.png", "").replace("_cropped.png", "").replace(".png", "")
        
        # 対応するcropped画像を探す
        cropped_filename = f"{base_name}_cropped.png"
        cropped_path = os.path.join(CROPPED_DIR, cropped_filename)

        if not os.path.exists(cropped_path):
            print(f"⚠️ 元画像が見つかりません: {cropped_filename} (スキップ)")
            continue

        # 出力パス
        output_filename = f"{base_name}_transparent.png"
        output_path = os.path.join(TRANSPARENT_DIR, output_filename)

        try:
            # cropped画像を開いて端をぼかす（角丸追加）
            with Image.open(cropped_path) as img:
                faded_img = fade_edges(img, FADE_WIDTH, CORNER_RADIUS)
                faded_img.save(output_path)
        except Exception as e:
            print(f"❌ 処理エラー {failed_filename}: {e}")

    print("🎉 修正完了！")

if __name__ == "__main__":
    main()