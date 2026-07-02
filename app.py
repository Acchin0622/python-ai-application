import streamlit as st

from config import GEMINI_API_KEY
from features import blog_writer, email_reply, summarizer

st.set_page_config(page_title="AIライティングツール", page_icon="✍️", layout="wide")

st.sidebar.title("✍️ AIライティングツール")
st.sidebar.markdown("---")

MENU = {
    "📝 ブログ記事執筆": blog_writer,
    "✉️ メール返信": email_reply,
    "📄 文章要約": summarizer,
}

choice = st.sidebar.radio("機能を選択", list(MENU.keys()))

st.sidebar.markdown("---")
if GEMINI_API_KEY:
    st.sidebar.success("Gemini API: 接続OK")
else:
    st.sidebar.error("GEMINI_API_KEY 未設定\n.env ファイルを確認してください。")

st.sidebar.caption("Powered by Google Gemini")

MENU[choice].render()
