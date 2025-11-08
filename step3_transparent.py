import os
from rembg import remove
from PIL import Image
from tqdm import tqdm
import io

INPUT_DIR = os.path.join("images", "cropped_cards")
OUTPUT_DIR = os.path.join("images", "transparent_cards")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.png')]
    print(f"--- Step 3: Remove Background ({len(files)} files) ---")

    for filename in tqdm(files):
        input_path = os.path.join(INPUT_DIR, filename)
        # _cropped を _transparent に置換
        output_filename = filename.replace("_cropped.png", "_transparent.png")
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        if os.path.exists(output_path):
            continue

        try:
            with open(input_path, 'rb') as i:
                input_data = i.read()
                output_data = remove(input_data)
                with open(output_path, 'wb') as o:
                    o.write(output_data)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print("✅ Background removal completed!")

if __name__ == "__main__":
    main()