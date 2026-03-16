import os
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from tqdm import tqdm

# --- 險ｭ螳夐・岼 ---
IMAGES_DIR = "images"
FAILED_DIR = os.path.join(IMAGES_DIR, "failed_transparent_cards")
CROPPED_DIR = os.path.join(IMAGES_DIR, "cropped_cards")
TRANSPARENT_DIR = os.path.join(IMAGES_DIR, "transparent_cards")

# 縺ｼ縺九＠・医ヵ繧ｧ繝ｼ繝会ｼ峨ｒ縺九￠繧句ｹ・ｼ医ヴ繧ｯ繧ｻ繝ｫ・・FADE_WIDTH = 20
# 隗剃ｸｸ縺ｮ蜊雁ｾ・ｼ医ヴ繧ｯ繧ｻ繝ｫ・・CORNER_RADIUS = 30

def fade_edges(img, fade_width, corner_radius):
    """
    逕ｻ蜒上・蝗幃嚆繧定ｧ剃ｸｸ縺九▽繧ｰ繝ｩ繝・・繧ｷ繝ｧ繝ｳ縺ｧ騾城℃縺輔○繧・    """
    img = img.convert("RGBA")
    width, height = img.size
    
    # 繝槭せ繧ｯ繧剃ｽ懈・・域怙蛻昴・逵溘▲鮟抵ｼ晏ｮ悟・騾城℃・・    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    
    # コメント文字化けのため、削除して再記述します
    draw.rounded_rectangle(
        [fade_width, fade_width, width - fade_width, height - fade_width],
        radius=corner_radius,
        fill=255
    )
    
    # 繝槭せ繧ｯ繧偵⊂縺九☆
    mask_blurred = mask.filter(ImageFilter.GaussianBlur(fade_width / 2))
    
    # 譁ｰ縺励＞繝槭せ繧ｯ繧帝←逕ｨ縺吶ｋ
    img.putalpha(mask_blurred)
    
    return img

def cleanup_double_transparent_files():
    """
    _transparent_transparent.png 繝輔ぃ繧､繝ｫ繧貞炎髯､縺吶ｋ
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
    # 1. 縺ｾ縺壹・荳崎ｦ√ヵ繧｡繧､繝ｫ縺ｮ謗・勁
    cleanup_double_transparent_files()

    if not os.path.exists(FAILED_DIR):
        print(f"笶・繧ｨ繝ｩ繝ｼ: 螟ｱ謨礼判蜒上ヵ繧ｩ繝ｫ繝縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ: {FAILED_DIR}")
        return

    failed_files = [f for f in os.listdir(FAILED_DIR) if f.lower().endswith('.png')]
    print(f"\n--- Step 3.5: Fix Failed Cards ({len(failed_files)} files) ---")

    for failed_filename in tqdm(failed_files):
        # 螟ｱ謨励＠縺溘ヵ繧｡繧､繝ｫ蜷阪°繧牙・縺ｮ繧ｫ繝ｼ繝牙錐繧呈耳貂ｬ
        base_name = failed_filename.replace("_transparent.png", "").replace("_cropped.png", "").replace(".png", "")
        
        # 蟇ｾ蠢懊☆繧議ropped逕ｻ蜒上ｒ謗｢縺・        cropped_filename = f"{base_name}.png"
        cropped_path = os.path.join(CROPPED_DIR, cropped_filename)

        if not os.path.exists(cropped_path):
            print(f"笞・・蜈・判蜒上′隕九▽縺九ｊ縺ｾ縺帙ｓ: {cropped_filename} (繧ｹ繧ｭ繝・・)")
            continue

        # 蜃ｺ蜉帙ヱ繧ｹ
        output_filename = f"{base_name}.png"
        output_path = os.path.join(TRANSPARENT_DIR, output_filename)

        try:
            # cropped逕ｻ蜒上ｒ髢九＞縺ｦ遶ｯ繧偵⊂縺九☆・郁ｧ剃ｸｸ霑ｽ蜉・・            with Image.open(cropped_path) as img:
                faded_img = fade_edges(img, FADE_WIDTH, CORNER_RADIUS)
                faded_img.save(output_path)
        except Exception as e:
            print(f"❌ 処理エラー {failed_filename}: {e}")

    print("✅ 修正完了！")

if __name__ == "__main__":
    main()
