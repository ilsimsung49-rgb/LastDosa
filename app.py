import streamlit as st
import requests
import random
from datetime import date

# 1. 앱 기본 설정 (처음부터 완전히 다시 설계)
st.set_page_config(page_title="할배 도사 만능 상담소", page_icon="👴", layout="wide")

# 2. [완전 새 방식] AI 직접 호출 엔진 (404 에러 물리적 차단)
def ask_ai_direct(prompt_text):
    api_key = st.secrets["GOOGLE_API_KEY"]
    # 구글 공식 라이브러리가 아닌 다이렉트 API 주소를 사용하여 경로 에러를 회피합니다.
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{
                "text": f"너는 구수한 사투리를 쓰는 용한 할배 도사야. 친절하고 재치 있게 상담해주렴. 질문: {prompt_text}"
            }]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status() 
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"👴: '에구구, 기운이 잠시 꼬였나 보구먼. 다시 한번 눌러보게! (오류 알림: {e})'"

# 3. 78장 타로 덱 새로 구축
def create_tarot_deck():
    major = [f"{i}_Major" for i in range(22)]
    suits = ["Wands", "Cups", "Swords", "Pentacles"]
    ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]
    return major + [f"{rank}_of_{suit}" for rank in ranks for suit in suits]

# 4. 세션 기반 메뉴 시스템
if 'page' not in st.session_state:
    st.session_state.page = "HOME"

# --- [페이지 1: 메인 로비] ---
if st.session_state.page == "HOME":
    st.markdown("<h1 style='text-align: center;'>👴 할배 도사 만능 상담소</h1>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("🔍 MBTI 판별", use_container_width=True): st.session_state.page = "MBTI"; st.rerun()
    with col2:
        if st.button("📅 오늘 운세", use_container_width=True): st.session_state.page = "TODAY"; st.rerun()
    with col3:
        if st.button("📜 전체 사주", use_container_width=True): st.session_state.page = "SAJU"; st.rerun()
    with col4:
        if st.button("🐉 2026 대운", use_container_width=True): st.session_state.page = "2026"; st.rerun()
    with col5:
        if st.button("🃏 78장 타로", use_container_width=True): st.session_state.page = "TAROT"; st.rerun()

# --- [페이지 2: 개별 상담실] ---
else:
    if st.button("⬅️ 처음으로 돌아가기"): st.session_state.page = "HOME"; st.rerun()
    st.write("---")

    if st.session_state.page == "MBTI":
        st.subheader("📍 할배 도사의 MBTI 독심술")
        text = st.text_area("성격이나 습관을 아무렇게나 적어보게.", height=150)
        if st.button("도사님 분석해주쇼"):
            if text:
                with st.spinner("살펴보는 중..."):
                    st.write(ask_ai_direct(f"MBTI를 맞히고 이유를 노인 말투로 설명해줘: {text}"))

    elif st.session_state.page == "TODAY":
        st.subheader("📍 오늘의 운세 실")
        name = st.text_input("이름")
        # 1900년부터 선택 가능한 달력 범위 확장
        birth = st.date_input("생년월일", value=date(1985, 1, 1), min_value=date(1900, 1, 1))
        if st.button("오늘 점괘 보기"):
            if name:
                with st.spinner("엽전 던지는 중..."):
                    card = random.choice(create_tarot_deck())
                    st.write(ask_ai_direct(f"이름:{name}, 생일:{birth}, 타로카드:{card}로 오늘 운세를 알려줘."))

    elif st.session_state.page == "SAJU":
        st.subheader("📍 평생 사주풀이 실")
        name = st.text_input("성함")
        birth = st.date_input("생년월일 ", value=date(1985, 1, 1), min_value=date(1900, 1, 1))
        if st.button("평생 팔자 확인"):
            if name:
                with st.spinner("단자 펼치는 중..."):
                    st.write(ask_ai_direct(f"이름:{name}, 생일:{birth}. 평생 사주를 자세히 풀어줘."))

    elif st.session_state.page == "2026":
        st.subheader("📍 2026년 대운 실")
        name = st.text_input("이름 ")
        birth = st.date_input("생년월일  ", value=date(1985, 1, 1), min_value=date(1900, 1, 1))
        if st.button("내년 총운 확인"):
            if name:
                with st.spinner("새해 기운 읽는 중..."):
                    st.write(ask_ai_direct(f"이름:{name}, 생일:{birth}. 2026년 운세를 알려줘."))

    elif st.session_state.page == "TAROT":
        st.subheader("📍 78장 타로 상담실")
        quest = st.text_input("고민이 무엇인가?")
        if st.button("카드 3장 뽑기"):
            if quest:
                with st.spinner("카드 섞는 중..."):
                    cards = random.sample(create_tarot_deck(), 3)
                    st.write(ask_ai_direct(f"질문:{quest}, 카드:{cards}로 타로 상담해줘."))
