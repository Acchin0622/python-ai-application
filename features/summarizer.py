import streamlit as st

from utils.gemini_client import generate_text, validate_input_length

SYSTEM_PROMPT = """あなたは要約のスペシャリストです。
元の文章の意図と重要情報を損なわず、指定された形式で過不足なく要約してください。"""


def render() -> None:
    st.header("📄 文章要約AI")
    st.caption("長文を貼り付けて、好みの形式で要約します。")

    with st.form("summary_form"):
        text = st.text_area("要約したい文章", height=300, placeholder="ここに記事・議事録・論文などを貼り付けてください。")
        style = st.radio(
            "要約スタイル",
            ["3行要約", "箇条書き（5項目）", "詳細な要約（300〜500字）", "TL;DR + キーポイント"],
            horizontal=False,
        )
        language = st.selectbox("出力言語", ["日本語", "英語"])
        submitted = st.form_submit_button("要約する", type="primary")

    if submitted:
        if not text.strip():
            st.warning("要約する文章を入力してください。")
            return

        is_valid, warning = validate_input_length(text)
        if not is_valid:
            st.error(warning)
            return
        if warning:
            st.warning(warning)

        prompt = f"""以下の文章を要約してください。

# 元の文章
{text}

# 要約スタイル
{style}

# 出力言語
{language}

指定されたスタイルに厳密に従って出力してください。
"""
        with st.spinner("要約中..."):
            try:
                result = generate_text(prompt, system_instruction=SYSTEM_PROMPT, temperature=0.3)
            except Exception as e:
                st.error(f"生成に失敗しました: {e}")
                return

        st.success("要約完了")
        st.markdown(result)

        original_len = len(text)
        summary_len = len(result)
        ratio = (summary_len / original_len * 100) if original_len else 0
        st.caption(f"元の文字数: {original_len} / 要約後: {summary_len} （圧縮率 {ratio:.1f}%）")
