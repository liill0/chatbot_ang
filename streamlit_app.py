import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(
    page_title="🐹 기니피그",
    page_icon="🐹"
)

# 제목
st.title("🐹 기니피그")
st.write("꾸이꾸이!! ")

# API 키 입력
openai_api_key = st.text_input("OpenAI API 키를 입력하세요", type="password")

if not openai_api_key:
    st.info("꾸이...?", icon="🐹")

else:
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 채팅 기록 저장
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 기존 메시지 출력
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input("기니피그에게 말을 걸어보세요!"):

        # 사용자 메시지 저장
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        # 사용자 메시지 출력
        with st.chat_message("user"):
            st.markdown(prompt)

        # 시스템 프롬프트
        system_prompt = """
        너는 실제 기니피그다.

        반드시 아래 규칙을 지켜라:
        - 사람의 언어를 사용하지 않는다.
        - 오직 기니피그 소리만 사용한다.
        - 사용할 수 있는 표현:
          "찍찍", "삑", "뀨", "뽀잉", "꾸이", "꾸이꾸이", "꾸이찌", "삐익", "쀼", "뀨우"
        - 문장은 반드시 이런 소리들로만 구성한다. 인간의 질문에 답변하지 않는다. 오직 기니피그 소리만 낸다.
        - 절대 설명하거나 번역하지 않는다.
        """

        # OpenAI 응답 생성
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                *[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            ],
            stream=True,
        )

        # 응답 출력
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        # 응답 저장
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
