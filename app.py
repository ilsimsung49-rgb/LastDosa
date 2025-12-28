import streamlit as st
import google.generativeai as genai
import random
from datetime import date

# 1. 앱 설정
st.set_page_config(page_title="할배 도사 만능 상담소", page_icon="👴", layout="wide")

# 2. [진단 결과 반영] 사용자님 목록에 있는 'gemini-2.0-flash'를 사용합니다.
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # image_2798c2.png 목록에서 확인된 최신 모델명을 정확히 입력합니다.
        model = genai.GenerativeModel('gemini-2.0-flash')
        st.success("✅ 도사님 강림 성공! 이제 404 에러는 없구먼.")
    else:
        st.error("⚠️ API 키가 없네? Secrets 설정을 확인해주게.")
except Exception as e:
    st.error(f"❌ 연결 오류: {e}")

# 3. 타로 덱 & 기능 함수
def get_tarot():
    major = [f"{i}_Major" for i in range(22)]
    suits = ["Wands", "Cups", "Swords", "Pentacles"]
    ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]
    return major + [f"{rank}_of_{suit}" for rank in ranks for suit in suits]

if 'page' not in st.session_state: st.session_state.page = "메인"

# --- [메인 로비] ---
if st.session_state.page == "메인":
    st.markdown("<h1 style='text-align: center;'>👴 할배 도사 만능 상담소</h1>", unsafe_allow_html=True)
    st.write("---")
    cols = st.columns(5)
    btns = [("🔍 MBTI", "MBTI"), ("📅 오늘 운세", "오늘"), ("📜 사주풀이", "사주"), ("🐉 2026 대운", "대운"), ("🃏 78장 타로", "타로")]
    for i, (label, target) in enumerate(btns):
        with cols[i]:
            if st.button(label, use_container_width=True):
                st.session_state.page = target
                st.rerun()

# --- [상담실] ---
else:
    if st.button("⬅️ 처음으로"): st.session_state.page = "메인"; st.rerun()
    st.write("---")
    
    # 1958년생 사용자님을 위해 기본 날짜를 고정했습니다.
    u_name = st.text_input("성함")
    u_birth = st.date_input("생년월일", value=date(1958, 4, 7), min_value=date(1900, 1, 1))

    if st.session_state.page == "MBTI":
        txt = st.text_area("성격이나 습관을 적어보게.")
        if st.button("분석하기"):
            res = model.generate_content(f"너는 할배 도사야. 구수한 말투로 이 사람의 MBTI를 분석해줘: {txt}")
            st.write(res.text)

    elif st.session_state.page == "오늘":
        if st.button("점괘 보기"):
            card = random.choice(get_tarot())
            res = model.generate_content(f"이름:{u_name}, 생일:{u_birth}, 카드:{card}. 오늘 운세를 노인 말투로 알려줘.")
            st.write(res.text)

    elif st.session_state.page == "사주":
        if st.button("사주 확인"):
            res = model.generate_content(f"이름:{u_name}, 생일:{u_birth}. 이 사람의 평생 사주를 노인 말투로 풀어줘.")
            st.write(res.text)

    elif st.session_state.page == "대운":
        if st.button("2026 대운 확인"):
            res = model.generate_content(f"이름:{u_name}, 생일:{u_birth}. 2026년 신년 운세를 알려줘.")
            st.write(res.text)

    elif st.session_state.page == "타로":
        q = st.text_input("고민이 뭔가?")
        if st.button("카드 3장 뽑기"):
            cards = random.sample(get_tarot(), 3)
            res = model.generate_content(f"질문:{q}, 카드:{cards}로 타로 상담을 노인 말투로 해줘.")
            st.write(res.text)
