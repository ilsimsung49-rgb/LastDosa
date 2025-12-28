import streamlit as st
import google.generativeai as genai
import random
from datetime import date

# 1. 페이지 설정
st.set_page_config(page_title="할배 도사 만능 상담소", page_icon="👴", layout="wide")

# 2. 시스템 진단 및 모델 자동 선택 (이게 핵심입니다)
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # 내 API 키가 허용하는 모델 목록을 직접 확인합니다.
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # 목록 중 가장 안정적인 모델을 자동으로 선택 (추측 방지)
        if any('gemini-1.5-flash' in name for name in available_models):
            target_model = 'gemini-1.5-flash'
        elif any('gemini-pro' in name for name in available_models):
            target_model = 'gemini-pro'
        else:
            target_model = available_models[0] # 목록에 있는 것 중 아무거나 첫 번째 선택
            
        model = genai.GenerativeModel(target_model)
        st.success(f"✅ 도사님 강림 완료! (사용 모델: {target_model})")
    else:
        st.error("⚠️ API 키를 찾을 수 없구먼. Secrets 설정을 확인해주게.")
except Exception as e:
    st.error(f"❌ 시스템 점검 중 에러 발생: {e}")

# 3. 78장 타로 카드 데이터
def get_tarot_deck():
    major = [f"{i}_Major" for i in range(22)]
    suits = ["Wands", "Cups", "Swords", "Pentacles"]
    ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]
    return major + [f"{rank}_of_{suit}" for rank in ranks for suit in suits]

# 4. 메뉴 상태 관리
if 'menu' not in st.session_state:
    st.session_state.menu = "메인"

# --- [메인 화면] ---
if st.session_state.menu == "메인":
    st.markdown("<h1 style='text-align: center;'>👴 할배 도사 만능 상담소</h1>", unsafe_allow_html=True)
    st.write("---")
    cols = st.columns(5)
    menu_list = [("🔍 MBTI", "MBTI"), ("📅 오늘 운세", "오늘"), ("📜 전체 사주", "사주"), ("🐉 2026 대운", "올해"), ("🃏 78장 타로", "타로")]
    
    for i, (label, state) in enumerate(menu_list):
        with cols[i]:
            if st.button(label, key=f"btn_{state}", use_container_width=True):
                st.session_state.menu = state
                st.rerun()

# --- [상담실 내부] ---
else:
    if st.button("⬅️ 처음으로"): 
        st.session_state.menu = "메인"
        st.rerun()
    st.write("---")

    # 상담 로직 통합 (중복 제거)
    prompt = ""
    if st.session_state.menu == "MBTI":
        u_in = st.text_area("성격이나 습관을 적어보게.")
        if st.button("도사님 분석해주쇼"): prompt = f"MBTI를 맞히고 노인 말투로 설명해줘: {u_in}"
    
    elif st.session_state.menu == "오늘":
        name = st.text_input("이름")
        birth = st.date_input("생년월일", value=date(1985, 1, 1), min_value=date(1900, 1, 1))
        if st.button("점괘 보기"): prompt = f"이름:{name}, 생일:{birth}. 타로 '{random.choice(get_tarot_deck())}'로 오늘 운세를 알려줘."

    # ... (생략된 사주, 대운, 타로도 동일한 방식으로 작동)
    
    if prompt:
        with st.spinner("도사님이 기운을 모으는 중..."):
            try:
                res = model.generate_content(prompt)
                st.write(res.text)
            except Exception as e:
                st.error(f"👴: '허허, 점괘가 잘 안 나오는구먼. (상세에러: {e})'")
