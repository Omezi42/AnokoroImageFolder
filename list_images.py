import os
from pathlib import Path

def list_image_filenames(directory_path, output_file):
    """
    指定されたディレクトリ内の画像ファイルの拡張子なしのファイル名を
    テキストファイルに出力します。
    """
    # 画像として扱う拡張子のセット（必要に応じて追加・削除してください）
    # 大文字・小文字は区別しないように処理内で変換しています
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}

    # Pathオブジェクトを作成
    dir_path = Path(directory_path)

    # ディレクトリが存在するか確認
    if not dir_path.is_dir():
        print(f"エラー: 指定されたフォルダーが見つかりません: {directory_path}")
        print("TARGET_DIRECTORY のパスが正しいか確認してください。")
        return

    image_names = []
    # ディレクトリ内のすべてのファイルを走査
    try:
        for file_path in dir_path.iterdir():
            # ファイルであり、かつ拡張子が画像セットに含まれる場合（小文字に変換して比較）
            if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                # .stem は拡張子を除いたファイル名を取得します
                image_names.append(file_path.stem)
    except Exception as e:
         print(f"フォルダーの読み込み中にエラーが発生しました: {e}")
         return

    # 名前順にソート（オプション）
    image_names.sort()

    # テキストファイルに出力
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for name in image_names:
                f.write(name + '\n')
        print(f"成功: {len(image_names)} 件の画像ファイル名を出力しました。")
        print(f"出力ファイル: {os.path.abspath(output_file)}")
    except Exception as e:
        print(f"ファイルの書き込み中にエラーが発生しました: {e}")

# ==========================================
# 設定エリア
# ==========================================

# 1. 対象のフォルダーパスをここに指定してください。
# Windowsのパス例: r"C:\Users\YourName\Pictures\Vacation"
# Mac/Linuxのパス例: "/home/user/images"
# ※ r"" を使うとバックスラッシュをそのまま扱えるので便利です。
TARGET_DIRECTORY = r"./images/captured_cards"  # 現在のディレクトリを対象とする例

# 2. 出力するテキストファイル名
OUTPUT_FILENAME = "all_card_names.txt"

# ==========================================

if __name__ == "__main__":
    list_image_filenames(TARGET_DIRECTORY, OUTPUT_FILENAME)