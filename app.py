import streamlit as st
import google.generativeai as genai

st.title("🧪 할배 도사 시스템 정밀 진단")

try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        st.write("### 1. 연결 상태 확인")
        st.success("✅ API 키 연결 성공!")

        st.write("### 2. 사용 가능한 모델 목록 (이게 핵심입니다)")
        # 사용자님의 키로 호출 가능한 모든 모델 목록을 가져옵니다.
        models = [m.name for m in genai.list_models()]
        
        if models:
            for m in models:
                st.code(m)
            st.info("💡 위 목록에 있는 이름 중 하나를 골라야 404 에러가 나지 않습니다.")
        else:
            st.warning("⚠️ 사용 가능한 모델이 하나도 발견되지 않았습니다.")
            
    else:
        st.error("❌ Secrets에 GOOGLE_API_KEY가 없습니다.")
except Exception as e:
    st.error(f"❌ 진단 중 오류 발생: {e}")
