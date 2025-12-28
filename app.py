import streamlit as st
import google.generativeai as genai
import random
from datetime import date

# 1. 페이지 설정 (최상단 고정)
st.set_page_config(page_title="할배 도사 만능 상담소", page_icon="👴", layout="wide")

# 2. AI 모델 설정 (에러 로그 분석 결과: 경로를 제거한 가장 단순한 이름 사용)
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # 'models/' 경로를 넣으면 404 에러가 납니다.
        # 유료 티어에서 가장 안정적인 gemini-pro 명칭만 사용합니다.
        model = genai.GenerativeModel('gemini-pro')
    else:
        st.error("⚠️ API 키가 설정되지 않았구먼! Secrets 설정을 확인해주게.")
except Exception as e:
    st.error(f"⚠️ 시스템 연결 오류: {e}")

# 3. 78장 타로 덱 정의
def get_tarot_deck():
    major = [f"{i}_Major" for i in range(22)]
    suits = ["Wands", "Cups", "Swords", "Pentacles"]
    ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]
    return major + [f"{rank}_of_{suit}" for rank in ranks for suit in suits]

# 4. 메뉴 상태 관리 (충돌 방지용 고유 키)
if 'menu' not in st.session_state:
    st.session_state.menu = "메인"

# --- [메인 화면: 5대 메뉴] ---
if st.session_state.menu == "메인":
    st.markdown("<h1 style='text-align: center;'>👴 할배 도사 만능 상담소</h1>", unsafe_allow_html=True)
    st.write("---")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("🔍 MBTI 판별", key="m1"): st.session_state.menu = "MBTI"; st.rerun()
    with col2:
        if st.button("📅 오늘 운세", key="m2"): st.session_state.menu = "오늘"; st.rerun()
    with col3:
        if st.button("📜 전체 사주", key="m3"): st.session_state.menu = "사주"; st.rerun()
    with col4:
        if st.button("🐉 2026 대운", key="m4"): st.session_state.menu = "올해"; st.rerun()
    with col5:
        if st.button("🃏 78장 타로", key="m5"): st.session_state.menu = "타로"; st.rerun()

# --- [상담방 내부] ---
else:
    if st.button("⬅️ 메인으로 돌아가기"): st.session_state.menu = "메인"; st.rerun()
    st.write("---")

    if st.session_state.menu == "MBTI":
        st.subheader("📍 MBTI 독심술")
        u_in = st.text_area("성격이나 습관을 적어보게.", height=150, key="m_txt")
        if st.button("도사님 맞춰보쇼"):
            if u_in:
                with st.spinner("살펴보는 중..."):
                    res = model.generate_content(f"너는 할배 도사야. 이 글을 분석해서 MBTI를 맞히고 노인 말투로 설명해줘: {u_in}")
                    st.write(res.text)

    elif st.session_state.menu == "오늘":
        st.subheader("📍 오늘의 운세")
        n_in = st.text_input("이름", key="n_t")
        # 1900년대생 어르신들도 선택 가능한 달력 범위 확장
        b_in = st.date_input("생년월일", value=date(1985, 1, 1), min_value=date(1900, 1, 1), key="b_t")
        if st.button("오늘 점괘 보기"):
            if n_in:
                with st.spinner("기운 읽는 중..."):
                    card = random.choice(get_tarot_deck())
                    res = model.generate_content(f"이름:{n_in}, 생일:{b_in}. 타로 {card}로 오늘 하루 운세를 노인 말투로 알려줘.")
                    st.write(res.text)

    elif st.session_state.menu == "사주":
        st.subheader("📍 평생 사주풀이")
        n_in = st.text_input("성함", key="n_s")
        b_in = st.date_input("생일 ", value=date(1985, 1, 1), min_value=date(1900, 1, 1), key="b_s")
        if st.button("평생 운명 확인"):
            if n_in:
                with st.spinner("단자를 보는 중..."):
                    res = model.generate_content(f"이름:{n_in}, 생일:{b_in}. 평생 사주와 운명을 노인 말투로 자세히 풀어줘.")
                    st.write(res.text)

    elif st.session_state.menu == "올해":
        st.subheader("📍 2026년 대운")
        n_in = st.text_input("성함 ", key="n_y")
        b_in = st.date_input("생일 ", value=date(1985, 1, 1), min_value=date(1900, 1, 1), key="b_y")
        if st.button("내년 총운 확인"):
            if n_in:
                with st.spinner("대운 읽는 중..."):
                    res = model.generate_content(f"이름:{n_in}, 생일:{b_in}. 2026년 운세를 노인 말투로 알려줘.")
                    st.write(res.text)

    elif st.session_state.menu == "타로":
        st.subheader("📍 78장 타로")
        q_in = st.text_input("고민?", key="q_ta")
        if st.button("카드 뽑기"):
            if q_in:
                with st.spinner("카드 섞는 중..."):
                    cards = random.sample(get_tarot_deck(), 3)
                    res = model.generate_content(f"질문:{q_in}, 카드:{cards}. 노인 말투로 타로 상담해줘.")
                    st.write(res.text)
