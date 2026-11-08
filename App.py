import streamlit as st
import random
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="사진 첨부형 AI 메이크업 꿀조합", page_icon="💄", layout="centered")

st.title("📸 사진 첨부형 AI 메이크업 파우치")
st.caption("화장품 사진만 찍어 올리면, AI가 섀도우 위치와 색감을 분석해 완벽한 레시피를 짜드려요! ✨")

# 1. API 키 입력
st.sidebar.header("🔑 AI 설정")
api_key = st.sidebar.text_input("Gemini API Key 입력", type="password", placeholder="AI 기능을 쓰려면 키를 넣어줘!")

# 세션 데이터 초기화
if "pouch" not in st.session_state:
    st.session_state.pouch = {
        "palettes": [],
        "lips": [],
        "cheeks": []
    }

# 사이드바: 사진 첨부하여 제품 추가
st.sidebar.header("💄 내 파우치 관리")
tab1, tab2 = st.sidebar.tabs(["📸 사진 등록", "🗑️ 목록 삭제"])

with tab1:
    category = st.selectbox("카테고리", ["팔레트", "립", "치크"])
    item_name = st.text_input("제품 별칭/이름", placeholder="예: 클리오 매화빛댕기, 롬앤 베어그레이프")
    uploaded_file = st.file_uploader("화장품 사진 첨부하기 (캡처/촬영)", type=["png", "jpg", "jpeg"])
    
    if st.button("사진으로 파우치에 쏙! 💖", use_container_width=True):
        if item_name and uploaded_file:
            img = Image.open(uploaded_file)
            item = {"name": item_name, "image": img}
            
            if category == "팔레트":
                st.session_state.pouch["palettes"].append(item)
            elif category == "립":
                st.session_state.pouch["lips"].append(item)
            elif category == "치크":
                st.session_state.pouch["cheeks"].append(item)
                
            st.success(f"추가 완료! 🎉 ({item_name})")
            st.rerun()
        else:
            st.warning("제품 이름이랑 사진을 모두 등록해 줘!")

with tab2:
    st.write("### 🎨 팔레트")
    for i, item in enumerate(st.session_state.pouch["palettes"]):
        c1, c2 = st.columns([3, 1])
        c1.image(item["image"], caption=item["name"], width=100)
        if c2.button("삭제", key=f"pal_{i}"):
            st.session_state.pouch["palettes"].pop(i)
            st.rerun()

    st.write("### 💄 립")
    for i, item in enumerate(st.session_state.pouch["lips"]):
        c1, c2 = st.columns([3, 1])
        c1.image(item["image"], caption=item["name"], width=100)
        if c2.button("삭제", key=f"lip_{i}"):
            st.session_state.pouch["lips"].pop(i)
            st.rerun()

    st.write("### 🌸 치크")
    for i, item in enumerate(st.session_state.pouch["cheeks"]):
        c1, c2 = st.columns([3, 1])
        c1.image(item["image"], caption=item["name"], width=100)
        if c2.button("삭제", key=f"chk_{i}"):
            st.session_state.pouch["cheeks"].pop(i)
            st.rerun()

# 메인 추천 및 AI 레시피 로직
st.divider()
st.header("✨ 오늘 어울리는 조합 뽑기")

mood = st.selectbox("오늘 원하는 무드 선택", [
    "여쿨뮤트 청순여리 메이크업 🌸", 
    "다얼자 몽환 쿨톤 메이크업 💜", 
    "출근/등교용 꾸안꾸 자연스러운 메이크업 🌿", 
    "힙하고 짜릿한 딥쿨 메이크업 🖤"
])

if st.button("🚀 찰떡 조합 & AI 레시피 생성!", type="primary", use_container_width=True):
    p = st.session_state.pouch
    if not p["palettes"] or not p["lips"] or not p["cheeks"]:
        st.error("앗! 팔레트, 립, 치크 사진을 최소 1개씩은 파우치에 등록해 줘!")
    else:
        picked_pal = random.choice(p["palettes"])
        picked_lip = random.choice(p["lips"])
        picked_chk = random.choice(p["cheeks"])
        
        st.balloons()
        st.subheader(f"✨ 오늘의 찰떡 조합 [{mood}]")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("**🎨 아이 팔레트**")
            st.image(picked_pal["image"], caption=picked_pal["name"])
        with col2:
            st.write("**🌸 치크/블러셔**")
            st.image(picked_chk["image"], caption=picked_chk["name"])
        with col3:
            st.write("**💄 립**")
            st.image(picked_lip["image"], caption=picked_lip["name"])
            
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                너는 트렌디한 뷰티 아티스트야. 첨부된 3장의 화장품 사진(아이 팔레트, 치크, 립)을 직접 눈으로 정밀 분석해줘.
                요청된 무드: [{mood}]

                [메이크업 레시피 작성 규칙]
                1. **아이 팔레트 분석 (매우 중요):**
                   - 사진 속 팔레트의 섀도우 배치와 색상을 직관적으로 보고, "상단 첫 번째 연한 베이스 컬러", "중간 음영 컬러", "포인트/삼각존 컬러" 등을 구체적인 위치와 함께 짚어줘.
                2. **치크 & 립 톤 매칭:**
                   - 사진으로 확인된 치크와 립의 실물 색감이 팔레트와 어떻게 어우러지는지 짝꿍 포인트를 설명해줘.
                3. **말투 및 형식:**
                   - 친근하고 감성적인 뷰티 유튜버/아티스트 말투로 단계별 튜토리얼(1단계~5단계)을 작성해줘.
                """
                
                with st.spinner("AI가 올린 사진 속 섀도우 위치와 색감을 분석하는 중... 📸"):
                    response = model.generate_content([prompt, picked_pal["image"], picked_chk["image"], picked_lip["image"]])
                    st.markdown("### 🪄 사진 분석 AI 맞춤 레시피")
                    st.write(response.text)
            except Exception as e:
                st.error(f"API 분석 중 오류 발생: {e}")
        else:
            st.info("💡 사이드바에 **Gemini API Key**를 넣으면, 올린 사진 속 섀도우 위치와 색감을 AI가 직접 읽어서 100% 맞춤형 튜토리얼을 짜 준답니다!")
