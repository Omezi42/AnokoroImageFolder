# あの頃カード画像プロセッサー

カードゲーム「あの頃の自作TCG」のカード画像を自動加工し、GitHubリポジトリに直接Pushする Web アプリです。

## 🚀 使い方

1. **[カード画像プロセッサー](https://omezi42.github.io/AnokoroImageFolder/)** を開く
2. カード画像をアップロード（ファイル選択 / ドラッグ＆ドロップ / `Ctrl+V`ペースト）
3. カード名を確認（自動検出 or 手動入力）
4. 「加工を実行」でクロップ＋AI背景透過処理
5. 「GitHubにPush」で自動コミット

> **初回セットアップ**: 「設定とヘルプ」欄からGitHub Personal Access Token（`repo`スコープ）を取得・入力してください。

## 🎯 画像加工パイプライン

| ステップ | 処理内容 | 相当するPythonスクリプト |
|---------|---------|----------------------|
| ① 入力 | 画像をアップロード/ペースト (全画面/カード単体) | `capture_cards.py` |
| ② カード名 | Gemini APIで自動検出 + リスト照合 | `capture_cards.py` (OCR) |
| ③ クロップ | イラスト領域を抽出 (22, 86, 445, 309) | `temp_crop.py` |
| ④ AI透過 | `@imgly/background-removal` を用いた背景透過 | `temp_rembg.py` |
| ⑤ Push | GitHub APIで3種の画像と辞書を自動コミット | （新規機能） |

## 🛠 新機能と保存場所

画像1枚につき、以下の3つのファイルがそれぞれのフォルダに保存されます。

- **`images/captured_cards/`** : アップロードされた元の画像（ゲーム画面全体）
- **`images/cropped_cards/`** : 透過処理を行う前の、イラスト部分の切り抜き
- **`images/transparent_cards/`** : AIによって背景が透過された最終画像

また、新しいカード名を検出した場合は、自動的に `all_card_names.txt` の末尾に追加し、これも同時にGitHubへPushして更新します。

## 📁 リポジトリ構成

```
AnokoroImageFolder/
├── index.html              # Webアプリ本体
├── style.css               # スタイルシート
├── all_card_names.txt      # カード名辞書（自動更新対応）
├── capture_cards.py        # (旧) スクリーンキャプチャ + OCR
├── temp_crop.py            # (旧) イラスト部分のクロップ
├── temp_rembg.py           # (旧) rembgによる背景透過
├── temp_fade.py            # (旧) エッジフェード処理
└── images/                 # 画像保存先ディレクトリ群
```

## ⚠️ 注意事項

- **初回のAI処理**: ブラウザ上でAIモデル（約40MB）をロードするため、最初の1枚目の処理には数秒〜十数秒の時間がかかります（プログレスが表示されます）。
- **PATの保存**: GitHub PATはブラウザの `localStorage` にのみ保存され、外部には送信されません。共有PC等では使用後に「クリア」ボタンを押してください。
