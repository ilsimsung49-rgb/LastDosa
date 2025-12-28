import streamlit as st
import google.generativeai as genai
import random
from datetime import date

# 1. 페이지 설정 (최상단 필수)
st.set_page_config(page_title="할배 도사 만능 상담소", page_icon="👴", layout="wide")

# 2. AI 모델 설정 (안정적인 모델명 사용)
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # 가장 안정적이고 호환성이 높은 모델명으로 고정
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("⚠️ API 키가 설정되지 않았네! Secrets 확인해보게.")
except Exception as e:
    st.error(f"⚠️ 연결 오류: {e}")

# 3. 78장 타로 덱 정의
def get_tarot_deck():
    major = [f"{i}_Major" for i in range(22)]
    suits = ["Wands", "Cups", "Swords", "Pentacles"]
    ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]
    return major + [f"{rank}_of_{suit}" for suit in suits for rank in ranks]

# 4. 메뉴 상태 관리
if 'menu' not in st.session_state:
    st.session_state.menu = "메인"

# --- [메인 화면] ---
if st.session_state.menu == "메인":
    st.markdown("<h1 style='text-align: center;'>👴 할배 도사 만능 상담소</h1>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    col4, col5, _ = st.columns(3)

    with col1:
        st.markdown("### 🔍 MBTI 족집게 판별")
        if st.button("내 MBTI 맞혀보쇼", key="m1"): st.session_state.menu = "MBTI"; st.rerun()
    with col2:
        st.markdown("### 📅 오늘의 운세")
        if st.button("오늘의 기운 보기", key="m2"): st.session_state.menu = "오늘"; st.rerun()
    with col3:
        st.markdown("### 📜 전체 사주풀이")
        if st.button("평생 팔자 확인", key="m3"): st.session_state.menu = "사주"; st.rerun()
    with col4:
        st.markdown("### 🐉 2026년 대운")
        if st.button("내년 운세 보기", key="m4"): st.session_state.menu = "올해"; st.rerun()
    with col5:
        st.markdown("### 🃏 78장 타로")
        if st.button("고민 상담하기", key="m5"): st.session_state.menu = "타로"; st.rerun()

# --- [상담방 내부] ---
else:
    if st.button("⬅️ 메인으로 돌아가기"): st.session_state.menu = "메인"; st.rerun()
    st.write("---")

    # 1. MBTI 판별 (독심술 방식)
    if st.session_state.menu == "MBTI":
        st.subheader("📍 할배 도사의 MBTI 독심술")
        st.info("👴: '자네 성격이나 평소 습관을 아무렇게나 적어보게. 도사가 딱 맞혀줄 테니!'")
        u_in = st.text_area("도사님께 건넬 말", height=150, key="m_txt")
        if st.button("제 MBTI는 뭔가요?", key="btn_mbti"):
            if u_in:
                with st.spinner("살펴보는 중..."):
                    res = model.generate_content(f"너는 용한 할배 도사야. 글: '{u_in}'. MBTI를 판별하고 노인 말투로 설명해줘.")
                    st.write(res.text)

    # 2. 오늘의 운세 (1900년부터 선택 가능)
    elif st.session_state.menu == "오늘":
        st.subheader("📍 오늘의 운세")
        n_in = st.text_input("이름", key="n_t")
        b_in = st.date_input("생년월일", value=date(1985, 1, 1), min_value=date(1900, 1, 1), key="b_t")
        if st.button("오늘 점괘 보기", key="btn_today"):
            if n_in:
                with st.spinner("기운을 살피는 중..."):
                    card = random.choice(get_tarot_deck())
                    res = model.generate_content(f"이름:{n_in}, 생일:{b_in}. 타로 {card}로 오늘 운세를 노인 말투로 알려줘.")
                    st.write(res.text)

    # 3. 전체 사주풀이 (평생 팔자)
    elif st.session_state.menu == "사주":
        st.subheader("📍 평생 사주팔자 풀이")
        n_in = st.text_input("성함", key="n_s")
        b_in = st.date_input("생년월일 ", value=date(1985, 1, 1), min_value=date(1900, 1, 1), key="b_s")
        t_in = st.text_input("태어난 시간", key="t_s")
        if st.button("평생 운명 확인", key="btn_saju"):
            if n_in:
                with st.spinner("사주 단자를 보는 중..."):
                    res = model.generate_content(f"이름:{n_in}, 생일:{b_in}, 시간:{t_in}. 평생 사주와 평생 운명을 노인 말투로 자세히 풀어줘.")
                    st.write(res.text)

    # 4. 2026년 대운 (올해 운세)
    elif st.session_state.menu == "올해":
        st.subheader("📍 2026년 병오년 대운")
        n_in = st.text_input("성함 ", key="n_y")
        b_in = st.date_input("생년월일  ", value=date(1985, 1, 1), min_value=date(1900, 1, 1), key="b_y")
        if st.button("내년 총운 확인", key="btn_year"):
            if n_in:
                with st.spinner("신년 운세 읽는 중..."):
                    res = model.generate_content(f"이름:{n_in}, 생일:{b_in}. 2026년 재물, 건강, 애정운을 사주 기반 노인 말투로 알려줘.")
                    st.write(res.text)

    # 5. 78장 타로
    elif st.session_state.menu == "타로":
        st.subheader("📍 78장 타로 심층 상담")
        q_in = st.text_input("무엇이 궁금한가?", key="q_ta")
        if st.button("카드 3장 뽑기", key="btn_tarot"):
            if q_in:
                with st.spinner("카드를 섞는 중..."):
                    cards = random.sample(get_tarot_deck(), 3)
                    res = model.generate_content(f"질문:{q_in}, 카드:{cards}. 노인 말투로 타로 상담해줘.")
                    st.write(res.text)
