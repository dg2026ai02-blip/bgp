import streamlit as st
import anthropic

# 1. 페이지 설정
st.set_page_config(page_title="Claude AI 질문 앱", page_icon="🤍", layout="centered")

# 2. 커스텀 CSS - 차분한 디자인
st.markdown("""
<style>
    /* 전체 배경 - 차분한 그레이 베이지 */
    .stApp {
        background: #f0ede8;
    }

    /* 메인 타이틀 */
    .main-title {
        text-align: center;
        font-size: 2.2em;
        font-weight: 800;
        color: #2c2c2c;
        margin-bottom: 5px;
        letter-spacing: -0.5px;
    }

    /* 서브타이틀 */
    .sub-title {
        text-align: center;
        color: #6b6b6b;
        font-size: 0.95em;
        margin-bottom: 30px;
    }

    /* 카드 박스 */
    .card-box {
        background: #ffffff;
        border-radius: 14px;
        padding: 22px 26px;
        margin: 12px 0;
        border: 1px solid #e0dbd4;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    /* 섹션 헤더 */
    .section-header {
        font-size: 1.05em;
        font-weight: 700;
        color: #2c2c2c;
        margin-bottom: 10px;
    }

    /* 버튼 */
    .stButton > button {
        background: #3d3d3d !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 30px !important;
        font-size: 1em !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15) !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background: #1a1a1a !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
        transform: translateY(-1px) !important;
    }

    /* 텍스트 입력 영역 */
    .stTextArea > div > div > textarea {
        border-radius: 10px !important;
        border: 1.5px solid #d4cfc9 !important;
        background: #fafaf9 !important;
        font-size: 0.97em !important;
        padding: 12px !important;
        color: #1a1a1a !important;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: #8a8a8a !important;
        box-shadow: 0 0 0 2px rgba(100,100,100,0.15) !important;
    }

    /* 셀렉트박스 */
    .stSelectbox > div > div {
        border-radius: 10px !important;
        border: 1.5px solid #d4cfc9 !important;
        background: #fafaf9 !important;
        color: #1a1a1a !important;
    }

    /* 라디오 버튼 */
    .stRadio > div {
        gap: 8px;
    }
    .stRadio > div > label {
        background: #f5f3f0 !important;
        border-radius: 10px !important;
        padding: 7px 14px !important;
        border: 1.5px solid #e0dbd4 !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        color: #2c2c2c !important;
        font-size: 0.9em !important;
    }
    .stRadio > div > label:hover {
        border-color: #8a8a8a !important;
        background: #eeebe6 !important;
    }

    /* 답변 영역 */
    .answer-box {
        background: #fafaf9;
        border-radius: 12px;
        padding: 22px;
        border: 1px solid #e0dbd4;
        margin-top: 12px;
        color: #1a1a1a;
        line-height: 1.75;
    }

    /* 대화 기록 - 사용자 메시지 */
    .chat-user {
        background: #eeebe6;
        border-radius: 12px 12px 4px 12px;
        padding: 12px 16px;
        margin: 8px 0;
        color: #1a1a1a;
        font-size: 0.95em;
        max-width: 85%;
        margin-left: auto;
        border: 1px solid #dedad4;
    }

    /* 대화 기록 - AI 메시지 */
    .chat-ai {
        background: #ffffff;
        border-radius: 12px 12px 12px 4px;
        padding: 12px 16px;
        margin: 8px 0;
        color: #1a1a1a;
        font-size: 0.95em;
        max-width: 85%;
        border: 1px solid #e0dbd4;
        line-height: 1.7;
    }

    /* 메트릭 */
    [data-testid="stMetric"] {
        background: #ffffff;
        border-radius: 10px;
        padding: 12px;
        border: 1px solid #e0dbd4;
    }
    [data-testid="stMetric"] label,
    [data-testid="stMetric"] div {
        color: #1a1a1a !important;
    }

    /* 구분선 */
    hr {
        border: none;
        height: 1px;
        background: #e0dbd4;
        margin: 18px 0;
    }

    /* 미리보기 박스 */
    .preview-box {
        background: #f5f3f0;
        border-radius: 10px;
        padding: 10px 15px;
        border: 1px solid #e0dbd4;
        font-size: 0.88em;
        color: #4a4a4a;
        margin-top: 10px;
    }

    /* 말투 배지 */
    .tone-badge {
        display: inline-block;
        background: #3d3d3d;
        color: white;
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.82em;
        font-weight: 600;
    }

    /* 대화 기록 날짜/시간 */
    .chat-meta {
        font-size: 0.75em;
        color: #9a9a9a;
        margin: 4px 0 2px 0;
    }

    /* 전체 텍스트 */
    p, span, div, label {
        color: #1a1a1a;
    }

    .stCaption {
        color: #6b6b6b !important;
    }

    .stAlert p {
        color: #1a1a1a !important;
    }

    /* 사이드바 */
    [data-testid="stSidebar"] {
        background: #e8e4de;
        border-right: 1px solid #d4cfc9;
    }

    /* 사이드바 버튼 */
    [data-testid="stSidebar"] .stButton > button {
        background: #ffffff !important;
        color: #2c2c2c !important;
        border: 1px solid #d4cfc9 !important;
        font-size: 0.85em !important;
        text-align: left !important;
        padding: 8px 14px !important;
        margin: 2px 0 !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: #dedad4 !important;
        border-color: #8a8a8a !important;
    }

    /* 삭제 버튼 */
    .delete-btn > button {
        background: #f5f0ee !important;
        color: #c0392b !important;
        border: 1px solid #e8d5d3 !important;
        font-size: 0.8em !important;
        padding: 4px 10px !important;
        width: auto !important;
    }
    .delete-btn > button:hover {
        background: #fae8e6 !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. 세션 상태 초기화
if "conversations" not in st.session_state:
    st.session_state.conversations = {}     # { 대화ID: { title, messages, tone, model } }
if "current_conv_id" not in st.session_state:
    st.session_state.current_conv_id = None
if "next_id" not in st.session_state:
    st.session_state.next_id = 1

# 4. API 키 불러오기
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=api_key)
except KeyError:
    st.error("🔑 API 키가 설정되지 않았습니다.")
    st.stop()

# 5. 말투 설정
TONE_OPTIONS = {
    "🤝 친근한 친구": {
        "description": "편하고 친근하게 반말로 대화해요",
        "preview": "\"야, 그거 완전 쉬워! 내가 설명해줄게~ 😄\"",
        "system_prompt": (
            "너는 친한 친구처럼 편하게 반말로 대화하는 AI야. "
            "이모지를 적절히 사용하고, 쉽고 재미있게 설명해줘. "
            "딱딱한 표현은 피하고 자연스럽고 따뜻하게 답해줘."
        )
    },
    "👔 정중한 비서": {
        "description": "예의 바르고 격식 있는 존댓말로 안내해드려요",
        "preview": "\"네, 고객님. 해당 내용에 대해 자세히 안내해 드리겠습니다.\"",
        "system_prompt": (
            "당신은 정중하고 전문적인 AI 비서입니다. "
            "항상 격식 있는 존댓말을 사용하고, 명확하고 체계적으로 답변하세요."
        )
    },
    "🎓 똑똑한 선생님": {
        "description": "차분하고 이해하기 쉽게 설명해드려요",
        "preview": "\"좋은 질문이에요! 단계별로 함께 살펴볼까요? 📚\"",
        "system_prompt": (
            "당신은 친절하고 지식이 풍부한 선생님입니다. "
            "어려운 개념을 쉬운 언어로 단계적으로 설명하고, "
            "예시를 들어 이해를 돕는 방식으로 답변하세요."
        )
    },
    "😄 유쾌한 개그맨": {
        "description": "유머와 재치로 웃으면서 배워요",
        "preview": "\"오~ 이거 완전 꿀잼 질문인데요?! ㅋㅋ 🎤\"",
        "system_prompt": (
            "너는 유쾌하고 재치 있는 AI야. "
            "답변할 때 적절한 유머와 재미있는 표현을 섞어서 설명해줘. "
            "하지만 핵심 내용은 정확하게 전달해야 해."
        )
    },
    "🤖 냉철한 AI": {
        "description": "감정 없이 핵심만 간결하게 전달해요",
        "preview": "\"분석 완료. 핵심 정보를 전달합니다.\"",
        "system_prompt": (
            "당신은 감정 없이 논리적이고 냉철하게 답변하는 AI입니다. "
            "불필요한 감정 표현 없이 핵심만 간결하게 전달하세요."
        )
    },
    "🌟 응원하는 코치": {
        "description": "긍정적이고 열정적으로 용기를 북돋아줘요",
        "preview": "\"와, 정말 대단한 질문이에요! 당신은 할 수 있어요! 💪\"",
        "system_prompt": (
            "당신은 열정적이고 긍정적인 코치 AI입니다. "
            "항상 상대방을 격려하고 응원하는 말투로 답변하세요."
        )
    },
}

# 6. 모델 옵션
MODEL_OPTIONS = {
    "Claude Sonnet — 균형 잡힌 성능": "claude-sonnet-4-5",
    "Claude Opus — 최고 성능": "claude-opus-4-5"
}

# ────────────────────────────────────────────
# 7. 사이드바 — 대화 기록 목록
# ────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 💬 대화 목록")

    # 새 대화 시작 버튼
    if st.button("＋ 새 대화 시작", key="new_conv"):
        st.session_state.current_conv_id = None
        st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    if not st.session_state.conversations:
        st.caption("아직 저장된 대화가 없어요.")
    else:
        # 최신순 정렬
        sorted_convs = sorted(
            st.session_state.conversations.items(),
            key=lambda x: x[0],
            reverse=True
        )
        for conv_id, conv_data in sorted_convs:
            col_title, col_del = st.columns([5, 1])
            with col_title:
                label = f"{'▶ ' if conv_id == st.session_state.current_conv_id else ''}{conv_data['title']}"
                if st.button(label, key=f"conv_{conv_id}"):
                    st.session_state.current_conv_id = conv_id
                    st.rerun()
            with col_del:
                st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
                if st.button("🗑", key=f"del_{conv_id}"):
                    del st.session_state.conversations[conv_id]
                    if st.session_state.current_conv_id == conv_id:
                        st.session_state.current_conv_id = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# ────────────────────────────────────────────
# 8. 메인 영역
# ────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 18px 0 8px 0;">
    <div class="main-title">Claude AI 질문 앱</div>
    <div class="sub-title">궁금한 것을 무엇이든 물어보세요</div>
</div>
""", unsafe_allow_html=True)

# 현재 대화 불러오기
current_conv = None
if st.session_state.current_conv_id is not None:
    current_conv = st.session_state.conversations.get(st.session_state.current_conv_id)

# ── 기존 대화 내용 표시
if current_conv and current_conv["messages"]:
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">📂 {current_conv["title"]}</div>', unsafe_allow_html=True)
    st.caption(f"말투: {current_conv['tone']}  |  모델: {current_conv['model_label']}")
    st.markdown("<hr>", unsafe_allow_html=True)

    for msg in current_conv["messages"]:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-meta" style="text-align:right;">나</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-meta">AI · {current_conv["tone"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-ai">{msg["content"]}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

# ── 설정 카드 (새 대화이거나 대화가 없을 때만 표시)
if current_conv is None:
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">⚙️ 모델 설정</div>', unsafe_allow_html=True)
    selected_model_label = st.selectbox(
        "모델 선택:",
        list(MODEL_OPTIONS.keys()),
        label_visibility="collapsed"
    )
    selected_model_id = MODEL_OPTIONS[selected_model_label]
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🎭 말투 선택</div>', unsafe_allow_html=True)
    st.caption("AI가 어떤 스타일로 답변할까요?")
    selected_tone = st.radio(
        "말투:",
        list(TONE_OPTIONS.keys()),
        horizontal=True,
        label_visibility="collapsed"
    )
    tone_info = TONE_OPTIONS[selected_tone]
    st.markdown(f"""
    <div class="preview-box">
        <b>{tone_info['description']}</b><br>
        예시: {tone_info['preview']}
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # 기존 대화 이어가기 — 설정 고정 표시
    selected_model_id = current_conv["model_id"]
    selected_model_label = current_conv["model_label"]
    selected_tone = current_conv["tone"]
    tone_info = TONE_OPTIONS[selected_tone]

# ── 질문 입력 카드
st.markdown('<div class="card-box">', unsafe_allow_html=True)
st.markdown('<div class="section-header">✏️ 질문 입력</div>', unsafe_allow_html=True)
user_input = st.text_area(
    "질문:",
    height=140,
    placeholder="궁금한 것을 입력해보세요.\n예) 파이썬에서 리스트와 튜플의 차이가 뭔가요?",
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# ── 답변 받기 버튼
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    ask_button = st.button("답변 받기", type="primary")

# ── API 호출 및 응답 처리
if ask_button:
    if not user_input.strip():
        st.warning("질문을 먼저 입력해주세요.")
    else:
        with st.spinner("답변을 생성하고 있어요..."):
            try:
                # 현재 대화의 메시지 히스토리 구성
                if current_conv:
                    history = current_conv["messages"]
                else:
                    history = []

                api_messages = history + [{"role": "user", "content": user_input}]

                response = client.messages.create(
                    model=selected_model_id,
                    max_tokens=4096,
                    system=tone_info["system_prompt"],
                    messages=api_messages
                )

                ai_reply = response.content[0].text

                # ── 대화 저장
                if current_conv is None:
                    # 새 대화 생성
                    conv_id = st.session_state.next_id
                    st.session_state.next_id += 1
                    title = user_input[:20] + ("..." if len(user_input) > 20 else "")
                    st.session_state.conversations[conv_id] = {
                        "title": title,
                        "tone": selected_tone,
                        "model_id": selected_model_id,
                        "model_label": selected_model_label,
                        "messages": [
                            {"role": "user", "content": user_input},
                            {"role": "assistant", "content": ai_reply}
                        ]
                    }
                    st.session_state.current_conv_id = conv_id
                else:
                    # 기존 대화에 추가
                    st.session_state.conversations[st.session_state.current_conv_id]["messages"].append(
                        {"role": "user", "content": user_input}
                    )
                    st.session_state.conversations[st.session_state.current_conv_id]["messages"].append(
                        {"role": "assistant", "content": ai_reply}
                    )

                st.rerun()

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

# 푸터
st.markdown("""
<div style="text-align:center; margin-top:40px; color:#9a9a9a; font-size:0.8em;">
    Claude AI · Streamlit
</div>
""", unsafe_allow_html=True)
