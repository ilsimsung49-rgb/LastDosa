import streamlit as st
import google.generativeai as genai
import random
from datetime import date

# 1. 앱 설정 (기초 공사)
st.set_page_config(page_title="할배 도사 만능 상담소", page_icon="👴", layout="wide")

# 2. 모델 설정 (사용자님 목록에서 확인된 최신 모델 사용)
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-2.0-flash')
        st.success("✅ 도사님 강림 성공! 이제 모든 점괘를 다 볼 수 있구먼.")
    else:
        st.error("⚠️ API 키가 없네? Secrets 설정을 확인해주게.")
except Exception as e:
    st.error(f"❌ 시스템 연결 오류: {e}")

# 3. 데이터 구축 (타로 및 별자리)
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

# --- [상담실 내부: 결과란 완비] ---
else:
    if st.button("⬅️ 메인으로"): st.session_state.page = "메인"; st.rerun()
    st.write("---")
    
    # 공통 입력 항목
    u_name = st.text_input("성함", placeholder="이름을 적어주게")
    col_date, col_type = st.columns([2, 1])
    with col_date:
        u_birth = st.date_input("생년월일", value=date(1995, 1, 1), min_value=date(1900, 1, 1))
    with col_type:
        u_cal = st.radio("구분", ["양력", "음력"], horizontal=True)

    st.write("---")

    # 1. MBTI 상담 (결과란 포함)
    if st.session_state.page == "MBTI":
        st.subheader("📍 할배 도사의 MBTI 독심술")
        txt = st.text_area("자네 성격이나 평소 습관을 아무렇게나 적어보게.")
        if st.button("MBTI 분석 결과 보기"):
            if txt:
                with st.spinner("도사님이 자네 속을 들여다보는 중..."):
                    res = model.generate_content(f"너는 할배 도사야. 이 사람의 성격을 분석해서 MBTI를 맞히고 노인 말투로 설명해줘: {txt}")
                    st.success("👴 [도사님의 MBTI 분석 결과]")
                    st.info(res.text)

    # 2. 오늘의 운세 (결과란 포함)
    elif st.session_state.page == "오늘":
        st.subheader("📍 오늘의 운세 상담실")
        if st.button("오늘의 운세 결과 보기"):
            if u_name:
                with st.spinner("오늘의 기운을 살피는 중..."):
                    card = random.choice(get_tarot())
                    res = model.generate_content(f"이름:{u_name}, 생일:{u_birth}({u_cal}), 카드:{card}. 오늘 하루 운세를 노인 말투로 알려줘.")
                    st.success(f"👴 [도사님이 읽어준 {u_name}님의 오늘 점괘]")
                    st.info(res.text)

    # 3. 평생 사주 (결과란 포함)
    elif st.session_state.page == "사주":
        st.subheader("📍 평생 사주풀이 상담실")
        if st.button("사주팔자 분석 결과 보기"):
            if u_name:
                with st.spinner("사주 단자를 펼치는 중..."):
                    res = model.generate_content(f"이름:{u_name}, 생일:{u_birth}({u_cal}). 평생 사주와 운명을 노인 말투로 아주 자세히 풀어줘.")
                    st.success(f"👴 [도사님이 풀어낸 {u_name}님의 인생 팔자]")
                    st.info(res.text)

    # 4. 2026 대운 (결과란 포함)
    elif st.session_state.page == "대운":
        st.subheader("📍 2026년 신년 대운 상담실")
        if st.button("2026년 대운 결과 보기"):
            if u_name:
                with st.spinner("내년의 기운을 읽는 중..."):
                    res = model.generate_content(f"이름:{u_name}, 생일:{u_birth}({u_cal}). 2026년 운세를 노인 말투로 알려줘.")
                    st.success(f"👴 [도사님이 알려주는 {u_name}님의 2026년 총운]")
                    st.info(res.text)

    # 5. 타로점 (결과란 포함)
    elif st.session_state.page == "타로":
        st.subheader("📍 78장 타로 상담실")
        q = st.text_input("무엇이 궁금한가? (예: 취직, 연애, 금전 등)")
        if st.button("타로 카드 점괘 보기"):
            if q:
                with st.spinner("카드를 섞고 기운을 모으는 중..."):
                    cards = random.sample(get_tarot(), 3)
                    res = model.generate_content(f"질문:{q}, 카드:{cards}가 나왔으니 타로 상담을 노인 말투로 정성껏 해줘.")
                    st.success(f"👴 [도사님의 타로 카드 상담 내용]")
                    st.info(res.text)

    # 6. 별자리 (결과란 포함)
    elif st.session_state.page == "별자리":
        st.subheader("📍 별자리 운세 상담실")
        z_sign = get_zodiac(u_birth)
        st.write(f"자네는 **'{z_sign}'**이구먼!")
        if st.button("별자리 상세 결과 보기"):
            with st.spinner("밤하늘의 별을 읽는 중..."):
                res = model.generate_content(f"이름:{u_name}, 별자리:{z_sign}. 특징과 오늘 기운을 노인 말투로 알려줘.")
                st.success(f"👴 [도사님이 들려주는 {z_sign} 이야기]")
                st.info(res.text)
