import streamlit as st
import random

st.set_page_config(page_title="내 파우치 꿀조합 레시피", page_icon="💄", layout="centered")

st.title("💄 내 파우치 찰떡 메이크업 레시피")
st.caption("제품 이름만 툭 넣어두고, 오늘 원하는 분위기를 골라봐! ✨")

# 기본 파우치 데이터
if "pouch" not in st.session_state:
    st.session_state.pouch = {
        "palettes": ["클리오 프로 아이 팔레트 [매화빛댕기]"],
        "lips": ["롬앤 쥬시 래스팅 틴트 [베어 그레이프]"],
        "cheeks": ["컬러그램 틴토리 덤 블러셔 [앙큼오브]"]
    }

# 사이드바: 제품 관리
st.sidebar.header("🎒 내 파우치 관리")
category = st.sidebar.selectbox("카테고리 선택", ["팔레트", "립", "치크"])
item_name = st.sidebar.text_input("제품 이름 입력", placeholder="예: 롬앤 피그케어")

if st.sidebar.button("파우치에 쏙 넣기! 💖"):
    if item_name:
        if category == "팔레트":
            st.session_state.pouch["palettes"].append(item_name)
        elif category == "립":
            st.session_state.pouch["lips"].append(item_name)
        elif category == "치크":
            st.session_state.pouch["cheeks"].append(item_name)
        st.sidebar.success(f"추가 완료: {item_name}")
        st.rerun()
    else:
        st.sidebar.warning("제품 이름을 적어줘!")

st.sidebar.divider()
st.sidebar.write("### 🗑️ 등록된 내 화장품 목록")
st.sidebar.write(f"🎨 **팔레트:** {st.session_state.pouch['palettes']}")
st.sidebar.write(f"💄 **립:** {st.session_state.pouch['lips']}")
st.sidebar.write(f"🌸 **치크:** {st.session_state.pouch['cheeks']}")

if st.sidebar.button("전체 초기화"):
    st.session_state.pouch = {"palettes": [], "lips": [], "cheeks": []}
    st.rerun()

# 메인 추천 화면
st.divider()
st.header("✨ 오늘 어울리는 메이크업 조합 룰렛")

mood = st.selectbox("오늘 원하는 무드 선택", [
    "여쿨뮤트 청순여리 메이크업 🌸", 
    "몽환적인 쿨톤 모브 메이크업 💜", 
    "출근/등교용 꾸안꾸 자연스러운 메이크업 🌿", 
    "힙하고 짜릿한 딥쿨 메이크업 🖤"
])

if st.button("🚀 찰떡 조합 & 레시피 뽑기!", type="primary", use_container_width=True):
    p = st.session_state.pouch
    if not p["palettes"] or not p["lips"] or not p["cheeks"]:
        st.error("앗! 팔레트, 립, 치크가 최소 1개씩은 파우치에 있어야 해!")
    else:
        picked_pal = random.choice(p["palettes"])
        picked_lip = random.choice(p["lips"])
        picked_chk = random.choice(p["cheeks"])
        
        st.balloons()
        st.subheader(f"✨ 오늘의 추천 무드: [{mood}]")
        
        st.info(f"""
        * **🎨 아이 팔레트:** {picked_pal}
        * **🌸 치크/블러셔:** {picked_chk}
        * **💄 립 틴트:** {picked_lip}
        """)
        
        st.markdown("### 🪄 오늘 세부 화장법 튜토리얼")
        st.write(f"1. **베이스 세팅:** **[{picked_pal}]**에서 가장 밝고 연한 1번 컬러를 넓은 브러쉬로 눈두덩 전체와 애교살에 슥슥 깔아주기!")
        st.write(f"2. **음영 그라데이션:** 중간 채도의 음영 컬러를 쌍꺼풀 라인 뒤쪽과 삼각존에 가볍게 얹어 깊이감 주기!")
        st.write(f"3. **생기 치크:** **[{picked_chk}]**을 볼 중앙에 톡톡 얹어 수채화 같은 생기 불어넣기!")
        st.write(f"4. **립 마무리:** **[{picked_lip}]**을 입술 안쪽부터 부드럽게 그라데이션해서 맑고 촉촉하게 마무리 💋")
