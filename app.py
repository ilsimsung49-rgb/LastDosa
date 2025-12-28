import streamlit as st
import google.generativeai as genai
import random
from datetime import date

# 1. API 키 및 모델 설정
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API 키 설정이 필요합니다. Secrets를 확인해주세요.")

# 2. 기본 설정
st.set_page_config(page_title="할배 도사 만능 상담소", page_icon="👴", layout="wide")

def get_tarot_deck():
    major = [f"{i}_Major" for i in range(22)]
    suits = ["Wands", "Cups", "Swords", "Pentacles"]
    ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]
    minor = [f"{rank}_of_{suit}" for suit in suits for rank in ranks]
    return major + minor

if 'menu' not in st.session_state:
    st.session_state.menu = "메인"

# --- 메인 화면 ---
if st.session_state.menu == "메인":
    st.markdown("<h1 style='text-align: center;'>👴 할배 도사 만능 상담소</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>MBTI부터 사주까지, 내 모르는 게 없느니라!</p>", unsafe_allow_html=True)
    st.write("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📅 오늘의 운세")
        st.image("https://cdn.pixabay.com/photo/2017/08/30/01/05/milky-way-2695569_1280.jpg", use_container_width=True)
        if st.button("오늘의 기운 보기", key="today_btn", use_container_width=True):
            st.session_state.menu = "오늘"
            st.rerun()
    with col2:
        st.markdown("### 🧧 올해의 사주/운세")
        st.image("https://cdn.pixabay.com/photo/2018/01/25/14/12/nature-3106213_1280.jpg", use_container_width=True)
        if st.button("2026년 대운 확인", key="year_btn", use_container_width=True):
            st.session_state.menu = "올해"
            st.rerun()
    with col3:
        st.markdown("### 🃏 78장 타로 상담")
        st.image("https://cdn.pixabay.com/photo/2021/11/14/10/33/tarot-6793540_1280.jpg", use_container_width=True)
        if st.button("깊은 고민 나누기", key="tarot_btn", use_container_width=True):
            st.session_state.menu = "타로"
            st.rerun()

# --- 개별 메뉴 화면 ---
else:
    if st.button("⬅️ 메인으로 돌아가기"):
        st.session_state.menu = "메인"
        st.rerun()
    st.write("---")

    if st.session_state.menu == "오늘":
        st.subheader("📍 오늘의 운세 (맞춤형 데이터 기반)")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("이름")
            birth = st.date_input("생년월일", value=date(1995, 1, 1))
        with col2:
            mbti = st.selectbox("MBTI가 뭔가?", ["모름", "ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP", "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"])
            blood = st.selectbox("혈액형은?", ["모름", "A형", "B형", "O형", "AB형"])
        
        if st.button("도사님, 오늘 제 운은요?") and name:
            with st.spinner("도사님이 데이터를 훑어보고 계시네..."):
                prompt = f"너는 할배 도사야. 이름:{name}, 생일:{birth}, MBTI:{mbti}, 혈액형:{blood}. 이 정보를 바탕으로 오늘의 운세를 사주와 타로 기운을 섞어 노인 말투로 재밌게 풀어줘."
                response = model.generate_content(prompt)
                st.write(response.text)

    elif st.session_state.menu == "올해":
        st.subheader("📍 2026년 대운 및 성격 분석")
        name = st.text_input("이름")
        birth = st.date_input("생년월일", value=date(1990, 1, 1))
        col_a, col_b = st.columns(2)
        with col_a:
            mbti = st.selectbox("MBTI 선택", ["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP", "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"])
        with col_b:
            blood = st.selectbox("혈액형 선택", ["A형", "B형", "O형", "AB형"])
        
        if st.button("올해의 종합 운세 보기"):
            with st.spinner("도사님이 돋보기를 쓰셨네..."):
                prompt = f"이름:{name}, 생일:{birth}, MBTI:{mbti}, 혈액형:{blood}. 너는 인생 경험 많은 할배 도사야. 이 사람의 성격적 특징(MBTI/혈액형)과 사주를 결합해서 2026년 재물, 건강, 연애운을 아주 구수하게 점쳐줘."
                response = model.generate_content(prompt)
                st.write(response.text)

    elif st.session_state.menu == "타로":
        st.subheader("📍 78장 타로 깊은 상담")
        question = st.text_input("고민이 무엇인가? (MBTI나 혈액형을 같이 적어주면 더 정확하드라고!)")
        if st.button("운명의 카드 뽑기") and question:
            cards = random.sample(get_tarot_deck(), 3)
            with st.spinner("카드가 춤을 추고 있구먼..."):
                prompt = f"질문: {question}. 뽑은 카드: {cards}. 너는 신통방통한 할배 도사야. 질문자의 고민을 타로 카드로 분석하고 노인 말투로 정성껏 상담해줘."
                response = model.generate_content(prompt)
                st.write(response.text)
