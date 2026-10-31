import streamlit as st
import json
import os
import re

# Page Configuration
st.set_page_config(
    page_title="Med-Lingo: 의대 기출 퀘스트",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished Duolingo / Modern Web App Look & Bottom Floating Bar
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
    .stApp {
        background-color: #F8FAFC;
    }

    /* -------------------------------------------------------------
       1. 상단 네비게이션 헤더 버튼 스타일 (우측 뱃지와 크기/높이 통일)
       ------------------------------------------------------------- */
    div[data-testid="stButton"] > button[key="global_home_btn"],
    div[data-testid="stButton"] > button[key="global_selector_btn"] {
        min-height: 44px !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        padding: 6px 16px !important;
        border: 1.5px solid #CBD5E1 !important;
        background-color: white !important;
        color: #1E293B !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stButton"] > button[key="global_home_btn"]:hover,
    div[data-testid="stButton"] > button[key="global_selector_btn"]:hover {
        border-color: #6366F1 !important;
        color: #4F46E5 !important;
        background-color: #EEF2FF !important;
    }

    /* -------------------------------------------------------------
       2. 홈 화면 히어로 카드 & 풀러가기 대형 버튼
       ------------------------------------------------------------- */
    .hero-card {
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%);
        border-radius: 24px;
        padding: 40px 32px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.4);
    }
    
    .hero-title {
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 12px;
        letter-spacing: -0.5px;
    }
    
    .hero-sub {
        font-size: 18px;
        opacity: 0.95;
        max-width: 620px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* 히어로 카드 너비와 동일한 대형 풀러가기 버튼 */
    div[data-testid="stButton"] > button[key="home_start_hero_btn"] {
        min-height: 72px !important;
        font-size: 22px !important;
        font-weight: 800 !important;
        border-radius: 18px !important;
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 8px 20px -3px rgba(16, 185, 129, 0.4) !important;
        transition: all 0.2s ease !important;
        margin-bottom: 24px !important;
    }
    div[data-testid="stButton"] > button[key="home_start_hero_btn"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 24px -2px rgba(16, 185, 129, 0.5) !important;
    }
    
    /* Stats & Feature Cards */
    .stat-box {
        background: white;
        border: 2px solid #E2E8F0;
        border-radius: 18px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03);
    }
    .stat-number {
        font-size: 28px;
        font-weight: 800;
        color: #4F46E5;
        margin-bottom: 4px;
    }
    .stat-label {
        font-size: 14px;
        font-weight: 600;
        color: #64748B;
    }

    /* -------------------------------------------------------------
       3. 문제 풀이 화면 상단 바 (목록으로 / 별표하기 버튼 확대)
       ------------------------------------------------------------- */
    div[data-testid="stButton"] > button[key="quiz_back_to_list"],
    div[data-testid="stButton"] > button[key^="quiz_star_"] {
        min-height: 48px !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        border-radius: 14px !important;
        padding: 8px 18px !important;
        border: 2px solid #CBD5E1 !important;
        background: white !important;
        color: #1E293B !important;
    }
    div[data-testid="stButton"] > button[key="quiz_back_to_list"]:hover {
        border-color: #6366F1 !important;
        color: #4F46E5 !important;
        background: #EEF2FF !important;
    }

    /* Question Card */
    .question-card {
        background: white;
        border: 2px solid #E2E8F0;
        border-radius: 20px;
        padding: 28px 24px 24px 24px;
        box-shadow: 0 6px 12px -2px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .question-badge {
        display: inline-block;
        background-color: #EEF2FF;
        color: #4338CA;
        font-size: 14px;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 10px;
        margin-bottom: 14px;
    }
    .question-text {
        font-size: 20px;
        font-weight: 700;
        color: #1E293B;
        line-height: 1.65;
    }

    /* Feedback Bars */
    .feedback-correct {
        background-color: #D1FAE5;
        border: 2px solid #10B981;
        border-radius: 16px;
        padding: 18px 22px;
        margin-top: 14px;
        margin-bottom: 20px;
        color: #065F46;
    }
    .feedback-wrong {
        background-color: #FEE2E2;
        border: 2px solid #EF4444;
        border-radius: 16px;
        padding: 18px 22px;
        margin-top: 14px;
        margin-bottom: 20px;
        color: #991B1B;
    }

    /* 선지 네모 박스 스타일링 */
    div[data-testid="stRadio"] > label,
    div[data-testid="stRadio"] label[data-testid="stWidgetLabel"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 0 10px 0 !important;
        cursor: default !important;
        font-size: 17px !important;
        font-weight: 800 !important;
        color: #1E293B !important;
    }
    div[data-testid="stRadio"] > label:hover,
    div[data-testid="stRadio"] label[data-testid="stWidgetLabel"]:hover {
        border: none !important;
        background: transparent !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-bottom: 30px;
    }
    
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        background-color: white !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 14px !important;
        padding: 16px 20px !important;
        margin: 0 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
    }
    
    div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
        border-color: #10B981 !important;
        background-color: #F0FDF4 !important;
    }
    
    div[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"],
    div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
        border-color: #10B981 !important;
        background-color: #ECFDF5 !important;
        color: #065F46 !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 10px rgba(16, 185, 129, 0.15) !important;
    }

    .choice-card-correct {
        background-color: #EFF6FF !important;
        border: 2px solid #2563EB !important;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 12px;
        color: #1E40AF;
        font-weight: 700;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.12);
    }

    .choice-card-wrong {
        background-color: #FEF2F2 !important;
        border: 2px solid #EF4444 !important;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 12px;
        color: #B91C1C;
        font-weight: 700;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 10px rgba(239, 68, 68, 0.12);
    }

    .choice-card-dimmed {
        background-color: #F8FAFC !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 12px;
        color: #64748B;
        opacity: 0.85;
    }

    /* -------------------------------------------------------------
       4. 화면 하단 고정 플로팅 액션 바 (Sticky / Fixed Action Bar)
       ------------------------------------------------------------- */
    .bottom-bar-spacer {
        height: 120px; /* 고정 바가 화면 내용을 가리지 않도록 바닥 여백 추가 */
    }

    div[data-testid="stVerticalBlock"]:has(> div.bottom-floating-anchor) {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background: rgba(255, 255, 255, 0.94) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border-top: 2px solid #CBD5E1 !important;
        padding: 14px 28px !important;
        z-index: 99999 !important;
        box-shadow: 0 -8px 24px rgba(0, 0, 0, 0.08) !important;
    }

    /* 하단 고정 바 내부 버튼들의 크기 및 높이 대폭 확대 */
    div[data-testid="stVerticalBlock"]:has(> div.bottom-floating-anchor) button {
        min-height: 56px !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        border-radius: 14px !important;
        transition: all 0.15s ease !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. 기출 데이터베이스 로드
# -------------------------------------------------------------
DEFAULT_QUESTIONS = []

def load_database():
    if os.path.exists("questions_db.json"):
        try:
            with open("questions_db.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    if "source_file" not in item:
                        item["source_file"] = f"{item.get('year', '')}_{item.get('subject', '기출문제')}.pdf"
                return data
        except Exception:
            pass
    return DEFAULT_QUESTIONS

questions_pool = load_database()

# -------------------------------------------------------------
# 2. 유연한 단답형 정답 판별 함수
# -------------------------------------------------------------
def check_short_answer(user_input: str, target_answer: str) -> bool:
    if not user_input or not target_answer:
        return False
    def clean_text(text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[-_/,]", " ", text)
        text = re.sub(r"[^a-z0-9가-힣\s]", "", text)
        return " ".join(text.split())

    c_user = clean_text(user_input)
    c_target = clean_text(target_answer)
    if c_user == c_target:
        return True
    if c_user.replace(" ", "") == c_target.replace(" ", ""):
        return True
    return False

# -------------------------------------------------------------
# 3. 세션 상태 관리
# -------------------------------------------------------------
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0
if "answered_state" not in st.session_state:
    st.session_state.answered_state = False
if "user_selected_ans" not in st.session_state:
    st.session_state.user_selected_ans = ""
if "is_correct" not in st.session_state:
    st.session_state.is_correct = False
if "starred_ids" not in st.session_state:
    st.session_state.starred_ids = set()
if "wrong_ids" not in st.session_state:
    st.session_state.wrong_ids = set()
if "correct_ids" not in st.session_state:
    st.session_state.correct_ids = set()
if "streak" not in st.session_state:
    st.session_state.streak = 0

# 필터 및 풀이 풀 상태 관리
if "filter_source_file" not in st.session_state:
    st.session_state.filter_source_file = "전체 파일 보기"
if "study_mode" not in st.session_state:
    st.session_state.study_mode = "전체 기출"
if "active_custom_pool" not in st.session_state:
    st.session_state.active_custom_pool = None

def go_home():
    st.session_state.current_page = "home"
    st.session_state.answered_state = False
    st.session_state.user_selected_ans = ""

def go_selector():
    st.session_state.current_page = "selector"
    st.session_state.answered_state = False
    st.session_state.user_selected_ans = ""

def start_quiz(idx=0, custom_pool=None):
    st.session_state.current_idx = idx
    if custom_pool is not None:
        st.session_state.active_custom_pool = custom_pool
    st.session_state.current_page = "quiz"
    st.session_state.answered_state = False
    st.session_state.user_selected_ans = ""

# -------------------------------------------------------------
# 4. 상단 네비게이션 헤더 (모든 버튼 및 뱃지 크기 균형 맞춤)
# -------------------------------------------------------------
col_h1, col_h2, col_h3 = st.columns([3, 4, 5])
with col_h1:
    if st.button("⚡ Med-Lingo", key="global_home_btn", use_container_width=True):
        go_home()
        st.rerun()

with col_h2:
    if st.session_state.current_page != "home":
        if st.button("📂 기출/문제 선택창 이동", key="global_selector_btn", use_container_width=True):
            go_selector()
            st.rerun()

with col_h3:
    st.markdown(
        f"""
        <div style='text-align: right; display: flex; justify-content: flex-end; align-items: center; gap: 8px;'>
            <span style='background: #EEF2FF; color: #4338CA; padding: 7px 14px; border-radius: 12px; font-size: 16px; font-weight: 800; border: 1.5px solid #C7D2FE;'>🔥 {st.session_state.streak}연승</span>
            <span style='background: #FEF3C7; color: #B45309; padding: 7px 14px; border-radius: 12px; font-size: 16px; font-weight: 800; border: 1.5px solid #FDE68A;'>⭐ {len(st.session_state.starred_ids)}</span>
            <span style='background: #FEE2E2; color: #B91C1C; padding: 7px 14px; border-radius: 12px; font-size: 16px; font-weight: 800; border: 1.5px solid #FECACA;'>❌ {len(st.session_state.wrong_ids)}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<hr style='margin-top: 10px; margin-bottom: 22px; border-color: #E2E8F0;'>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 5. 화면 1: 홈 화면 (HOME)
# -------------------------------------------------------------
if st.session_state.current_page == "home":
    st.markdown("""
    <div class="hero-card">
        <div style="font-size: 52px; margin-bottom: 10px;">🩺</div>
        <div class="hero-title">Med-Lingo</div>
        <div class="hero-sub">
            Jokbo-Based Learning<br>
            의대 족보와 기출문제를 듀오링고처럼 가볍고 확실하게 정복하세요.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 상단 히어로 카드와 동일한 전체 너비 및 큼직한 높이의 CTA 버튼
    if st.button("🚀 Med-Lingo 기출 풀러가기", key="home_start_hero_btn", use_container_width=True):
        go_selector()
        st.rerun()
            
    st.write("")
    st.markdown("### 📊 나의 학습 진행 현황")
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{len(questions_pool)}</div>
            <div class="stat-label">총 기출 문항 수</div>
        </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number" style="color: #10B981;">{len(st.session_state.correct_ids)}</div>
            <div class="stat-label">정답 맞힌 문항</div>
        </div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number" style="color: #EF4444;">{len(st.session_state.wrong_ids)}</div>
            <div class="stat-label">누적 오답 문항</div>
        </div>
        """, unsafe_allow_html=True)
    with s4:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number" style="color: #F59E0B;">{len(st.session_state.starred_ids)}</div>
            <div class="stat-label">별표 체크 문항</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    st.markdown("### 💡 주요 기능 가이드")
    g1, g2, g3 = st.columns(3)
    with g1:
        st.markdown("**📁 기출문제 파일별 & 상세 필터**\n\n족보 PDF 파일별 혹은 과목/년도/교수님 조건별로 맞춤형 문항 세트를 구성하여 풀 수 있습니다.")
    with g2:
        st.markdown("**🎯 듀오링고식 풀이 & 하단 고정 버튼**\n\n객관식 카드 선지와 유연한 단답형 채점을 지원하며, 이전/다음 버튼이 화면 하단에 고정되어 편안하게 풀 수 있습니다.")
    with g3:
        st.markdown("**🔄 즉각적인 오답 노트 반영**\n\n풀이 결과에 따라 정답 및 오답이 실시간 집계되며, 표기 차이로 인한 억울한 오답은 '정답 인정' 버튼으로 구제할 수 있습니다.")

# -------------------------------------------------------------
# 6. 화면 2: 기출문제 선택 창 (SELECTOR)
# -------------------------------------------------------------
elif st.session_state.current_page == "selector":
    st.markdown("## 📂 기출문제 선택 & 필터")
    st.caption("풀고 싶은 기출문제 파일 또는 과목/년도/교수님 조건을 선택하세요.")
    
    tab_files, tab_custom = st.tabs(["📁 기출문제 파일별 선택", "🔍 과목/년도/교수님 상세 필터"])
    
    with tab_files:
        st.write("")
        all_files = sorted(list(set(q.get("source_file", "기타 기출.pdf") for q in questions_pool)))
        
        if not all_files:
            st.info("등록된 기출 데이터가 없습니다. questions_db.json 파일을 확인해주세요.")
        else:
            f_cols = st.columns([4, 8])
            with f_cols[0]:
                st.markdown("<p style='font-size: 16px; font-weight: 800; color: #1E293B; margin-bottom: 8px;'>📁 기출 파일 목록</p>", unsafe_allow_html=True)
                picked_file = st.radio("기출 파일 목록", all_files, label_visibility="collapsed")
            with f_cols[1]:
                file_qs = [q for q in questions_pool if q.get("source_file") == picked_file]
                st.markdown(f"#### 📄 {picked_file}")
                st.markdown(f"- **문항 수:** {len(file_qs)}문항")
                st.markdown(f"- **포함 교수님:** {', '.join(sorted(list(set(q['professor'] for q in file_qs))))}")
                if file_qs:
                    st.markdown(f"- **과목/년도:** {file_qs[0]['subject']} ({file_qs[0]['year']}년)")
                
                st.write("")
                btn_col1, btn_col2 = st.columns([5, 5])
                with btn_col1:
                    if st.button("🚀 이 파일 처음부터 풀기 (Q1)", type="primary", use_container_width=True):
                        st.session_state.filter_source_file = picked_file
                        st.session_state.study_mode = "파일별 풀기"
                        start_quiz(0, custom_pool=file_qs)
                        st.rerun()
                with btn_col2:
                    if st.button("📋 이 파일 문제 목록 펼치기", use_container_width=True):
                        st.session_state.filter_source_file = picked_file
                        st.session_state.study_mode = "파일별 풀기"
                        st.session_state.active_custom_pool = file_qs
                        st.rerun()

    with tab_custom:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            all_subs = ["전체 과목"] + sorted(list(set(q["subject"] for q in questions_pool)))
            sel_sub = st.selectbox("과목", all_subs)
        with c2:
            sub_qs = questions_pool if sel_sub == "전체 과목" else [q for q in questions_pool if q["subject"] == sel_sub]
            all_yrs = sorted(list(set(q["year"] for q in sub_qs)), reverse=True)
            sel_yrs = st.multiselect("년도", all_yrs, default=all_yrs)
        with c3:
            yr_qs = [q for q in sub_qs if q["year"] in sel_yrs]
            all_p = sorted(list(set(q["professor"] for q in yr_qs)))
            sel_p = st.multiselect("교수님", all_p, default=all_p)
        with c4:
            s_mode = st.selectbox("학습 모드", ["전체 기출", "⭐ 별표 문제만", "❌ 오답 문제만"])
            
        custom_matched = [
            q for q in questions_pool
            if (sel_sub == "전체 과목" or q["subject"] == sel_sub) and
               (q["year"] in sel_yrs) and
               (q["professor"] in sel_p)
        ]
        if s_mode == "⭐ 별표 문제만":
            custom_matched = [q for q in custom_matched if q["id"] in st.session_state.starred_ids]
        elif s_mode == "❌ 오답 문제만":
            custom_matched = [q for q in custom_matched if q["id"] in st.session_state.wrong_ids]
            
        st.write("")
        c_btn_c1, c_btn_c2 = st.columns([5, 5])
        with c_btn_c1:
            if st.button(f"🎯 조건 만족 문제 풀기 ({len(custom_matched)}문항)", type="primary", use_container_width=True):
                st.session_state.filter_source_file = "커스텀 필터"
                st.session_state.study_mode = s_mode
                start_quiz(0, custom_pool=custom_matched)
                st.rerun()
        with c_btn_c2:
            if st.button(f"📋 이 필터 문제 목록 펼치기 ({len(custom_matched)}문항)", use_container_width=True):
                st.session_state.filter_source_file = "커스텀 필터"
                st.session_state.study_mode = s_mode
                st.session_state.active_custom_pool = custom_matched
                st.rerun()

    # ---------------------------------------------------------
    # 문제 리스트 뷰어 (클릭한 문제부터 앞뒤로 연속 풀이 가능)
    # ---------------------------------------------------------
    st.write("")
    st.markdown("---")
    st.markdown("### 📑 문항 직접 선택 창")
    st.caption("원하는 문항 번호를 클릭하면 **해당 문제부터 이전/다음으로 이동하며 연속해서** 풀 수 있습니다.")
    
    if st.session_state.active_custom_pool is not None:
        display_qs = st.session_state.active_custom_pool
    elif st.session_state.filter_source_file != "커스텀 필터" and st.session_state.filter_source_file != "전체 파일 보기":
        display_qs = [q for q in questions_pool if q.get("source_file") == st.session_state.filter_source_file]
    else:
        display_qs = questions_pool

    if not display_qs:
        st.info("선택된 파일이나 조건에 해당하는 문제가 없습니다.")
    else:
        grid_cols = st.columns(5)
        for i, q in enumerate(display_qs):
            col_target = grid_cols[i % 5]
            q_id = q["id"]
            
            status_emoji = "⚪"
            if q_id in st.session_state.correct_ids:
                status_emoji = "🟢"
            elif q_id in st.session_state.wrong_ids:
                status_emoji = "🔴"
            if q_id in st.session_state.starred_ids:
                status_emoji += "⭐"
                
            btn_title = f"{status_emoji} Q{i+1}. {q['subject'][:4]} ({q['professor']})"
            if col_target.button(btn_title, key=f"jump_btn_{q_id}_{i}", use_container_width=True):
                start_quiz(i, custom_pool=display_qs)
                st.rerun()

# -------------------------------------------------------------
# 7. 화면 3: 문제 풀이 화면 (QUIZ & 플로팅 하단 고정 바)
# -------------------------------------------------------------
elif st.session_state.current_page == "quiz":
    if st.session_state.active_custom_pool is not None and len(st.session_state.active_custom_pool) > 0:
        current_active_pool = st.session_state.active_custom_pool
    elif st.session_state.filter_source_file not in ["전체 파일 보기", "커스텀 필터"]:
        current_active_pool = [q for q in questions_pool if q.get("source_file") == st.session_state.filter_source_file]
    else:
        current_active_pool = questions_pool

    if not current_active_pool:
        st.warning("풀이할 문항이 없습니다. 문제 선택창으로 돌아갑니다.")
        if st.button("문제 선택창으로 이동"):
            go_selector()
            st.rerun()
        st.stop()

    if st.session_state.current_idx >= len(current_active_pool):
        st.session_state.current_idx = 0

    current_q = current_active_pool[st.session_state.current_idx]
    q_id = current_q["id"]
    is_starred = q_id in st.session_state.starred_ids

    # 진행도 게이지
    p_val = (st.session_state.current_idx + 1) / len(current_active_pool)
    st.progress(p_val)

    # 상단 정보 및 대형 조작 버튼 (진행도 / 문제 목록 / 별표하기)
    sub_c1, sub_c2, sub_c3 = st.columns([5, 3.2, 2.8])
    with sub_c1:
        st.markdown(
            f"<div style='font-size: 18px; font-weight: 800; color: #1E293B; margin-top: 8px;'>"
            f"진행도 {st.session_state.current_idx + 1} / {len(current_active_pool)} "
            f"<span style='font-size: 14px; font-weight: 600; color: #64748B;'>| `{current_q.get('source_file', '기출문제')}`</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    with sub_c2:
        if st.button("📋 문제 목록으로 돌아가기", key="quiz_back_to_list", use_container_width=True):
            go_selector()
            st.rerun()
    with sub_c3:
        star_txt = "⭐ 별표됨" if is_starred else "☆ 별표하기"
        if st.button(star_txt, key=f"quiz_star_{q_id}", use_container_width=True):
            if is_starred:
                st.session_state.starred_ids.remove(q_id)
            else:
                st.session_state.starred_ids.add(q_id)
            st.rerun()

    # 문제 본문 카드
    st.markdown(f"""
    <div class="question-card">
        <span class="question-badge">{current_q['year']}년도 | {current_q['professor']} 교수님 | {current_q['subject']}</span>
        <div class="question-text">Q{st.session_state.current_idx + 1}. {current_q['question']}</div>
    </div>
    """, unsafe_allow_html=True)

    # 문항 이미지 렌더링
    img_data = current_q.get("image")
    if img_data:
        if isinstance(img_data, str) and (img_data.startswith("data:image") or img_data.startswith("http")):
            st.image(img_data, use_container_width=True)
        elif isinstance(img_data, str) and os.path.exists(img_data):
            st.image(img_data, use_container_width=True)

    # 답안 입력부
    user_answer_raw = ""
    if current_q["type"] == "single_choice":
        if not st.session_state.answered_state:
            user_choice = st.radio(
                "정답을 선택하세요:",
                current_q["choices"],
                index=None,
                key=f"radio_{q_id}_{st.session_state.current_idx}",
                label_visibility="collapsed"
            )
            if user_choice:
                user_answer_raw = user_choice.strip()[0]
        else:
            st.markdown("<p style='font-weight:800; color:#1E293B; margin-bottom:12px; font-size:16px;'>📋 전체 선지 및 정답 결과:</p>", unsafe_allow_html=True)
            target_ans = str(current_q["answer"]).strip()
            user_ans = str(st.session_state.user_selected_ans).strip()

            for choice_text in current_q["choices"]:
                c_num = choice_text.strip()[0]
                is_correct_choice = (c_num == target_ans or choice_text.strip().startswith(target_ans))
                is_user_choice = (c_num == user_ans or choice_text.strip().startswith(user_ans))

                if is_correct_choice:
                    st.markdown(f"""
                    <div class="choice-card-correct">
                        <div>{choice_text}</div>
                        <span style="background:#2563EB; color:white; font-size:13px; font-weight:700; padding:4px 12px; border-radius:8px; white-space:nowrap; margin-left:12px;">✅ 정답</span>
                    </div>
                    """, unsafe_allow_html=True)
                elif is_user_choice and not is_correct_choice:
                    st.markdown(f"""
                    <div class="choice-card-wrong">
                        <div>{choice_text}</div>
                        <span style="background:#EF4444; color:white; font-size:13px; font-weight:700; padding:4px 12px; border-radius:8px; white-space:nowrap; margin-left:12px;">❌ 내가 고른 오답</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="choice-card-dimmed">
                        <div>{choice_text}</div>
                    </div>
                    """, unsafe_allow_html=True)

    elif current_q["type"] == "short_answer":
        if not st.session_state.answered_state:
            user_text = st.text_input(
                "정답 입력 (단답형):",
                key=f"text_{q_id}_{st.session_state.current_idx}",
                placeholder="답안을 입력하세요..."
            )
            user_answer_raw = user_text.strip()
        else:
            st.markdown(f"**내가 제출한 답:** `{st.session_state.user_selected_ans}`")

    # 결과 피드백 바
    if st.session_state.answered_state:
        if st.session_state.is_correct:
            st.markdown(f"""
            <div class="feedback-correct">
                <h4 style="margin:0; font-size: 19px;">🎉 정답입니다! 계속 집중해 볼까요?</h4>
                <p style="margin: 6px 0 0 0; font-size: 15px;">정답: <b>{current_q['answer']}</b></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="feedback-wrong">
                <h4 style="margin:0; font-size: 19px;">❌ 오답 처리되었습니다.</h4>
                <p style="margin: 6px 0 0 0; font-size: 15px;">기준 정답: <b>{current_q['answer']}</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🙋 맞았는데 틀렸어요! (정답으로 인정)", key="override_btn", use_container_width=True):
                st.session_state.is_correct = True
                st.session_state.streak += 1
                st.session_state.correct_ids.add(q_id)
                if q_id in st.session_state.wrong_ids:
                    st.session_state.wrong_ids.remove(q_id)
                st.toast("정답으로 인정되어 오답노트에서 제외되었습니다!")
                st.rerun()

    # 하단 고정 바 아래 콘텐츠 공간 확보용 스페이서
    st.markdown('<div class="bottom-bar-spacer"></div>', unsafe_allow_html=True)

    # -------------------------------------------------------------
    # 8. [화면 하단 고정 플로팅 바] (문제 높이와 무관하게 항상 하단에 고정)
    # -------------------------------------------------------------
    is_last_question = (st.session_state.current_idx >= len(current_active_pool) - 1)

    bottom_bar_container = st.container()
    with bottom_bar_container:
        # CSS Anchor Div (이 태그가 있는 컨테이너를 CSS로 하단 고정)
        st.markdown('<div class="bottom-floating-anchor"></div>', unsafe_allow_html=True)

        if not st.session_state.answered_state:
            # 문제 풀기 전: [이전] / [그냥 다음(스킵)] / [정답 확인]
            btn_col1, btn_col2, btn_col3 = st.columns([3, 4, 4])
            with btn_col1:
                if st.button("⬅️ 이전", disabled=(st.session_state.current_idx == 0), use_container_width=True):
                    st.session_state.current_idx -= 1
                    st.session_state.answered_state = False
                    st.session_state.user_selected_ans = ""
                    st.rerun()
            with btn_col2:
                if st.button("➡️ 그냥 다음 (스킵)", disabled=is_last_question, use_container_width=True):
                    st.session_state.current_idx += 1
                    st.session_state.answered_state = False
                    st.session_state.user_selected_ans = ""
                    st.rerun()
            with btn_col3:
                check_btn = st.button("정답 확인 ✔️", type="primary", use_container_width=True)

            if check_btn:
                if not user_answer_raw:
                    st.warning("답안을 먼저 선택하거나 입력해 주세요!")
                else:
                    st.session_state.user_selected_ans = user_answer_raw
                    correct_ans = str(current_q["answer"]).strip()
                    
                    if current_q["type"] == "single_choice":
                        matched = (user_answer_raw == correct_ans)
                    else:
                        matched = check_short_answer(user_answer_raw, correct_ans)
                        
                    st.session_state.is_correct = matched
                    st.session_state.answered_state = True
                    
                    if matched:
                        st.session_state.streak += 1
                        st.session_state.correct_ids.add(q_id)
                        if q_id in st.session_state.wrong_ids:
                            st.session_state.wrong_ids.remove(q_id)
                    else:
                        st.session_state.streak = 0
                        st.session_state.wrong_ids.add(q_id)
                    st.rerun()

        else:
            # 정답 확인 후: [이전 문제] / [다음 문제 or 풀이 완료]
            btn_col1, btn_col2 = st.columns([4, 6])
            with btn_col1:
                if st.button("⬅️ 이전 문제", disabled=(st.session_state.current_idx == 0), use_container_width=True):
                    st.session_state.current_idx -= 1
                    st.session_state.answered_state = False
                    st.session_state.user_selected_ans = ""
                    st.rerun()
            with btn_col2:
                next_label = "풀이 완료 (선택창으로 이동)" if is_last_question else "다음 문제 ➡️"
                if st.button(next_label, type="primary", use_container_width=True):
                    if is_last_question:
                        go_selector()
                    else:
                        st.session_state.current_idx += 1
                        st.session_state.answered_state = False
                        st.session_state.user_selected_ans = ""
                    st.rerun()
