import streamlit as st
import google.generativeai as genai
import random
from datetime import date

# 1. API 설정 (Tier 1 무적 기운 유지)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API 키 설정 확인이 필요하구먼!")

# 2. 페이지 설정
st.set_page_config(page_title="할배 도사 만능 상담소", page_icon="👴", layout="wide")

if 'menu' not in st.session_state:
    st.session_state.menu = "메인"

# --- 메인 화면: 4개 블록으로 확장 ---
if st.session_state.menu == "메인":
    st.markdown("<h1 style='text-align: center;'>👴 할배 도사 족집게 상담소</h1>", unsafe_allow_html=True)
    st.write("---")
    col1, col2, col3, col4 = st.columns(4) # 블록을 4개로 늘렸습니다!
    
    with col1:
        st.markdown("### 🔍 MBTI 족집게 판별")
        st.image("https://cdn.pixabay.com/photo/2017/05/13/17/48/zodiac-2310232_1280.jpg", use_container_width=True)
        if st.button("내 MBTI 맞혀보쇼", use_container_width=True):
            st.session_state.menu = "MBTI판별"
            st.rerun()
    # ... (중략: 오늘의 운세, 올해의 운세, 타로 상담 블록은 그대로 유지) ...
    with col2:
        st.markdown("### 📅 오늘의 운세")
        if st.button("오늘의 기운 보기", use_container_width=True): st.session_state.menu = "오늘"; st.rerun()
    with col3:
        st.markdown("### 🧧 올해의 사주")
        if st.button("2026년 대운 확인", use_container_width=True): st.session_state.menu = "올해"; st.rerun()
    with col4:
        st.markdown("### 🃏 78장 타로")
        if st.button("깊은 고민 나누기", use_container_width=True): st.session_state.menu = "타로"; st.rerun()

# --- MBTI 판별 전용 화면 ---
if st.session_state.menu == "MBTI판별":
    st.subheader("📍 할배 도사의 MBTI 독심술")
    st.button("⬅️ 메인으로", on_click=lambda: st.session_state.update(menu="메인"))
    
    user_input = st.text_area("자네 성격이나 평소 습관을 아무렇게나 적어보드라고. 내가 딱 맞혀줄 테니!", 
                              placeholder="예: 나는 계획 세우는 건 귀찮은데 막상 하면 완벽하게 하려고 해. 사람 만나는 건 좋지만 금방 지쳐.")
    
    if st.button("도사님, 제 MBTI는 뭔가요?"):
        if user_input:
            with st.spinner("도사님이 자네 속을 훤히 들여다보고 있네..."):
                prompt = f"사용자의 글: '{user_input}'. 너는 아주 용한 할배 도사야. 이 글을 분석해서 사용자의 MBTI를 딱 하나로 판별해주고, 왜 그렇게 생각하는지 노인 말투로 아주 신통방통하게 설명해줘."
                response = model.generate_content(prompt)
                st.write(response.text)
