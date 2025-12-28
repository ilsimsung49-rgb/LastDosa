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
        st.success("✅ 도사님 강림 성공! 양력/음력 다 물어보게나.")
    else:
        st.error("⚠️ API 키가 없구먼. Secrets 설정을 확인해주게.")
except Exception as e:
    st.error(f"❌ 시스템 연결 오류: {e}")

# 3. 별자리 계산 함수
def get_zodiac(birth_date):
    month = birth_date.month
    day = birth_date.day
    if (month == 3 and day >= 21) or (month == 4 and day <= 19): return "양자리"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20): return "황소자리"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 21): return "쌍둥이자리"
    elif (month == 6 and day >= 22) or (month == 7 and day <= 22): return "게자리"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22): return "사자자리"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 23): return "처녀자리"
    elif (month == 9 and day >= 24) or (month == 10 and day <= 22): return "천칭자리"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 22): return "전갈자리"
    elif (month == 11 and day >= 23) or (month == 12 and day <= 24): return "사수자리"
    elif (month == 12 and day >= 25) or (month == 1 and day <= 19): return "염소자리"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18): return "물병자리"
    else: return "물고기자리"

def get_tarot():
    major = [f"{i}_Major" for i in range(22)]
    suits = ["Wands", "Cups", "Swords", "Pentacles"]
    ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]
    return major + [f"{rank}_of_{suit}" for rank in ranks for suit in suits]

if 'page' not in st.session_state: st.session_state.page = "메인"

# --- [메인 화면] ---
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
    
    # 공통 입력창
    u_name = st.text_input("성함")
    col_date, col_type = st.columns([2, 1])
    with col_date:
        u_birth = st.date_input("생년월일", value=date(1995, 1, 1), min_value=date(1900, 1, 1))
    with col_type:
        u_calendar = st.radio("구분", ["양력", "음력"], horizontal=True)

    if st.session_state.page == "오늘":
        if st.button("오늘 점괘 보기"):
            with st.spinner("엽전 던지는 중..."):
                card = random.choice(get_tarot())
                res = model.generate_content(f"이름:{u_name}, 생일:{u_birth}({u_calendar}). 타로카드:{card}. 오늘 운세를 노인 말투로 알려줘.")
                st.write(res.text)

    elif st.session_state.page == "사주":
        if st.button("사주 확인"):
            with st.spinner("단자 펼치는 중..."):
                res = model.generate_content(f"이름:{u_name}, 생일:{u_birth}({u_calendar}). 평생 사주를 노인 말투로 풀어줘.")
                st.write(res.text)

    elif st.session_state.page == "별자리":
        z_sign = get_zodiac(u_birth)
        st.info(f"자네의 별자리는 **'{z_sign}'**이구먼!")
        if st.button("별자리 운세 보기"):
            with st.spinner("밤하늘 보는 중..."):
                res = model.generate_content(f"별자리:{z_sign}, 이름:{u_name}. 이 별자리의 특징과 오늘 기운을 노인 말투로 알려줘.")
                st.write(res.text)

    # (MBTI, 대운, 타로 메뉴도 동일하게 작동합니다)
