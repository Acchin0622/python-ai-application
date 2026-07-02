# AIライティングツール（個人用 MVP）

Python + Streamlit + Gemini API で動く、個人用のAIライティングツールです。

## 機能（MVP）

- 📝 **ブログ記事執筆AI** — テーマ・読者・トーン・文字数を指定して記事を生成
- ✉️ **メール返信AI** — 受信メールと返信意図から、整った返信文を生成
- 📄 **文章要約AI** — 3行 / 箇条書き / 詳細 / TL;DR の4スタイルで要約

## セットアップ

### 1. Gemini APIキーを取得

[Google AI Studio](https://aistudio.google.com/app/apikey) で無料の API キーを発行します。

### 2. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 3. APIキーの設定

`.env.example` をコピーして `.env` を作成し、取得したキーを記入します。

```bash
copy .env.example .env
```

`.env` の中身：

```
GEMINI_API_KEY=ここにキーを貼り付け
```

### 4. 起動

```bash
streamlit run app.py
```

ブラウザで `http://localhost:8501` が開きます。サイドバーから機能を選択してください。

## ディレクトリ構成

```
.
├── app.py                  Streamlit エントリポイント
├── config.py               APIキー・モデル設定
├── requirements.txt
├── .env.example
├── features/
│   ├── blog_writer.py
│   ├── email_reply.py
│   └── summarizer.py
└── utils/
    └── gemini_client.py    Gemini API 共通ラッパー
```

## 使用モデル

デフォルトは `gemini-2.5-flash`（高速・低コスト）。変更する場合は `config.py` の `DEFAULT_MODEL` を編集してください。
