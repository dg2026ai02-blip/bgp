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
        text-shadow: none;
        margin-bottom: 5px;
        animation: shimmer 3s infinite;
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

    /* 메트릭 카드 */
    .metric-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 15px;
        padding: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
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

    /* 경고/오류 메시지 */
    .stAlert {
        border-radius: 15px !important;
    }

    /* 스피너 색상 */
    .stSpinner > div {
        border-top-color: #e84393 !important;
    }

    /* 장식용 이모지 애니메이션 */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    .floating {
        display: inline-block;
        animation: float 3s ease-in-out infinite;
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

# 5. 모델 선택 카드
st.markdown('<div class="card-box">', unsafe_allow_html=True)
st.markdown('<div class="section-header">⚙️ AI 모델 설정</div>', unsafe_allow_html=True)

model_options = {
    "🚀 Claude Sonnet - 빠르고 균형 잡힌 성능": "claude-sonnet-4-5",
    "💎 Claude Opus - 최고 수준의 강력한 성능": "claude-opus-4-5"
}
selected_model_label = st.selectbox(
    "사용할 AI 모델을 선택하세요:",
    list(model_options.keys()),
    label_visibility="collapsed"
)
selected_model_id = model_options[selected_model_label]
st.markdown('</div>', unsafe_allow_html=True)

# 6. 질문 입력 카드
st.markdown('<div class="card-box">', unsafe_allow_html=True)
st.markdown('<div class="section-header">💬 질문 입력</div>', unsafe_allow_html=True)
user_input = st.text_area(
    "AI에게 물어볼 내용:",
    height=160,
    placeholder="🌟 궁금한 것을 자유롭게 입력해보세요!\n예) 파이썬에서 리스트와 튜플의 차이가 뭔가요?",
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# 7. 버튼 및 응답 처리
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    ask_button = st.button("🌸 답변 받기 🌸", type="primary")

if ask_button:
    if not user_input.strip():
        st.warning("💡 질문을 먼저 입력해주세요!")
    else:
        with st.spinner("🌈 AI가 열심히 답변을 만들고 있어요... 잠깐만요!"):
            try:
                response = client.messages.create(
                    model=selected_model_id,
                    max_tokens=4096,
                    messages=[
                        {"role": "user", "content": user_input}
                    ]
                )

                # 구분선
                st.markdown("<hr>", unsafe_allow_html=True)

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
                st.success("🎉 답변이 완성되었어요! 도움이 되셨으면 좋겠어요 💖")

            except Exception as e:
                st.error(f"😢 API 호출 중 오류가 발생했습니다: {e}")

# 푸터
st.markdown("""
<div style="text-align:center; margin-top:40px; color:#b2bec3; font-size:0.85em;">
    🌸 Made with ❤️ using Streamlit & Claude AI 🌸
</div>
""", unsafe_allow_html=True)
