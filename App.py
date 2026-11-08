import streamlit as st
import json

# 페이지 기본 설정
st.set_page_config(page_title="오늘의 메이크업 꿀조합", page_icon="💄", layout="centered")

st.title("🎨 오늘의 맞춤 메이크업 추천기")
st.caption("내 파우치 속 화장품으로 매일매일 인스타 재질 메이크업 레시피 짜기! ✨")

# 브라우저 로컬 스토리지 데이터 관리 (새로고침해도 유지!)
if "pouch" not in st.session_state:
    st.session_state.pouch = {
        "palettes": [{"brand": "클리오", "name": "프로 아이 팔레트 에어 [매화빛댕기]"}],
        "lips": [{"brand": "롬앤", "name": "쥬시 래스팅 틴트 [베어 그레이프]"}],
        "cheeks": [{"brand": "컬러그램", "name": "틴토리 덤 블러셔 [앙큼오브]"}]
    }

# 사이드바: 파우치 관리
st.sidebar.header("💄 내 파우치 관리")
tab1, tab2 = st.sidebar.tabs(["➕ 화장품 추가", "🗑️ 목록 관리"])

with tab1:
    category = st.selectbox("카테고리", ["팔레트", "립", "치크"])
    brand = st.text_input("브랜드명", placeholder="예: 클리오, 롬앤")
    name = st.text_input("제품명 및 색상", placeholder="예: 매화빛댕기, 바인누드")
    
    if st.button("파우치에 쏙 넣기! 💖", use_container_width=True):
        if brand and name:
            item = {"brand": brand, "name": name}
            if category == "팔레트":
                st.session_state.pouch["palettes"].append(item)
            elif category == "립":
                st.session_state.pouch["lips"].append(item)
            elif category == "치크":
                st.session_state.pouch["cheeks"].append(item)
            st.success(f"추가 완료! 🎉 ({brand} - {name})")
            st.rerun()
        else:
            st.warning("브랜드랑 이름을 모두 적어줘!")

with tab2:
    st.write("### 🎨 팔레트")
    for i, item in enumerate(st.session_state.pouch["palettes"]):
        c1, c2 = st.columns([3, 1])
        c1.text(f"{item['brand']} - {item['name']}")
        if c2.button("삭제", key=f"pal_{i}"):
            st.session_state.pouch["palettes"].pop(i)
            st.rerun()

    st.write("### 💄 립")
    for i, item in enumerate(st.session_state.pouch["lips"]):
        c1, c2 = st.columns([3, 1])
        c1.text(f"{item['brand']} - {item['name']}")
        if c2.button("삭제", key=f"lip_{i}"):
            st.session_state.pouch["lips"].pop(i)
            st.rerun()

    st.write("### 🌸 치크")
    for i, item in enumerate(st.session_state.pouch["cheeks"]):
        c1, c2 = st.columns([3, 1])
        c1.text(f"{item['brand']} - {item['name']}")
        if c2.button("삭제", key=f"chk_{i}"):
            st.session_state.pouch["cheeks"].pop(i)
            st.rerun()

# 메인 화면: 룰렛 & 레시피
st.divider()
st.header("✨ 오늘의 메이크업 추천 룰렛")

mood = st.selectbox("오늘 어떤 분위기로 연출할까?", [
    "여쿨뮤트 청순여리 메이크업 🌸", 
    "다얼자 몽환 쿨톤 메이크업 💜", 
    "출근/등교용 꾸안꾸 자연스러운 메이크업 🌿", 
    "힙하고 짜릿한 딥쿨 메이크업 🖤"
])

import random

if st.button("🚀 오늘 화장 조합 뽑기!", type="primary", use_container_width=True):
    p = st.session_state.pouch
    if not p["palettes"] or not p["lips"] or not p["cheeks"]:
        st.error("앗! 팔레트, 립, 치크가 최소 1개씩은 파우치에 있어야 해 ㅠㅠ 왼쪽 사이드바에서 추가해 줘!")
    else:
        picked_pal = random.choice(p["palettes"])
        picked_lip = random.choice(p["lips"])
        picked_chk = random.choice(p["cheeks"])
        
        st.balloons()
        st.subheader(f"✨ 오늘의 추천 무드: [{mood}]")
        
        # 카드 형태로 예쁘게 출력
        with st.container():
            st.markdown("#### 🛍️ 오늘의 내 화장품 픽!")
            st.info(f"""
            * **🎨 아이 팔레트:** {picked_pal['brand']} - {picked_pal['name']}
            * **🌸 치크/블러셔:** {picked_chk['brand']} - {picked_chk['name']}
            * **💄 립 틴트:** {picked_lip['brand']} - {picked_lip['name']}
            """)
            
            st.markdown("#### 🪄 튜토리얼 메이크업 레시피")
            st.write(f"1. **베이스 셋팅:** **{picked_pal['name']}**에서 가장 연한 베이스 섀도우를 넓게 쓸어 밝혀주기!")
            st.write(f"2. **음영 스머징:** 중간 톤 색상으로 쌍꺼풀 라인부터 삼각존까지 자연스럽게 음영 넣기!")
            st.write(f"3. **치크 톡톡:** **{picked_chk['name']}**으로 양 볼 중앙에 얹어 러블리 생기 더하기!")
            st.write(f"4. **립 그라데이션:** **{picked_lip['name']}**을 입술 안쪽부터 그라데이션해서 맑게 연출해주면 완성 💋")
