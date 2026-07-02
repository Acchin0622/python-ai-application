import streamlit as st

from utils.gemini_client import generate_text

SYSTEM_PROMPT = """あなたはプロのブログライターです。
読者にとって価値があり、読みやすく、SEOにも配慮したブログ記事を執筆してください。
見出し（##）、小見出し（###）、箇条書きを適切に使い、構造的にまとめます。"""


def render() -> None:
    st.header("📝 ブログ記事執筆AI")
    st.caption("テーマとトーンを指定すると、構成済みのブログ記事を生成します。")

    with st.form("blog_form"):
        topic = st.text_input("テーマ / タイトル案", placeholder="例: 初心者向けPython学習ロードマップ")
        target = st.text_input("想定読者", placeholder="例: プログラミング初心者の社会人")
        tone = st.selectbox(
            "トーン",
            ["フレンドリー", "丁寧・ビジネス調", "専門的・解説調", "カジュアル"],
        )
        length = st.select_slider(
            "目安の文字数",
            options=["800字", "1500字", "2500字", "4000字"],
            value="1500字",
        )
        keywords = st.text_input("含めたいキーワード（任意・カンマ区切り）", placeholder="例: 独学, 副業, 学習法")
        submitted = st.form_submit_button("記事を生成", type="primary")

    if submitted:
        if not topic.strip():
            st.warning("テーマを入力してください。")
            return

        prompt = f"""以下の条件でブログ記事を作成してください。

# テーマ
{topic}

# 想定読者
{target or "一般読者"}

# トーン
{tone}

# 目安の文字数
{length}

# 含めたいキーワード
{keywords or "（指定なし）"}

出力は Markdown 形式で、導入・本文（複数セクション）・まとめの構成にしてください。
"""
        with st.spinner("記事を生成中..."):
            try:
                result = generate_text(prompt, system_instruction=SYSTEM_PROMPT, temperature=0.8)
            except Exception as e:
                st.error(f"生成に失敗しました: {e}")
                return

        st.success("生成完了")
        st.markdown(result)
        st.download_button("Markdownでダウンロード", result, file_name="blog_article.md")
