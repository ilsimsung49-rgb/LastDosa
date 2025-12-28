import streamlit as st
import google.generativeai as genai
import random
from datetime import date

# 1. 앱 설정
st.set_page_config(page_title="할배 도사 만능 상담소", page_icon="👴", layout="wide")

# 2. [진단 결과 반영] 확인된 모델명을 정확히 사용합니다.
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # image_2798c2.png 목록에서 확인된 gemini-2.0-flash를 사용합니다.
        model = genai.GenerativeModel('gemini-2.0-flash')
        st.success("✅ 도사님 강림 성공! 이제 점을 볼 수 있구먼.")
    else:
        st.error("⚠️ API 키가 없네? Secrets 설정을 확인해주게.")
except Exception as e:
    st.error(f"❌ 시스템 연결 오류: {e}")

# 3. 기능 함수
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
    
    u_name = st.text_input("성함")
    # 생년월일 기본값을 중립적인 1995년으로 변경했습니다. 
    u_birth = st.date_input("생년월일", value=date(1995, 1, 1), min_value=date(1900, 1, 1))

    if st.session_state.page == "MBTI":
        txt = st.text_area("성격이나 습관을 적어보게.")
        if st.button("분석하기"):
            with st.spinner("살펴보는 중..."):
                res = model.generate_content(f"너는 할배 도사야. 구수한 전라도 말투로 이 사람의 MBTI를 분석해줘: {txt}")
                st.write(res.text)

    elif st.session_state.page == "오늘":
        if st.button("점괘 보기"):
            with st.spinner("엽전 던지는 중..."):
                card = random.choice(get_tarot())
                res = model.generate_content(f"이름:{u_name}, 생일:{u_birth}, 카드:{card}. 오늘 하루 운세를 노인 말투로 알려줘.")
                st.write(res.text)

    elif st.session_state.page == "사주":
        if st.button("사주 확인"):
            with st.spinner("단자 펼치는 중..."):
                res = model.generate_content(f"이름:{u_name}, 생일:{u_birth}. 이 사람의 평생 사주를 노인 말투로 정성껏 풀어줘.")
                st.write(res.text)

    elif st.session_state.page == "대운":
        if st.button("2026 대운 확인"):
            with st.spinner("대운 읽는 중..."):
                res = model.generate_content(f"이름:{u_name}, 생일:{u_birth}. 2026년 신년 대운을 노인 말투로 알려줘.")
                st.write(res.text)

    elif st.session_state.page == "타로":
        q = st.text_input("고민이 뭔가?")
        if st.button("카드 뽑기"):
            with st.spinner("카드 섞는 중..."):
                cards = random.sample(get_tarot(), 3)
                res = model.generate_content(f"질문:{q}, 카드:{cards}로 타로 상담을 노인 말투로 해줘.")
                st.write(res.text)
