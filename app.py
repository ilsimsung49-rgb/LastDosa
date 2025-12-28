import streamlit as st
import google.generativeai as genai
import random
from datetime import date

# 1. 페이지 설정 (최상단 고정)
st.set_page_config(page_title="할배 도사 만능 상담소", page_icon="👴", layout="wide")

# 2. AI 모델 설정 (안정화 필터 적용)
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("⚠️ API 키가 없구먼! Secrets 설정을 확인해주드라고.")
except Exception as e:
    st.error(f"⚠️ 도사님 목소리 연결 오류: {e}")

# 3. 78장 타로 덱 정의
def get_tarot_deck():
    major = [f"{i}_Major" for i in range(22)]
    suits = ["Wands", "Cups", "Swords", "Pentacles"]
    ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]
    return major + [f"{rank}_of_{suit}" for suit in suits for rank in ranks]

# 4. 메뉴 상태 관리
if 'menu' not in st.session_state:
    st.session_state.menu = "메인"

# --- [메인 화면: 5대 명당] ---
if st.session_state.menu == "메인":
    st.markdown("<h1 style='text-align: center;'>👴 할배 도사 만능 상담소</h1>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    col4, col5, _ = st.columns(3)

    with col1:
        st.markdown("### 🔍 MBTI 족집게 판별")
        st.image("https://cdn.pixabay.com/photo/2017/05/13/17/48/zodiac-2310232_1280.jpg")
        if st.button("내 MBTI 맞혀보쇼", key="m1"): st.session_state.menu = "MBTI판별"; st.rerun()
    with col2:
        st.markdown("### 📅 오늘의 운세")
        st.image("https://cdn.pixabay.com/photo/2017/08/30/01/05/milky-way-2695569_1280.jpg")
        if st.button("오늘의 기운 보기", key="m2"): st.session_state.menu = "오늘"; st.rerun()
    with col3:
        st.markdown("### 📜 전체 사주풀이")
        st.image("https://cdn.pixabay.com/photo/2015/10/31/12/00/astronomy-1015509_1280.jpg")
        if st.button("평생 팔자 확인", key="m3"): st.session_state.menu = "전체사주"; st.rerun()
    with col4:
        st.markdown("### 🐉 2026년 대운")
        st.image("https://cdn.pixabay.com/photo/2018/01/25/14/12/nature-3106213_1280.jpg")
        if st.button("내년 운세 보기", key="m4"): st.session_state.menu = "올해"; st.rerun()
    with col5:
        st.markdown("### 🃏 78장 타로")
        st.image("https://cdn.pixabay.com/photo/2021/11/14/10/33/tarot-6793540_1280.jpg")
        if st.button("고민 상담하기", key="m5"): st.session_state.menu = "타로"; st.rerun()

# --- [상담방 내부] ---
else:
    if st.button("⬅️ 메인으로 돌아가기", key="back_btn"): st.session_state.menu = "메인"; st.rerun()
    st.write("---")

    if st.session_state.menu == "MBTI판별":
        st.subheader("📍 할배 도사의 MBTI 독심술")
        st.info("👴: '자네 성격이나 고민을 편하게 적어보게. 내가 자네 말투만 들어도 MBTI를 딱 맞혀줄 테니!'")
        user_input = st.text_area("도사님께 건넬 말", height=150, key="in_mbti")
        if st.button("도사님, 제 MBTI는 뭔가요?", key="go_mbti"):
            if user_input:
                with st.spinner("자네 속을 훤히 들여다보는 중..."):
                    prompt = f"너는 용한 할배 도사야. 이 글을 분석해서 MBTI를 판별해주고 이유를 아주 구수한 노인 말투로 설명해줘: '{user_input}'"
                    st.write(model.generate_content(prompt).text)
            else: st.warning("말 한마디라도 건네야 점을 치지!")

    elif st.session_state.menu == "오늘":
        st.subheader("📍 오늘의 운세")
        name = st.text_input("성함", key="in_name_today")
        birth = st.date_input("생년월일", value=date(1985, 1, 1), min_value=date(1900, 1, 1), max_value=date.today(), key="in_birth_today")
        if st.button("오늘 점괘 보기", key="go_today"):
            if name:
                with st.spinner("기운을 살피는 중..."):
                    card = random.choice(get_tarot_deck())
                    prompt = f"이름:{name}, 생일:{birth}. 타로 {card}로 오늘 운세를 노인 말투로 알려줘."
                    st.write(model.generate_content(prompt).text)

    elif st.session_state.menu == "전체사주":
        st.subheader("📍 타고난 평생 사주팔자 풀이")
        name = st.text_input("성함", key="in_name_saju")
        birth = st.date_input("생년월일 ", value=date(1985, 1, 1), min_value=date(1900, 1, 1), max_value=date.today(), key="in_birth_saju")
        time = st.text_input("태어난 시간 (모르면 모름)", key="in_time_saju")
        if st.button("평생 운명 확인하기", key="go_saju"):
            if name:
                with st.spinner("사주 단자 펼치는 중..."):
                    prompt = f"이름:{name}, 생일:{birth}, 태어난시간:{time}. 이 사람의 타고난 사주팔자, 성격, 평생의 운을 역학적으로 자세히 노인 말투로 풀어줘."
                    st.write(model.generate_content(prompt).text)

    elif st.session_state.menu == "올해":
        st.subheader("📍 2026년 병오년 신년 운세")
        name = st.text_input("성함 ", key="in_name_year")
        birth = st.date_input("생년월일  ", value=date(1985, 1, 1), min_value=date(1900, 1, 1), max_value=date.today(), key="in_birth_year")
        if st.button("2026년 총운 보기", key="go_year"):
            if name:
                with st.spinner("신년 대운을 보는 중..."):
                    prompt = f"이름:{name}, 생일:{birth}. 2026년의 재물, 건강, 애정운을 사주 기반으로 노인 말투로 정성껏 알려줘."
                    st.write(model.generate_content(prompt).text)

    elif st.session_state.menu == "타로":
        st.subheader("📍 78장 타로 상담")
        question = st.text_input("고민이 뭔가?", key="in_q_tarot")
        if st.button("카드 3장 뽑기", key="go_tarot"):
            if question:
                with st.spinner("카드를 섞는 중..."):
                    cards = random.sample(get_tarot_deck(), 3)
                    prompt = f"질문:{question}, 카드:{cards}. 노인 말투로 타로 상담해줘."
                    st.write(model.generate_content(prompt).text)
