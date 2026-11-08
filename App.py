import streamlit as st
import random

st.set_page_config(page_title="스마트 메이크업 꿀조합 레시피", page_icon="💄", layout="centered")

st.title("🎨 찰떡 톤조합 메이크업 추천기")
st.caption("내 파우치 제품들의 색감과 톤을 맞춰 찰떡 레시피를 만들어드려요! ✨")

# 기본 데이터 세팅
if "pouch" not in st.session_state:
    st.session_state.pouch = {
        "palettes": [
            {
                "brand": "클리오", 
                "name": "프로 아이 팔레트 에어 [매화빛댕기]",
                "tone": "여쿨뮤트",
                "base": "페일아이시핑크",
                "shade": "뮤트더스티핑크",
                "point": "빈티지로즈오브 & 쿨그레이토프"
            }
        ],
        "lips": [
            {"brand": "롬앤", "name": "쥬시 래스팅 틴트 [베어 그레이프]", "tone": "여쿨뮤트", "color_type": "모브 핑크"},
            {"brand": "페리페라", "name": "무드 글로이 틴트 [포도속살]", "tone": "여쿨뮤트", "color_type": "딥 모브"}
        ],
        "cheeks": [
            {"brand": "컬러그램", "name": "틴토리 덤 블러셔 [앙큼오브]", "tone": "여쿨뮤트", "color_type": "라벤더 핑크"}
        ]
    }

# 사이드바: 내 파우치 상세 관리
st.sidebar.header("💄 내 파우치 관리")
tab1, tab2 = st.sidebar.tabs(["➕ 상세 등록", "🗑️ 목록 삭제"])

with tab1:
    st.subheader("새 화장품 상세 추가")
    category = st.selectbox("카테고리", ["팔레트", "립", "치크"])
    brand = st.text_input("브랜드명", placeholder="예: 클리오, 롬앤")
    name = st.text_input("제품명 및 옵션", placeholder="예: 매화빛댕기, 베어그레이프")
    tone = st.selectbox("퍼스널 톤 / 색감", ["여쿨뮤트", "여쿨라이트", "봄웜라이트", "봄웜브라이트", "가을뮤트", "겨울딥/쿨"])
    
    if category == "팔레트":
        st.caption("🎨 팔레트 세부 색상 입력 (추천 레시피용)")
        base_color = st.text_input("베이스 섀도우 색상명", placeholder="예: 페일아이시핑크")
        shade_color = st.text_input("음영 섀도우 색상명", placeholder="예: 뮤트더스티핑크")
        point_color = st.text_input("포인트/삼각존 색상명", placeholder="예: 빈티지로즈오브")
    else:
        color_type = st.text_input("대표 색감 묘사", placeholder="예: 라벤더핑크, 모브, 코랄누드")

    if st.button("파우치에 쏙 넣기! 💖", use_container_width=True):
        if brand and name:
            if category == "팔레트":
                item = {
                    "brand": brand, "name": name, "tone": tone,
                    "base": base_color or "기본 베이스 컬러",
                    "shade": shade_color or "중간 음영 컬러",
                    "point": point_color or "포인트 음영 컬러"
                }
                st.session_state.pouch["palettes"].append(item)
            elif category == "립":
                item = {"brand": brand, "name": name, "tone": tone, "color_type": color_type or "립 컬러"}
                st.session_state.pouch["lips"].append(item)
            elif category == "치크":
                item = {"brand": brand, "name": name, "tone": tone, "color_type": color_type or "치크 컬러"}
                st.session_state.pouch["cheeks"].append(item)
            st.success(f"추가 완료! 🎉 ({brand} - {name})")
            st.rerun()
        else:
            st.warning("브랜드와 제품명을 적어줘!")

with tab2:
    st.write("### 🎨 팔레트")
    for i, item in enumerate(st.session_state.pouch["palettes"]):
        c1, c2 = st.columns([3, 1])
        c1.text(f"[{item['tone']}] {item['brand']} - {item['name']}")
        if c2.button("삭제", key=f"pal_{i}"):
            st.session_state.pouch["palettes"].pop(i)
            st.rerun()

    st.write("### 💄 립")
    for i, item in enumerate(st.session_state.pouch["lips"]):
        c1, c2 = st.columns([3, 1])
        c1.text(f"[{item['tone']}] {item['brand']} - {item['name']}")
        if c2.button("삭제", key=f"lip_{i}"):
            st.session_state.pouch["lips"].pop(i)
            st.rerun()

    st.write("### 🌸 치크")
    for i, item in enumerate(st.session_state.pouch["cheeks"]):
        c1, c2 = st.columns([3, 1])
        c1.text(f"[{item['tone']}] {item['brand']} - {item['name']}")
        if c2.button("삭제", key=f"chk_{i}"):
            st.session_state.pouch["cheeks"].pop(i)
            st.rerun()

# 메인 추천 로직
st.divider()
st.header("✨ 톤맞춤 메이크업 꿀조합 룰렛")

target_tone = st.selectbox("오늘 맞추고 싶은 분위기/톤 선택!", ["전체 랜덤", "여쿨뮤트", "여쿨라이트", "봄웜라이트", "봄웜브라이트", "가을뮤트", "겨울딥/쿨"])

if st.button("🚀 찰떡 톤조합 메이크업 뽑기!", type="primary", use_container_width=True):
    p = st.session_state.pouch
    if not p["palettes"] or not p["lips"] or not p["cheeks"]:
        st.error("앗! 팔레트, 립, 치크가 최소 1개씩은 등록되어 있어야 해 ㅠㅠ")
    else:
        # 1. 톤 필터링 또는 메인 기준 잡기
        if target_tone != "전체 랜덤":
            matched_palettes = [item for item in p["palettes"] if item["tone"] == target_tone] or p["palettes"]
            matched_cheeks = [item for item in p["cheeks"] if item["tone"] == target_tone] or p["cheeks"]
        else:
            matched_palettes = p["palettes"]
            matched_cheeks = p["cheeks"]

        # 2. 메인 블러셔/팔레트 먼저 픽!
        picked_chk = random.choice(matched_cheeks)
        picked_pal = random.choice(matched_palettes)
        
        # 3. 메인 블러셔 톤과 가장 잘 어울리는 립 맞춤 픽스!
        matched_lips = [item for item in p["lips"] if item["tone"] == picked_chk["tone"]]
        if not matched_lips: # 동일 톤이 없으면 전체에서 선택
            matched_lips = p["lips"]
        picked_lip = random.choice(matched_lips)

        st.balloons()
        st.subheader(f"🌸 메인 기준: [{picked_chk['tone']}] 찰떡 톤조합 완성!")
        
        st.info(f"""
        * **🌸 주인공 치크:** {picked_chk['brand']} - {picked_chk['name']} ({picked_chk.get('color_type', '치크')})
        * **💄 찰떡 짝꿍 립:** {picked_lip['brand']} - {picked_lip['name']} ({picked_lip.get('color_type', '립')})
        * **🎨 매칭 팔레트:** {picked_pal['brand']} - {picked_pal['name']}
        """)

        st.markdown("### 🪄 오늘 세부 화장법 튜토리얼")
        st.write(f"1. **눈가 쿨 베이스 세팅:** **[{picked_pal['name']}]**의 **'{picked_pal.get('base', '베이스 색상')}'** 컬러를 넓은 브러쉬로 눈두덩 전체에 깔아 화사하게 밝혀주기.")
        st.write(f"2. **음영 그라데이션:** **'{picked_pal.get('shade', '음영 색상')}'** 컬러를 쌍꺼풀 라인에 발라 붓기 빠진 자연스러운 음영 완성.")
        st.write(f"3. **깊이감 & 포인트:** **'{picked_pal.get('point', '포인트 색상')}'**으로 눈꼬리 아우터 V영역과 삼각존을 채워 탁 트인 눈매 만들기.")
        st.write(f"4. **치크 얹기:** **[{picked_chk['name']}]**으로 양 볼 중앙에 톡톡 쓸어 생기 더하기.")
        st.write(f"5. **립 마무리:** **[{picked_lip['name']}]**을 입술 안쪽부터 부드럽게 바르면 톤 어그로 없는 찰떡 조합 완성 💋")


