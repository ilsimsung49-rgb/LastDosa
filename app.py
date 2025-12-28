import streamlit as st
import google.generativeai as genai
import random
from datetime import date

# 1. 앱 설정
st.set_page_config(page_title="할배 도사 만능 상담소", page_icon="👴", layout="wide")

# 2. 모델 설정 (사용자님 환경에서 확인된 gemini-2.0-flash 사용)
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-2.0-flash')
        st.success("✅ 도사님 강림 성공! 음력 사주도 척척 보신다네.")
    else:
        st.error("⚠️ API 키가 없구먼. Secrets 설정을 확인해주게.")
except Exception as e:
    st.error(f"❌ 시스템 연결 오류: {e}")

# 3. 별자리 계산 로직
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

def get_tarot():
    major = [f"{i}_Major" for i in range(22)]
    suits = ["Wands", "Cups", "Swords", "Pentacles"]
    ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]
    return major + [f"{rank}_of_{suit}" for rank in ranks for suit in suits]

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

# --- [상담실] ---
else:
    if st.button("⬅️ 처음으로"): st.session_state.page = "메인"; st.rerun()
    st.write("---")
    
    u_name = st.text_input("상담받을 분 성함", placeholder="김재성")
    col_date, col_type = st.columns([2, 1])
    with col_date:
        u_birth = st.date_input("생년월일", value=date(1995, 1, 1), min_value=date(1900, 1, 1))
    with col_type:
        u_cal = st.radio("구분", ["양력", "음력"], horizontal=True)

    # 공통 프롬프트 생성 (음력 변환 지시 포함)
    base_info = f"이름:{u_name}, 생일:{u_birth}({u_cal} 생일임). "
    if u_cal == "음력":
        # AI에게 음력을 양력으로 정밀 변환하여 계산하라고 강력히 지시합니다.
        base_info += "반드시 이 음력 날짜를 정밀하게 양력으로 변환한 뒤 사주와 기운을 분석해줘. "

    if st.session_state.page == "오늘":
        if st.button("오늘 점괘 보기"):
            with st.spinner("도사님이 기운을 모으는 중..."):
                card = random.choice(get_tarot())
                res = model.generate_content(f"{base_info} 타로카드 '{card}'를 곁들여 오늘 하루 운세를 구수한 사투리 노인 말투로 알려줘.")
                st.write(res.text)

    elif st.session_state.page == "사주":
        if st.button("평생 사주 확인"):
            with st.spinner("사주 단자 펼치는 중..."):
                res = model.generate_content(f"{base_info} 이 사람의 타고난 평생 사주와 팔자를 노인 말투로 아주 자세히 풀어줘.")
                st.write(res.text)

    elif st.session_state.page == "별자리":
        z_sign = get_zodiac(u_birth)
        st.info(f"자네의 수호 별자리는 **'{z_sign}'**이구먼!")
        if st.button("별자리 상세 운세"):
            with st.spinner("밤하늘 별을 읽는 중..."):
                res = model.generate_content(f"{base_info} 별자리 '{z_sign}'의 특징과 오늘 이 별자리의 기운을 노인 말투로 설명해줘.")
                st.write(res.text)
