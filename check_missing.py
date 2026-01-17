import os
from pathlib import Path

# --- Settings ---
# The master list of card names
LIST_FILE = "all_card_names.txt"
# The directory containing captured images
IMAGE_DIR = os.path.join("images", "captured_cards_add")
# ----------------

def main():
    if not os.path.exists(LIST_FILE):
        print(f"Error: List file '{LIST_FILE}' not found.")
        return

    if not os.path.exists(IMAGE_DIR):
        print(f"Error: Image directory '{IMAGE_DIR}' not found.")
        return

    # 1. Read the expected card names
    expected_names = set()
    with open(LIST_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            name = line.strip()
            if name:
                expected_names.add(name)
    
    print(f"Loaded {len(expected_names)} expected card names from '{LIST_FILE}'.")

    # 2. Read the existing image filenames (stems)
    existing_names = set()
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    
    dir_path = Path(IMAGE_DIR)
    for file_path in dir_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            # Handle potential duplicate suffixes like _1.png, but user asked for simple check first
            # step1_capture.py uses sanitize_filename, so filenames usually match card names
            # BUT if there are duplicates, step1_capture adds _1, _2. 
            # We should probably check if the stem STARTS with a card name or if we reverse sanitize?
            # For now, let's assume exact match of sanitized names.
            # step1_capture uses: base_name = sanitize_filename(card_name)
            existing_names.add(file_path.stem)

    print(f"Found {len(existing_names)} images in '{IMAGE_DIR}'.")

    # 3. Compare
    # We need to account for sanitization. The file on disk is sanitized. The list is raw text.
    # So we should sanitize the expected names before checking if they exist.
    
    import re
    def sanitize_filename(filename):
        return re.sub(r'[\\|/|:|?|.|"|<|>|\|]', '_', filename)

    missing_cards = []
    
    # Check each expected card
    # We need to handle the case where multiple cards sanitize to the same name? 
    # Or simply: for each card in list, does sanitized(card) exist in existing_names?
    # Note: existing_names might have _1, _2 suffix. 
    # Let's clean existing names by removing _\d+ suffix? Or just check if sanitized name is in existing_names?
    
    # Creating a set of base sanitized names present in the folder
    # If "CardA.png" exists, we have "CardA". 
    # If "CardA_1.png" exists, we effectively have "CardA" captured (maybe multiple times).
    
    existing_bases = set()
    for name in existing_names:
        # distinct _\d+ removal is tricky if card name ends in number. 
        # But step1_capture adds _counter only if collision.
        # For this check, let's just see if exact match or match-with-suffix exists.
        existing_bases.add(name)

    count_missing = 0
    print("\n--- Missing Cards ---")
    
    files_files = [f.stem for f in Path(IMAGE_DIR).glob("*") if f.is_file()]
    
    for name in sorted(expected_names):
        sanitized = sanitize_filename(name)
        
        # Check if straight match exists
        found = False
        if sanitized in existing_bases:
            found = True
        else:
             # Check if any file starts with sanitized + "_" (e.g. CardName_1)
             for existing in existing_bases:
                 if existing.startswith(sanitized + "_"):
                     # This is a weak check (CardNameExtended_1 would match CardName), but reasonable for now
                     found = True
                     break
        
        if not found:
            print(name)
            missing_cards.append(name)
            count_missing += 1

    if count_missing == 0:
        print("\nAll cards are captured! (Based on filename matching)")
    else:
        print(f"\nTotal Missing: {count_missing}")
        
    # Save missing to file for easy reference
    with open("missing_cards.txt", "w", encoding="utf-8") as f:
        for name in missing_cards:
            f.write(name + "\n")
    print("\nMissing list saved to 'missing_cards.txt'")

if __name__ == "__main__":
    main()
