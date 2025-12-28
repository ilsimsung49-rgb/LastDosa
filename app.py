import streamlit as st
import google.generativeai as genai
import random
from datetime import date

# 1. 앱 설정
st.set_page_config(page_title="할배 도사 만능 상담소", page_icon="👴", layout="wide")

# 2. 모델 설정 (사용자님 목록에서 확인된 gemini-2.0-flash 사용)
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-2.0-flash')
        st.success("✅ 도사님 강림 성공! 남녀 기운을 따로 읽어드림세.")
    else:
        st.error("⚠️ API 키가 없네? Secrets 설정을 확인해주게.")
except Exception as e:
    st.error(f"❌ 시스템 연결 오류: {e}")

# 3. 데이터 구축
def get_tarot():
    major = [f"{i}_Major" for i in range(22)]
    suits = ["Wands", "Cups", "Swords", "Pentacles"]
    ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]
    return major + [f"{rank}_of_{suit}" for rank in ranks for suit in suits]

def get_zodiac(birth_date):
    m, d = birth_date.month, birth_date.day
    if (m == 3 and d >= 21) or (m == 4 and d <= 19): return "양자리"
    elif (m == 4 and d >= 20) or (m == 5 and d <= 20): return "황소자리"
    elif (m == 5 and d >= 21) or (m == 6 and d <= 21): return "쌍둥이자리"
    elif (m == 6 and d >= 22) or (m == 7 and d <= 22): return "게자리"
    elif (m == 7 and d >= 23) or (m == 8 and d <= 22): return "사자자리"
    elif (m == 8 and d >= 23) or (m == 9 and d <= 23): return "처녀자리"
    elif (m == 9 and d >= 24) or (m == 10 and d <= 22): return "천칭자리"
    elif (m == 10 and d >= 23) or (m == 11 and d <= 22): return "전갈자리"
    elif (m == 11 and d >= 23) or (m == 12 and d <= 24): return "사수자리"
    elif (m == 12 and d >= 25) or (m == 1 and d <= 19): return "염소자리"
    elif (m == 1 and d >= 20) or (m == 2 and d <= 18): return "물병자리"
    else: return "물고기자리"

# 4. 메뉴 시스템
if 'page' not in st.session_state: st.session_state.page = "메인"

# --- [메인 로비] ---
if st.session_state.page == "메인":
    st.markdown("<h1 style='text-align: center;'>👴 할배 도사 만능 상담소</h1>", unsafe_allow_html=True)
    st.write("---")
    cols = st.columns(6)
    btns = [("🔍 MBTI", "MBTI"), ("📅 오늘운세", "오늘"), ("📜 사주풀이", "사주"), 
            ("🐉 2026대운", "대운"), ("🃏 타로점", "타로"), ("✨ 별자리", "별자리")]
    for i, (label, target) in enumerate(btns):
        with cols[i]:
            if st.button(label, use_container_width=True):
                st.session_state.page = target
                st.rerun()

# --- [상담실 내부] ---
else:
    if st.button("⬅️ 메인으로"): st.session_state.page = "메인"; st.rerun()
    st.write("---")
    
    # 1. 공통 입력 항목 (성별 추가!)
    u_name = st.text_input("성함", placeholder="이름을 적어주게")
    
    col_gender, col_cal = st.columns(2)
    with col_gender:
        u_gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    with col_cal:
        u_calendar = st.radio("달력 구분", ["양력", "음력"], horizontal=True)
        
    u_birth = st.date_input("생년월일", value=date(1995, 1, 1), min_value=date(1900, 1, 1))

    st.write("---")

    # 도사님께 전달할 기본 정보 정리
    base_info = f"이름:{u_name}, 성별:{u_gender}, 생일:{u_birth}({u_calendar}). "

    # 2. 각 메뉴별 상담 로직
    if st.session_state.page == "MBTI":
        txt = st.text_area("성격이나 평소 습관을 적어보게.")
        if st.button("MBTI 분석 결과 보기"):
            with st.spinner("살펴보는 중..."):
                res = model.generate_content(f"{base_info} 이 글을 토대로 MBTI를 맞히고 노인 말투로 설명해줘: {txt}")
                st.success(f"👴 {u_name}님의 MBTI 분석 결과")
                st.info(res.text)

    elif st.session_state.page == "오늘":
        if st.button("오늘 점괘 보기"):
            with st.spinner("엽전 던지는 중..."):
                card = random.choice(get_tarot())
                res = model.generate_content(f"{base_info} 타로카드 '{card}'로 오늘 하루 운세를 노인 말투로 알려줘.")
                st.success(f"👴 {u_name}님의 오늘 운세 결과")
                st.info(res.text)

    elif st.session_state.page == "사주":
        if st.button("평생 사주 확인하기"):
            with st.spinner("단자 펼치는 중..."):
                res = model.generate_content(f"{base_info} 이 사람의 평생 사주와 운명을 노인 말투로 아주 정성껏 풀어줘.")
                st.success(f"👴 {u_name}님의 평생 사주 분석")
                st.info(res.text)

    elif st.session_state.page == "대운":
        if st.button("2026 대운 결과 보기"):
            with st.spinner("대운 읽는 중..."):
                res = model.generate_content(f"{base_info} 2026년 한 해 운세를 노인 말투로 알려줘.")
                st.success(f"👴 {u_name}님의 2026년 대운 결과")
                st.info(res.text)

    elif st.session_state.page == "타로":
        q = st.text_input("고민이 뭔가?")
        if st.button("타로 카드 점괘 보기"):
            with st.spinner("카드 섞는 중..."):
                cards = random.sample(get_tarot(), 3)
                res = model.generate_content(f"{base_info} 질문:{q}, 카드:{cards}로 타로 상담을 노인 말투로 해줘.")
                st.success(f"👴 {u_name}님의 타로 상담 결과")
                st.info(res.text)

    elif st.session_state.page == "별자리":
        z_sign = get_zodiac(u_birth)
        st.write(f"자네의 수호 별자리는 **'{z_sign}'**이구먼!")
        if st.button("별자리 상세 결과 보기"):
            with st.spinner("밤하늘 읽는 중..."):
                res = model.generate_content(f"{base_info} 별자리:{z_sign}. 특징과 오늘 기운을 노인 말투로 알려줘.")
                st.success(f"👴 {z_sign} 운세 분석")
                st.info(res.text)
