import streamlit as st

from utils.gemini_client import generate_text, validate_input_length

SYSTEM_PROMPT = """あなたは熟練のビジネスアシスタントです。
受信したメールに対して、相手との関係性と返信意図を踏まえた自然で適切な返信文を作成します。
日本のビジネスマナー（宛名、挨拶、結びなど）を遵守してください。"""


def render() -> None:
    st.header("✉️ メール返信AI")
    st.caption("受信メールと返信したい内容を入力すると、整った返信文を生成します。")

    with st.form("email_form"):
        received = st.text_area(
            "受信したメール本文",
            height=200,
            placeholder="ここに相手から届いたメール本文を貼り付けてください。",
        )
        intent = st.text_area(
            "返信したい内容・意図",
            height=100,
            placeholder="例: 来週の打ち合わせを水曜10時に変更したい旨を丁寧に伝えたい",
        )
        relation = st.selectbox(
            "相手との関係",
            ["社外の取引先", "社内の上司", "社内の同僚・部下", "初対面・新規問い合わせ", "顧客（カスタマー対応）"],
        )
        tone = st.selectbox(
            "トーン",
            ["丁寧・フォーマル", "標準的なビジネス", "ややカジュアル"],
        )
        sender_name = st.text_input("自分の署名に使う名前（任意）", placeholder="例: 山田太郎")
        submitted = st.form_submit_button("返信文を生成", type="primary")

    if submitted:
        if not received.strip() or not intent.strip():
            st.warning("受信メールと返信意図の両方を入力してください。")
            return

        # Validate input length for the received email (intent is usually short)
        is_valid, warning = validate_input_length(received)
        if not is_valid:
            st.error(warning)
            return
        if warning:
            st.warning(warning)

        prompt = f"""以下の受信メールに対する返信文を作成してください。

# 受信メール
{received}

# 返信意図
{intent}

# 相手との関係
{relation}

# トーン
{tone}

# 署名
{sender_name or "（署名は省略）"}

件名・宛名・本文・結び・署名を含む完成形のメールを出力してください。
"""
        with st.spinner("返信文を生成中..."):
            try:
                result = generate_text(prompt, system_instruction=SYSTEM_PROMPT, temperature=0.6)
            except Exception as e:
                st.error(f"生成に失敗しました: {e}")
                return

        st.success("生成完了")
        st.text_area("生成された返信文", result, height=400)
