import os
import sys

CARD_NAMES_FILE = "all_card_names.txt"

def load_card_names():
    if not os.path.exists(CARD_NAMES_FILE):
        return set()
    with open(CARD_NAMES_FILE, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

def save_card_names(names_set):
    # 日本語の辞書順（文字コード順）にソートして保存
    sorted_names = sorted(list(names_set))
    with open(CARD_NAMES_FILE, 'w', encoding='utf-8') as f:
        for name in sorted_names:
            f.write(name + "\n")
    return len(sorted_names)

def main():
    print("=== 辞書ファイル (all_card_names.txt) 更新ツール ===")
    names_set = load_card_names()
    start_count = len(names_set)
    print(f"現在の登録数: {start_count} 件\n")

    # もし引数にパス（ファイルまたはフォルダ）が指定された場合
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        if os.path.isdir(input_path):
            print(f"📁 フォルダ '{input_path}' 内の画像ファイル名から読み込みます...")
            for filename in os.listdir(input_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    name = os.path.splitext(filename)[0]
                    # 不要なサフィックスがあれば一応除去
                    name = name.replace("_cropped", "").replace("_transparent", "")
                    if name:
                        names_set.add(name)
        elif os.path.isfile(input_path):
            print(f"📄 ファイル '{input_path}' からテキスト行を一括読み込みます...")
            with open(input_path, 'r', encoding='utf-8') as f:
                for line in f:
                    name = line.strip()
                    if name:
                        names_set.add(name)
        else:
            print(f"⚠️ 指定されたパスが見つかりません: {input_path}")
    else:
        # 引数がない場合は対話モードで一つずつ追加する
        print("追加したい新しいカード名を1つずつ入力してください。")
        print("（終わる時は何も入力せずに Enter を押してください）\n")
        while True:
            new_name = input("追加するカード名 > ").strip()
            if not new_name:
                break
            
            if new_name in names_set:
                print(f"  ⚠️ 「{new_name}」は既に登録されています。")
            else:
                names_set.add(new_name)
                print(f"  ✅ 「{new_name}」をリストに追加しました！")

    end_count = len(names_set)
    added = end_count - start_count

    # 追加分がある場合のみ保存して更新を知らせる
    if added > 0:
        save_card_names(names_set)
        print(f"\n🎉 更新完了！ 新たに {added} 件追加し、合計 {end_count} 件になりました。（あいうえお順に並べ直して保存しました）")
    else:
        print("\n💡 追加する新しいカード名はありませんでした（ファイル更新なし）。")

if __name__ == "__main__":
    main()
