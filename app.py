import streamlit as st
import google.generativeai as genai
import random
import datetime

# 1. 도사님 설정 (에러 방지용 모델 자동 선택 로직)
genai.configure(api_key="AIzaSyCLYFZyJJTUrGiV9e24Uud8o234Ic54RaI")

def get_dosa_model():
    """에러를 방지하기 위해 사용 가능한 모델을 자동으로 찾아 연결합니다."""
    try:
        # 현재 사용 가능한 모델 목록을 가져옵니다.
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return genai.GenerativeModel(m.name)
    except:
        # 목록을 못 가져올 경우 가장 안정적인 기본 모델을 사용합니다.
        return genai.GenerativeModel('gemini-1.5-flash')

model = get_dosa_model()

# 2. 화면 디자인
st.set_page_config(page_title="할배 도사 만능 상담소", page_icon="🔮", layout="wide")

# 사이드바 메뉴
st.sidebar.title("🔮 도사님 주특기")
menu = st.sidebar.selectbox("원하는 점사를 고르쇼:", 
    ["🏠 메인 화면", "📅 사주/궁합", "🃏 신점 타로", "🧠 MBTI 정밀진단", "💑 연애운 & MBTI궁합", "🩸 혈액형 궁합"])

st.sidebar.markdown("---")
st.sidebar.write("📺 **유튜브 @jsd_in 대박 기원!**")

# --- 기능 1: 메인 화면 ---
if menu == "🏠 메인 화면":
    st.title("👴 할배 도사 천하제일 상담소")
    st.image("https://images.unsplash.com/photo-1534190760961-74e8c1c5c3da?q=80&w=1000")
    st.header("어서 오쇼! 인생 모든 풍파, 내가 다 해결해 줄라니까!")

# --- 기능 2: 사주/궁합 ---
elif menu == "📅 사주/궁합":
    st.title("📅 사주명리 & 인생 풀이")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("이름이 뭐여?", placeholder="홍길동")
        gender = st.radio("성별은?", ["남성", "여성"])
    with col2:
        birth_date = st.date_input("생년월일이 언제여?", min_value=datetime.date(1920, 1, 1))
        birth_time = st.time_input("태어난 시는?", value=datetime.time(12, 0))
    
    if st.button("내 팔자 좀 봐주쇼!"):
        with st.spinner("도사님이 돋보기 찾는 중..."):
            try:
                res = model.generate_content(f"{name}({gender}), {birth_date} {birth_time}생의 사주를 80대 할배 사투리로 풀이해줘.")
                st.success(f"👴 {name} 도령/낭자, 잘 들으쇼!")
                st.write(res.text)
            except Exception as e:
                st.error("아이구야, 신령님이 노하셨나보다. 다시 한번 눌러보쇼!")

# --- 기능 3: 신점 타로 (이미지 보강) ---
elif menu == "🃏 신점 타로":
    st.title("🃏 도사님의 영험한 타로")
    st.image("https://images.unsplash.com/photo-1590483734724-38fa19dd7423?q=80&w=1000", width=400)
    
    tarot_cards = {
        "The Sun": "https://upload.wikimedia.org/wikipedia/commons/9/94/RWS_Tarot_19_Sun.jpg",
        "The Moon": "https://upload.wikimedia.org/wikipedia/commons/7/7f/RWS_Tarot_18_Moon.jpg",
        "The Lovers": "https://upload.wikimedia.org/wikipedia/commons/d/db/RWS_Tarot_06_Lovers.jpg",
        "The Death": "https://upload.wikimedia.org/wikipedia/commons/d/d7/RWS_Tarot_13_Death.jpg"
    }

    if st.button("카드 한 장 주쇼!"):
        card = random.choice(list(tarot_cards.keys()))
        st.subheader(f"✨ 당신이 뽑은 카드는: {card}")
        st.image(tarot_cards[card], width=250)
        with st.spinner("해석 중..."):
            res = model.generate_content(f"타로 '{card}' 카드를 80대 할배 사투리로 화끈하게 풀이해줘.")
            st.write(res.text)

# --- 기능 4: MBTI 정밀진단 (12문항) ---
elif menu == "🧠 MBTI 정밀진단":
    st.title("🧠 도사님의 족집게 MBTI 진단")
    st.write("12가지 질문에 답하면 네놈의 정체를 밝혀주마!")
    
    questions = [
        "1. 처음 본 사람과도 말을 잘 섞나?", "2. 계획이 틀어지면 화가 나나?", "3. 슬픈 영화 보면 눈물이 나나?",
        "4. 사람 많은 곳에 가면 기가 빨리나?", "5. 남 눈치를 많이 보는 편인가?", "6. 정리정돈이 취미인가?",
        "7. 현실보다 상상을 많이 하나?", "8. 결과보다 과정이 중요한가?", "9. 남의 말에 공감을 잘 해주나?",
        "10. 호불호가 확실한가?", "11. 일단 저지르고 보나?", "12. 가끔 혼자만의 시간이 절실한가?"
    ]
    ans = []
    for q in questions:
        ans.append(st.radio(q, ["그렇다", "아니다"], horizontal=True))
    
    if st.button("내 정체가 뭐여?"):
        with st.spinner("관상 보는 중..."):
            res = model.generate_content(f"답변: {ans}. 이 내용을 바탕으로 MBTI를 추측하고 특징을 할배 사투리로 말해줘.")
            st.write(res.text)

# --- 기능 5: 연애운 & MBTI궁합 ---
elif menu == "💑 연애운 & MBTI궁합":
    st.title("💑 도사님의 화끈한 연애 상담소")
    mbtis = ["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP", "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"]
    col1, col2 = st.columns(2)
    my_m = col1.selectbox("니 MBTI가 뭐여?", mbtis)
    target_m = col2.selectbox("그놈/그년 MBTI는?", mbtis)
    situation = st.text_input("지금 고민이 뭐여? (예: 썸 타는 중, 싸움, 짝사랑)")
    
    if st.button("우리 잘될까?"):
        with st.spinner("궁합 보는 중..."):
            res = model.generate_content(f"내 MBTI {my_m}, 상대 {target_m}, 상황: {situation}. 연애운을 할배 사투리로 알려줘.")
            st.write(res.text)

# --- 기능 6: 혈액형 궁합 ---
elif menu == "🩸 혈액형 궁합":
    st.title("🩸 피는 못 속여! 혈액형 궁합")
    blood_types = ["A형", "B형", "O형", "AB형"]
    col1, col2 = st.columns(2)
    my_b = col1.radio("니 혈액형?", blood_types)
    your_b = col2.radio("상대 혈액형?", blood_types)
    
    if st.button("우리 피가 잘 맞나?"):
        with st.spinner("피 섞어보는 중..."):
            res = model.generate_content(f"{my_b}와 {your_b}의 혈액형 궁합을 할배 사투리로 말해줘.")
            st.write(res.text)


