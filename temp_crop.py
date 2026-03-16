import os
from PIL import Image
from tqdm import tqdm # 騾ｲ謐苓｡ｨ遉ｺ逕ｨ・・ip install tqdm 縺悟ｿ・ｦ√ゅ↑縺代ｌ縺ｰprint縺ｧ繧ょ庄・・
# --- 險ｭ螳夐・岼 ---
# 繧ｫ繝ｼ繝臥判蜒丞・縺ｧ縺ｮ繧､繝ｩ繧ｹ繝井ｽ咲ｽｮ・育嶌蟇ｾ蠎ｧ讓呻ｼ・# 蜈・・繧ｹ繧ｯ繝ｪ繝ｼ繝ｳ繧ｷ繝ｧ繝・ヨ(CARD_CROP_REGION)縺ｮ蟾ｦ荳翫ｒ(0,0)縺ｨ縺励◆縺ｨ縺阪・蠎ｧ讓吶〒縺吶・# CARD_CROP_REGION = (293, 175, 770, 840)  蟷・477, 鬮倥＆=665
# ILLUST_CROP_REGION = (315, 261, 738, 484)
# 逶ｸ蟇ｾ蠎ｧ讓・= (315-293, 261-175, 738-293, 484-175) = (22, 86, 445, 309)
RELATIVE_ILLUST_REGION = (22, 86, 445, 309)

INPUT_DIR = os.path.join("images", "captured_cards_add")
OUTPUT_DIR = os.path.join("images", "cropped_cards_add")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.png')]
    print(f"--- Step 2: Crop ({len(files)} files) ---")

    # tqdm繧剃ｽｿ縺・→繝励Ο繧ｰ繝ｬ繧ｹ繝舌・縺悟・縺ｾ縺吶ゆｽｿ繧上↑縺・ｴ蜷医・騾壼ｸｸ縺ｮfor繝ｫ繝ｼ繝励〒OK
    for filename in tqdm(files):
        input_path = os.path.join(INPUT_DIR, filename)
        output_filename = f"{os.path.splitext(filename)[0]}.png"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        # 既に存在する場合はスキップ
        if os.path.exists(output_path):
            continue

        try:
            with Image.open(input_path) as img:
                cropped_img = img.crop(RELATIVE_ILLUST_REGION)
                cropped_img.save(output_path)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print("笨・Cropping completed!")

if __name__ == "__main__":
    main()
