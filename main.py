import streamlit as st
import anthropic

# 1. 페이지 설정
st.set_page_config(page_title="Claude AI 질문 앱", page_icon="🤖", layout="centered")
st.title("Claude AI 질의응답 앱 🤖")

# 2. API 키 불러오기 (Streamlit Secrets 활용)
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=api_key)
except KeyError:
    st.error("API 키가 설정되지 않았습니다. Streamlit Cloud의 'Secrets' 설정에서 `ANTHROPIC_API_KEY`를 추가해주세요.")
    st.stop()

# 3. 모델 선택
st.markdown("### ⚙️ 설정")
model_options = {
    "Claude 4.6 Sonnet (속도와 성능의 균형)": "claude-4-6-sonnet-latest",
    "Claude 4.6 Opus (최고 수준의 성능)": "claude-4-6-opus-latest"
    # 참고: 실제 Anthropic API 업데이트에 따라 위 model ID 문자열은 변경될 수 있습니다.
}
selected_model_label = st.selectbox("사용할 AI 모델을 선택하세요:", list(model_options.keys()))
selected_model_id = model_options[selected_model_label]

# 4. 사용자 입력
st.markdown("### 💬 질문하기")
user_input = st.text_area("AI에게 물어볼 내용을 입력하세요:", height=150, placeholder="여기에 질문을 입력하세요...")

# 5. 실행 버튼 및 AI 응답 처리
if st.button("답변 받기", type="primary"):
    if not user_input.strip():
        st.warning("질문을 먼저 입력해주세요!")
    else:
        with st.spinner("AI가 답변을 생성하고 있습니다... 잠시만 기다려주세요."):
            try:
                # Claude API 호출
                response = client.messages.create(
                    model=selected_model_id,
                    max_tokens=4096, # 필요에 따라 최대 출력 토큰 수 조절
                    messages=[
                        {"role": "user", "content": user_input}
                    ]
                )
                
                # 답변 출력
                st.markdown("---")
                st.markdown("### ✨ AI 답변")
                st.write(response.content[0].text)
                
                # 사용량(토큰) 출력
                st.markdown("---")
                st.markdown("### 📊 API 사용량")
                col1, col2, col3 = st.columns(3)
                col1.metric("입력 토큰 (Input)", f"{response.usage.input_tokens:,} 개")
                col2.metric("출력 토큰 (Output)", f"{response.usage.output_tokens:,} 개")
                col3.metric("총합", f"{response.usage.input_tokens + response.usage.output_tokens:,} 개")

            except Exception as e:
                st.error(f"API 호출 중 오류가 발생했습니다: {e}")
