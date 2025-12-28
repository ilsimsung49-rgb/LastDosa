import streamlit as st
import random
from datetime import date

# 1. 페이지 설정
st.set_page_config(page_title="할배 도사 전문 상담소", page_icon="👴", layout="wide")

# 2. 78장 타로 카드 덱 정의
def get_tarot_deck():
    major = [f"{i}_Major" for i in range(22)]
    suits = ["Wands", "Cups", "Swords", "Pentacles"]
    ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]
    minor = [f"{rank}_of_{suit}" for suit in suits for rank in ranks]
    return major + minor

# 3. 세션 상태 초기화 (메뉴 선택 저장)
if 'menu' not in st.session_state:
    st.session_state.menu = "메인"

# --- 메인 화면: 블록형 메뉴 ---
if st.session_state.menu == "메인":
    st.markdown("<h1 style='text-align: center;'>👴 할배 도사 전문 상담소</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>원하시는 보약(점괘)을 하나 골라보드라고!</p>", unsafe_allow_html=True)
    st.write("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📅 오늘의 운세")
        st.image("https://cdn.pixabay.com/photo/2017/08/30/01/05/milky-way-2695569_1280.jpg", use_container_width=True)
        if st.button("오늘의 기운 보기", use_container_width=True):
            st.session_state.menu = "오늘"
            st.rerun()

    with col2:
        st.markdown("### 🧧 올해의 운세")
        st.image("https://cdn.pixabay.com/photo/2018/01/25/14/12/nature-3106213_1280.jpg", use_container_width=True)
        if st.button("2026년 대운 확인", use_container_width=True):
            st.session_state.menu = "올해"
            st.rerun()

    with col3:
        st.markdown("### 🃏 78장 타로 상담")
        st.image("https://cdn.pixabay.com/photo/2021/11/14/10/33/tarot-6793540_1280.jpg", use_container_width=True)
        if st.button("깊은 고민 나누기", use_container_width=True):
            st.session_state.menu = "타로"
            st.rerun()

# --- 개별 메뉴 화면 ---
if st.session_state.menu != "메인":
    if st.button("⬅️ 메인으로 돌아가기"):
        st.session_state.menu = "메인"
        st.rerun()
    st.write("---")

    if st.session_state.menu == "오늘":
        st.subheader("📍 오늘의 운세")
        # [여기에 기존 오늘의 운세 기능 코드 삽입]
        
    elif st.session_state.menu == "올해":
        st.subheader("📍 2026년 올해의 운세")
        # [여기에 기존 올해의 운세 기능 코드 삽입]
        
    elif st.session_state.menu == "타로":
        st.subheader("📍 78장 타로 상담")
        # [여기에 기존 78장 타로 기능 코드 삽입]
