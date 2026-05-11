import streamlit as st
import anthropic

# 1. 페이지 설정
st.set_page_config(page_title="Claude AI 질문 앱", page_icon="🌸", layout="centered")

# 2. 커스텀 CSS - 화사한 디자인 적용
st.markdown("""
<style>
    /* 전체 배경 그라데이션 */
    .stApp {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 25%, #ffeaa7 50%, #dfe6e9 75%, #a29bfe 100%);
        background-attachment: fixed;
    }
    
    /* 메인 타이틀 스타일 */
    .main-title {
        text-align: center;
        font-size: 2.8em;
        font-weight: 900;
        background: linear-gradient(90deg, #e84393, #f39c12, #e74c3c, #9b59b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 5px;
    }

    /* 서브타이틀 */
    .sub-title {
        text-align: center;
        color: #636e72;
        font-size: 1.1em;
        margin-bottom: 30px;
    }
    
    /* 카드 스타일 박스 */
    .card-box {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px 30px;
        margin: 15px 0;
        border: 2px solid rgba(255, 182, 193, 0.5);
        box-shadow: 0 8px 32px rgba(232, 67, 147, 0.1);
    }
    
    /* 섹션 헤더 */
    .section-header {
        font-size: 1.3em;
        font-weight: 700;
        color: #e84393;
        margin-bottom: 10px;
    }

    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(90deg, #f093fb, #f5576c, #fda085) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 12px 40px !important;
        font-size: 1.1em !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.5) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(240, 147, 251, 0.7) !important;
    }

    /* 텍스트 입력 영역 */
    .stTextArea > div > div > textarea {
        border-radius: 15px !important;
        border: 2px solid #f093fb !important;
        background: rgba(255, 255, 255, 0.9) !important;
        font-size: 1em !important;
        padding: 12px !important;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: #e84393 !important;
        box-shadow: 0 0 0 3px rgba(232, 67, 147, 0.2) !important;
    }

    /* 셀렉트박스 */
    .stSelectbox > div > div {
        border-radius: 15px !important;
        border: 2px solid #f093fb !important;
        background: rgba(255, 255, 255, 0.9) !important;
    }

    /* 말투 선택 라디오 버튼 영역 */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.5);
        border-radius: 15px;
        padding: 10px;
        gap: 10px;
    }
    .stRadio > div > label {
        background: rgba(255, 255, 255, 0.8) !important;
        border-radius: 12px !important;
        padding: 8px 16px !important;
        border: 2px solid rgba(240, 147, 251, 0.4) !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    .stRadio > div > label:hover {
        border-color: #e84393 !important;
        background: rgba(232, 67, 147, 0.1) !important;
    }

    /* 답변 영역 */
    .answer-box {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(253, 160, 133, 0.15));
        border-radius: 20px;
        padding: 25px;
        border-left: 5px solid #e84393;
        border: 2px solid rgba(232, 67, 147, 0.3);
        box-shadow: 0 8px 32px rgba(232, 67, 147, 0.1);
        margin-top: 15px;
    }

    /* 메트릭 커스텀 스타일 */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 15px;
        padding: 15px;
        border: 2px solid rgba(162, 155, 254, 0.4);
        box-shadow: 0 4px 15px rgba(162, 155, 254, 0.2);
    }

    /* 구분선 스타일 */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #f093fb, #f5576c, transparent);
        margin: 20px 0;
    }

    /* 말투 미리보기 박스 */
    .preview-box {
        background: linear-gradient(135deg, rgba(162,155,254,0.15), rgba(240,147,251,0.15));
        border-radius: 12px;
        padding: 12px 18px;
        border: 1px dashed rgba(162, 155, 254, 0.6);
        font-size: 0.9em;
        color: #636e72;
        margin-top: 10px;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# 3. 타이틀 영역
st.markdown("""
<div style="text-align:center; padding: 20px 0;">
    <div class="main-title">🌸 Claude AI 질문 앱 🌸</div>
    <div class="sub-title">✨ 무엇이든 물어보세요! AI가 친절하게 답해드려요 ✨</div>
</div>
""", unsafe_allow_html=True)

# 4. API 키 불러오기
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=api_key)
except KeyError:
    st.error("🔑 API 키가 설정되지 않았습니다. Streamlit Cloud의 'Secrets' 설정에서 `ANTHROPIC_API_KEY`를 추가해주세요.")
    st.stop()

# 5. 말투 설정 딕셔너리 (시스템 프롬프트 포함)
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
            "항상 격식 있는 존댓말을 사용하고, 명확하고 체계적으로 답변하세요. "
            "고객을 존중하는 태도로 친절하게 응대해 주세요."
        )
    },
    "🎓 똑똑한 선생님": {
        "description": "차분하고 이해하기 쉽게 설명해드려요",
        "preview": "\"좋은 질문이에요! 단계별로 함께 살펴볼까요? 📚\"",
        "system_prompt": (
            "당신은 친절하고 지식이 풍부한 선생님입니다. "
            "어려운 개념을 쉬운 언어로 단계적으로 설명하고, "
            "예시를 들어 이해를 돕는 방식으로 답변하세요. "
            "학생이 스스로 이해할 수 있도록 격려하는 말투를 사용하세요."
        )
    },
    "😄 유쾌한 개그맨": {
        "description": "유머와 재치로 웃으면서 배워요",
        "preview": "\"오~ 이거 완전 꿀잼 질문인데요?! 빵 터지게 설명해드림 ㅋㅋ 🎤\"",
        "system_prompt": (
            "너는 유쾌하고 재치 있는 AI야. "
            "답변할 때 적절한 유머와 재미있는 표현을 섞어서 웃음을 주면서 설명해줘. "
            "하지만 핵심 내용은 정확하게 전달해야 해. "
            "이모지를 많이 활용하고 밝고 에너지 넘치는 말투를 써줘!"
        )
    },
    "🤖 냉철한 AI": {
        "description": "감정 없이 핵심만 간결하게 전달해요",
        "preview": "\"분석 완료. 핵심 정보를 전달합니다. [결론]: ...\"",
        "system_prompt": (
            "당신은 감정 없이 논리적이고 냉철하게 답변하는 AI입니다. "
            "불필요한 감정 표현이나 수식어 없이 핵심만 간결하게 전달하세요. "
            "데이터와 사실에 기반하여 답변하고, 번호나 구조적 형식을 활용하세요."
        )
    },
    "🌟 응원하는 코치": {
        "description": "긍정적이고 열정적으로 용기를 북돋아줘요",
        "preview": "\"와, 정말 대단한 질문이에요! 당신은 할 수 있어요! 💪🔥\"",
        "system_prompt": (
            "당신은 열정적이고 긍정적인 코치 AI입니다. "
            "항상 상대방을 격려하고 응원하는 말투로 답변하세요. "
            "어떤 질문이든 칭찬으로 시작하고, 할 수 있다는 자신감을 심어주세요. "
            "에너지 넘치고 밝은 표현과 이모지를 적극 활용하세요! 💪"
        )
    },
}

# 6. 모델 선택 카드
st.markdown('<div class="card-box">', unsafe_allow_html=True)
st.markdown('<div class="section-header">⚙️ AI 모델 설정</div>', unsafe_allow_html=True)
model_options = {
    "🚀 Claude Sonnet - 빠르고 균형 잡힌 성능": "claude-sonnet-4-5",
    "💎 Claude Opus - 최고 수준의 강력한 성능": "claude-opus-4-5"
}
selected_model_label = st.selectbox(
    "모델 선택:",
    list(model_options.keys()),
    label_visibility="collapsed"
)
selected_model_id = model_options[selected_model_label]
st.markdown('</div>', unsafe_allow_html=True)

# 7. 말투 선택 카드 ⭐ 새로 추가된 기능!
st.markdown('<div class="card-box">', unsafe_allow_html=True)
st.markdown('<div class="section-header">🎭 AI 말투 선택</div>', unsafe_allow_html=True)
st.caption("AI가 어떤 스타일로 답변해줬으면 좋겠나요?")

selected_tone = st.radio(
    "말투 선택:",
    list(TONE_OPTIONS.keys()),
    horizontal=True,
    label_visibility="collapsed"
)

# 선택된 말투 미리보기
tone_info = TONE_OPTIONS[selected_tone]
st.markdown(f"""
<div class="preview-box">
    📝 <b>{tone_info['description']}</b><br>
    💬 예시: {tone_info['preview']}
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 8. 질문 입력 카드
st.markdown('<div class="card-box">', unsafe_allow_html=True)
st.markdown('<div class="section-header">💬 질문 입력</div>', unsafe_allow_html=True)
user_input = st.text_area(
    "질문 입력:",
    height=160,
    placeholder="🌟 궁금한 것을 자유롭게 입력해보세요!\n예) 파이썬에서 리스트와 튜플의 차이가 뭔가요?",
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# 9. 버튼 및 응답 처리
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    ask_button = st.button("🌸 답변 받기 🌸", type="primary")

if ask_button:
    if not user_input.strip():
        st.warning("💡 질문을 먼저 입력해주세요!")
    else:
        with st.spinner(f"🌈 [{selected_tone}] 말투로 답변을 만들고 있어요... 잠깐만요!"):
            try:
                # 선택된 말투의 시스템 프롬프트 가져오기
                system_prompt = tone_info["system_prompt"]

                response = client.messages.create(
                    model=selected_model_id,
                    max_tokens=4096,
                    system=system_prompt,   # ⭐ 말투 시스템 프롬프트 적용
                    messages=[
                        {"role": "user", "content": user_input}
                    ]
                )

                # 구분선
                st.markdown("<hr>", unsafe_allow_html=True)

                # 적용된 말투 표시
                st.markdown(f"""
                <div style="text-align:center; margin-bottom:10px;">
                    <span style="background: linear-gradient(90deg,#f093fb,#f5576c);
                                 color:white; border-radius:20px; padding:5px 18px;
                                 font-size:0.9em; font-weight:700;">
                        {selected_tone} 말투로 답변 중
                    </span>
                </div>
                """, unsafe_allow_html=True)

                # 답변 출력
                st.markdown('<div class="section-header">✨ AI 답변</div>', unsafe_allow_html=True)
                st.markdown('<div class="answer-box">', unsafe_allow_html=True)
                st.write(response.content[0].text)
                st.markdown('</div>', unsafe_allow_html=True)

                # 구분선
                st.markdown("<hr>", unsafe_allow_html=True)

                # 토큰 사용량
                st.markdown('<div class="section-header">📊 API 사용량</div>', unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                col1.metric("📥 입력 토큰", f"{response.usage.input_tokens:,} 개")
                col2.metric("📤 출력 토큰", f"{response.usage.output_tokens:,} 개")
                col3.metric("🔢 총합", f"{response.usage.input_tokens + response.usage.output_tokens:,} 개")

                # 완료 메시지
                st.success(f"🎉 {selected_tone} 말투로 답변이 완성되었어요! 도움이 되셨으면 좋겠어요 💖")

            except Exception as e:
                st.error(f"😢 API 호출 중 오류가 발생했습니다: {e}")

# 10. 푸터
st.markdown("""
<div style="text-align:center; margin-top:40px; color:#b2bec3; font-size:0.85em;">
    🌸 Made with ❤️ using Streamlit & Claude AI 🌸
</div>
""", unsafe_allow_html=True)
