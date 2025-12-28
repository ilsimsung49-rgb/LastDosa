import streamlit as st
import google.generativeai as genai
import random
from datetime import date

# 1. 페이지 설정 (가장 먼저 실행되어야 함)
st.set_page_config(page_title="할배 도사 만능 상담소", page_icon="👴", layout="wide")

# 2. API 설정 및 AI 모델 연결
try:
    # 스트림릿 Secrets에 설정된 API 키를 가져옵니다.
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"⚠️ 도사님 목소리 연결 실패: {e}")

# 3. 78장 타로 카드 정의
def get_tarot_deck():
    major = [f"{i}_Major" for i in range(22)]
    suits = ["Wands", "Cups", "Swords", "Pentacles"]
    ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]
    minor = [f"{rank}_of_{suit}" for suit in suits for rank in ranks]
    return major + minor

# 4. 메뉴 상태 관리
if 'menu' not in st.session_state:
    st.session_state.menu = "메인"

# --- [메인 화면 구성] ---
if st.session_state.menu == "메인":
    st.markdown("<h1 style='text-align: center;'>👴 할배 도사 만능 상담소</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>자네의 운명을 낱낱이 파헤쳐주마!</p>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("### 🔍 MBTI 족집게 판별")
        st.image("https://cdn.pixabay.com/photo/2017/05/13/17/48/zodiac-2310232_1280.jpg")
        if st.button("내 MBTI 맞혀보쇼", key="m1"): 
            st.session_state.menu = "MBTI판별"
            st.rerun()
    with col2:
        st.markdown("### 📅 오늘의 운세")
        st.image("https://cdn.pixabay.com/photo/2017/08/30/01/05/milky-way-2695569_1280.jpg")
        if st.button("오늘의 기운 보기", key="m2"): 
            st.session_state.menu = "오늘"
            st.rerun()
    with col3:
        st.markdown("### 🧧 올해의 사주")
        st.image("https://cdn.pixabay.com/photo/2018/01/25/14/12/nature-3106213_1280.jpg")
        if st.button("2026년 대운 확인", key="m3"): 
            st.session_state.menu = "올해"
            st.rerun()
    with col4:
        st.markdown("### 🃏 78장 타로")
        st.image("https://cdn.pixabay.com/photo/2021/11/14/10/33/tarot-6793540_1280.jpg")
        if st.button("깊은 고민 나누기", key="m4"): 
            st.session_state.menu = "타로"
            st.rerun()

# --- [개별 상담방 구성] ---
else:
    if st.button("⬅️ 메인으로 돌아가기"):
        st.session_state.menu = "메인"
        st.rerun()
    st.write("---")

    # 1. MBTI 판별방
    if st.session_state.menu == "MBTI판별":
        st.subheader("📍 할배 도사의 MBTI 독심술")
        user_input = st.text_area("자네 성격이나 고민을 아무렇게나 적어보드라고. 도사가 맞춰줄 테니!")
        if st.button("도사님, 제 MBTI는 뭔가요?"):
            if user_input:
                with st.spinner("도사님이 돋보기를 꺼내셨네..."):
                    prompt = f"너는 용한 할배 도사야. 글: '{user_input}'. MBTI를 판별하고 아주 구수한 노인 말투로 설명해줘."
                    response = model.generate_content(prompt)
                    st.write(response.text)

    # 2. 오늘의 운세방
    elif st.session_state.menu == "오늘":
        st.subheader("📍 오늘의 운세 (사주 & 타로)")
        name = st.text_input("이름")
        birth = st.date_input("생년월일", value=date(1995, 1, 1))
        if st.button("오늘의 점괘 보기"):
            if name:
                with st.spinner("엽전 던지는 중..."):
                    card = random.choice(get_tarot_deck())
                    prompt = f"이름:{name}, 생일:{birth}. 너는 할배 도사야. 오늘의 타로카드 {card}를 바탕으로 운세를 노인 말투로 풀이해줘."
                    response = model.generate_content(prompt)
                    st.write(response.text)

    # 3. 올해의 사주방
    elif st.session_state.menu == "올해":
        st.subheader("📍 2026년 대운 풀이")
        name = st.text_input("이름 ")
        birth = st.date_input("생일 ", value=date(1990, 1, 1))
        if st.button("올해 총운 확인하기"):
            if name:
                with st.spinner("사주 단자 보는 중..."):
                    prompt = f"이름:{name}, 생일:{birth}. 너는 할배 도사야. 2026년 신년 운세를 노인 말투로 아주 길고 정성껏 봐줘."
                    response = model.generate_content(prompt)
                    st.write(response.text)

    # 4. 78장 타로방
    elif st.session_state.menu == "타로":
        st.subheader("📍 78장 타로 심층 상담")
        question = st.text_input("무엇이 궁금한가?")
        if st.button("운명의 카드 3장 뽑기"):
            if question:
                with st.spinner("카드 섞는 중..."):
                    cards = random.sample(get_tarot_deck(), 3)
                    prompt = f"질문:{question}, 뽑은카드:{cards}. 너는 할배 도사야. 타로 결과를 노인 말투로 깊이 있게 상담해줘."
                    response = model.generate_content(prompt)
                    st.write(response.text)
