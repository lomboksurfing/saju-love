import streamlit as st
import openai
import datetime


from dotenv import load_dotenv
import os

load_dotenv( )
openai.api_key = os.getenv("OPENAI_API_KEY")


# 🔐 OpenAI API 키 설정 (직접 넣거나 환경변수 사용)
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="사주 연애운 상담소", page_icon="🔮", layout="centered")
st.title("🔮 사주 연애운 상담소")
st.markdown("출생 정보를 입력하고, 지금 하고 있는 연애 고민을 허심탄회하게 적어주세요. <br>AI 사주 전문가가 정확하게 상담해드립니다.", unsafe_allow_html=True)

# 👉 사용자 입력 변수 초기화
birth_info = ""
love_question = ""

# ✍️ 사용자 입력

with st.form("saju_form"):
    st.markdown("### 📆 출생 정보 입력")

    calendar_type = st.radio("달력 종류 선택", ["양력", "음력"], horizontal=True)

    birth_date = st.date_input(
        "생년월일을 선택하세요",
        min_value=datetime.date(1900, 1, 1),
        max_value=datetime.date(2099, 12, 31)
    )

    meridiem = st.radio("시간대", ["오전", "오후"], horizontal=True)  # ✅ 들여쓰기 맞춤

    time_input = st.text_input("시간 입력 (예: 09:30)", placeholder="예: 08:15 또는 12:00")
    love_question = st.text_input("💌 연애 고민을 적어주세요!")

    submitted = st.form_submit_button("✨ 두둥! 결과 보기")

    if submitted:
        if not time_input or ":" not in time_input:
            st.warning("시간을 '09:30' 형식으로 입력해주세요.")
        elif not love_question:
            st.warning("연애 질문을 입력해주세요.")
        else:
            birth_info = f"{calendar_type} {birth_date.strftime('%Y년 %-m월 %-d일')} {meridiem} {time_input}"
            st.markdown("---")
            st.info(f"🧾 입력된 출생 정보: `{birth_info}`")

# 💬 GPT 응답 출력
if submitted and birth_info and love_question:
    with st.spinner("사주를 풀이하는 중입니다... 🧘‍♀️"):
        prompt = f"""
당신은 연애운에 특화된 사주 명리학 전문가입니다.
출생 정보와 질문을 참고하여 따뜻하고 현실적인 연애 상담을 해주세요.

출생 정보: {birth_info}
연애 질문: {love_question}
"""
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=800,
            )
            result = response.choices[0].message.content.strip()
            st.success("📜 상담 결과")
            st.write(result)
        except Exception as e:
            st.error(f"❌ 에러가 발생했습니다: {e}")
