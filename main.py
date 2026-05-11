import streamlit as st
import anthropic
from datetime import datetime

# ──────────────────────────────────────────
# 1. 페이지 설정
# ──────────────────────────────────────────
st.set_page_config(
    page_title="Claude AI 질문 앱",
    page_icon="🤖",
    layout="wide"
)

st.title("Claude AI 질의응답 앱 🤖")

# ──────────────────────────────────────────
# 2. API 키 불러오기
# ──────────────────────────────────────────
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=api_key)
except KeyError:
    st.error("API 키가 설정되지 않았습니다. Streamlit Cloud의 'Secrets' 설정에서 `ANTHROPIC_API_KEY`를 추가해주세요.")
    st.stop()

# ──────────────────────────────────────────
# 3. 세션 상태 초기화
# ──────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []          # 대화 히스토리
if "total_input_tokens" not in st.session_state:
    st.session_state.total_input_tokens = 0
if "total_output_tokens" not in st.session_state:
    st.session_state.total_output_tokens = 0
if "favorite_prompts" not in st.session_state:
    st.session_state.favorite_prompts = []  # 즐겨찾기 질문
if "last_user_input" not in st.session_state:
    st.session_state.last_user_input = ""

# ──────────────────────────────────────────
# 4. 사이드바 - 설정 패널
# ──────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ 설정")

    # 모델 선택
    model_options = {
        "Claude Sonnet (속도·성능 균형)": "claude-sonnet-4-5",
        "Claude Opus (최고 성능)":        "claude-opus-4-5",
    }
    selected_model_label = st.selectbox(
        "🧠 AI 모델 선택",
        list(model_options.keys())
    )
    selected_model_id = model_options[selected_model_label]

    st.markdown("---")

    # 시스템 프롬프트 설정
    st.subheader("🗂️ 시스템 프롬프트")
    preset_roles = {
        "기본 AI 어시스턴트": "You are a helpful AI assistant. Answer in Korean.",
        "친절한 선생님": "You are a kind and patient teacher. Explain concepts clearly and simply in Korean.",
        "코드 전문가": "You are an expert programmer. Provide clean, well-commented code and explain it in Korean.",
        "창의적인 작가": "You are a creative writer. Help with storytelling and creative writing in Korean.",
        "직접 입력": ""
    }
    selected_role = st.selectbox("역할 프리셋 선택", list(preset_roles.keys()))

    if selected_role == "직접 입력":
        system_prompt = st.text_area(
            "시스템 프롬프트 직접 입력",
            height=100,
            placeholder="AI의 역할을 직접 설정하세요..."
        )
    else:
        system_prompt = preset_roles[selected_role]
        st.info(f"💡 {system_prompt}")

    st.markdown("---")

    # Temperature 조절
    st.subheader("🌡️ 창의성(Temperature)")
    temperature = st.slider(
        "값이 높을수록 창의적인 답변",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )

    # Max Tokens 조절
    max_tokens = st.slider(
        "📏 최대 출력 토큰 수",
        min_value=256,
        max_value=8192,
        value=4096,
        step=256
    )

    st.markdown("---")

    # 누적 사용량 표시
    st.subheader("📊 누적 토큰 사용량")
    st.metric("총 입력 토큰", f"{st.session_state.total_input_tokens:,}")
    st.metric("총 출력 토큰", f"{st.session_state.total_output_tokens:,}")
    st.metric(
        "총합",
        f"{st.session_state.total_input_tokens + st.session_state.total_output_tokens:,}"
    )

    st.markdown("---")

    # 대화 초기화 버튼
    if st.button("🗑️ 대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_input_tokens = 0
        st.session_state.total_output_tokens = 0
        st.session_state.last_user_input = ""
        st.success("대화가 초기화되었습니다!")
        st.rerun()

# ──────────────────────────────────────────
# 5. 메인 화면 - 두 컬럼 레이아웃
# ──────────────────────────────────────────
col_chat, col_favorite = st.columns([3, 1])

# ── 오른쪽: 즐겨찾기 패널 ──────────────────
with col_favorite:
    st.markdown("### 📌 즐겨찾기 질문")

    # 즐겨찾기 추가 입력
    new_fav = st.text_input("즐겨찾기에 추가할 질문", placeholder="자주 쓰는 질문 입력...")
    if st.button("➕ 추가", use_container_width=True):
        if new_fav.strip():
            if new_fav not in st.session_state.favorite_prompts:
                st.session_state.favorite_prompts.append(new_fav.strip())
                st.success("추가되었습니다!")
            else:
                st.warning("이미 추가된 질문입니다.")

    # 즐겨찾기 목록 표시
    if st.session_state.favorite_prompts:
        st.markdown("#### 저장된 질문")
        for i, fav in enumerate(st.session_state.favorite_prompts):
            col_a, col_b = st.columns([4, 1])
            with col_a:
                # 버튼 클릭 시 해당 질문을 입력창에 자동 설정
                if st.button(
                    f"📝 {fav[:20]}{'...' if len(fav) > 20 else ''}",
                    key=f"fav_{i}",
                    use_container_width=True
                ):
                    st.session_state.prefill_input = fav
                    st.rerun()
            with col_b:
                if st.button("🗑️", key=f"del_fav_{i}"):
                    st.session_state.favorite_prompts.pop(i)
                    st.rerun()
    else:
        st.info("아직 즐겨찾기가 없습니다.")

# ── 왼쪽: 채팅 메인 영역 ───────────────────
with col_chat:
    st.markdown("### 💬 대화")

    # 대화 히스토리 출력
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            role_label = "🧑 나" if msg["role"] == "user" else "🤖 Claude"
            with st.chat_message(msg["role"]):
                st.markdown(f"**{role_label}** `{msg.get('time', '')}`")
                st.write(msg["content"])

    st.markdown("---")

    # 즐겨찾기에서 불러온 질문 자동 채우기
    prefill = st.session_state.pop("prefill_input", "")

    # 사용자 입력
    user_input = st.text_area(
        "✏️ 질문 입력",
        value=prefill,
        height=130,
        placeholder="여기에 질문을 입력하세요...",
        key="user_input_area"
    )

    # 버튼 행
    btn_col1, btn_col2, btn_col3 = st.columns([2, 2, 1])

    with btn_col1:
        send_clicked = st.button("📨 답변 받기", type="primary", use_container_width=True)
    with btn_col2:
        regen_clicked = st.button("🔄 마지막 답변 재생성", use_container_width=True)
    with btn_col3:
        # 대화 내보내기 버튼
        if st.session_state.messages:
            export_text = "\n\n".join(
                [
                    f"[{msg.get('time','')}] {'나' if msg['role']=='user' else 'Claude'}:\n{msg['content']}"
                    for msg in st.session_state.messages
                ]
            )
            st.download_button(
                label="💾 저장",
                data=export_text,
                file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

    # ── API 호출 함수 ──────────────────────
    def call_claude(messages_history, user_msg):
        """Claude API를 호출하고 응답을 반환합니다."""
        # 히스토리 + 새 메시지 조합
        api_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in messages_history
        ]
        api_messages.append({"role": "user", "content": user_msg})

        kwargs = dict(
            model=selected_model_id,
            max_tokens=max_tokens,
            messages=api_messages,
            temperature=temperature,
        )
        if system_prompt:
            kwargs["system"] = system_prompt

        return client.messages.create(**kwargs)

    # ── 답변 받기 처리 ────────────────────
    if send_clicked:
        if not user_input.strip():
            st.warning("⚠️ 질문을 먼저 입력해주세요!")
        else:
            st.session_state.last_user_input = user_input.strip()
            with st.spinner("🤔 AI가 답변을 생성하고 있습니다..."):
                try:
                    response = call_claude(st.session_state.messages, user_input.strip())
                    answer = response.content[0].text
                    now = datetime.now().strftime("%H:%M:%S")

                    # 히스토리 저장
                    st.session_state.messages.append(
                        {"role": "user",      "content": user_input.strip(), "time": now}
                    )
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer,             "time": now}
                    )

                    # 토큰 누적
                    st.session_state.total_input_tokens  += response.usage.input_tokens
                    st.session_state.total_output_tokens += response.usage.output_tokens

                    # 이번 응답 사용량 표시
                    st.success("✅ 답변이 생성되었습니다!")
                    ic, oc, tc = st.columns(3)
                    ic.metric("입력 토큰", f"{response.usage.input_tokens:,}")
                    oc.metric("출력 토큰", f"{response.usage.output_tokens:,}")
                    tc.metric("합계",
                              f"{response.usage.input_tokens + response.usage.output_tokens:,}")
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ API 호출 오류: {e}")

    # ── 재생성 처리 ───────────────────────
    if regen_clicked:
        if not st.session_state.last_user_input:
            st.warning("⚠️ 재생성할 이전 질문이 없습니다.")
        else:
            # 마지막 assistant 답변 제거 후 재요청
            if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
                st.session_state.messages.pop()
            if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                st.session_state.messages.pop()

            with st.spinner("🔄 답변을 재생성하고 있습니다..."):
                try:
                    response = call_claude(
                        st.session_state.messages,
                        st.session_state.last_user_input
                    )
                    answer = response.content[0].text
                    now = datetime.now().strftime("%H:%M:%S")

                    st.session_state.messages.append(
                        {"role": "user",      "content": st.session_state.last_user_input, "time": now}
                    )
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer, "time": now}
                    )

                    st.session_state.total_input_tokens  += response.usage.input_tokens
                    st.session_state.total_output_tokens += response.usage.output_tokens

                    st.success("✅ 재생성 완료!")
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ 재생성 오류: {e}")
