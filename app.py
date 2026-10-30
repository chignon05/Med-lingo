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

# Custom CSS for polished Duolingo / Modern Web App Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Top Navigation bar */
    .top-nav {
        background: white;
        padding: 12px 24px;
        border-radius: 16px;
        border: 2px solid #E2E8F0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03);
    }
    
    /* Home Hero Card */
    .hero-card {
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%);
        border-radius: 24px;
        padding: 40px 32px;
        color: white;
        text-align: center;
        margin-bottom: 28px;
        box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.4);
    }
    
    .hero-title {
        font-size: 36px;
        font-weight: 800;
        margin-bottom: 12px;
        letter-spacing: -0.5px;
    }
    
    .hero-sub {
        font-size: 17px;
        opacity: 0.95;
        max-width: 620px;
        margin: 0 auto 24px auto;
        line-height: 1.6;
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

    /* Question Card */
    .question-card {
        background: white;
        border: 2px solid #E2E8F0;
        border-radius: 20px;
        padding: 28px 24px 20px 24px;
        box-shadow: 0 6px 12px -2px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .question-badge {
        display: inline-block;
        background-color: #EEF2FF;
        color: #4338CA;
        font-size: 13px;
        font-weight: 700;
        padding: 5px 12px;
        border-radius: 10px;
        margin-bottom: 14px;
    }
    .question-text {
        font-size: 18px;
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
        margin-top: 16px;
        color: #065F46;
    }
    .feedback-wrong {
        background-color: #FEE2E2;
        border: 2px solid #EF4444;
        border-radius: 16px;
        padding: 18px 22px;
        margin-top: 16px;
        color: #991B1B;
    }
    .ai-box {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
        padding: 16px 20px;
        border-radius: 0 14px 14px 0;
        margin-top: 14px;
        font-size: 14px;
        color: #1E3A8A;
        line-height: 1.6;
    }
    
    /* Exam Source File Card */
    .exam-file-card {
        background: white;
        border: 2px solid #E2E8F0;
        border-radius: 16px;
        padding: 18px 22px;
        margin-bottom: 14px;
        transition: all 0.2s ease;
    }
    .exam-file-card:hover {
        border-color: #6366F1;
        box-shadow: 0 6px 16px -2px rgba(99, 102, 241, 0.15);
    }

    /* -------------------------------------------------------------
       선지 네모 박스 스타일링
       ------------------------------------------------------------- */
    /* Streamlit Radio 상단 제목 라벨 리셋 (네모 박스 해제, 굵은 텍스트) */
    div[data-testid="stRadio"] > label,
    div[data-testid="stRadio"] label[data-testid="stWidgetLabel"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 0 10px 0 !important;
        cursor: default !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        color: #1E293B !important;
    }
    div[data-testid="stRadio"] > label:hover,
    div[data-testid="stRadio"] label[data-testid="stWidgetLabel"]:hover {
        border: none !important;
        background: transparent !important;
    }

    /* Streamlit Radio 실제 선택 옵션 항목들만 카드형 네모 박스로 변경 */
    div[data-testid="stRadio"] div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 12px;
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
    
    /* 풀기 전 선택된 선지 (초록색 하이라이트) */
    div[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"],
    div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
        border-color: #10B981 !important;
        background-color: #ECFDF5 !important;
        color: #065F46 !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 10px rgba(16, 185, 129, 0.15) !important;
    }

    /* 정답 확인 후: 정답 선지 (파란색 박스 + 맞춤 표시) */
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
        animation: fadeIn 0.3s ease;
    }

    /* 정답 확인 후: 내가 선택한 오답 선지 (빨간색 박스 + 틀림 표시) */
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
        animation: fadeIn 0.3s ease;
    }

    /* 정답 확인 후: 선택하지 않은 다른 오답 선지 */
    .choice-card-dimmed {
        background-color: #F8FAFC !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 12px;
        color: #64748B;
        opacity: 0.85;
    }

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. 기본 기출 데이터셋 (파일별 출처 명시: source_file)
# -------------------------------------------------------------
DEFAULT_QUESTIONS = [
    {
        "id": "251020_bio_01",
        "source_file": "251020_예2_의학생화학_정답.pdf",
        "subject": "의학생화학",
        "year": 2025,
        "professor": "부용출",
        "type": "single_choice",
        "question": "Which of the following statements about insulin secretion and its physiological role or related diseases is NOT correct?",
        "choices": [
            "1) Insulin is secreted by pancreatic a-cells through exocytosis, triggered by increased intracellular calcium following glucose-stimulated opening of ATP-sensitive K channels.",
            "2) Insulin promotes glucose uptake into skeletal muscle and adipose tissue by stimulating the translocation of GLUT4 transporters to the plasma membrane.",
            "3) In type 1 diabetes mellitus, autoimmune destruction of pancreatic B-cells leads to absolute insulin deficiency.",
            "4) In type 2 diabetes mellitus, insulin resistance in peripheral tissues is the primary cause of hyperglycemia."
        ],
        "answer": "1",
        "ai_explanation": "인슐린은 췌장의 a-cell(알파세포)이 아니라 B-cell(베타세포)에서 분비됩니다. 또한 포도당 자극 시 ATP-sensitive K+ 채널은 닫히며(closure), 막 탈분극 후 전압개폐칼슘채널이 열려 칼슘 유입이 유도됩니다."
    },
    {
        "id": "251020_bio_03",
        "source_file": "251020_예2_의학생화학_정답.pdf",
        "subject": "의학생화학",
        "year": 2025,
        "professor": "부용출",
        "type": "single_choice",
        "question": "Which of the following monosaccharides is primarily metabolized in the liver through a pathway that bypasses the regulatory step catalyzed by phosphofructokinase-1 (PFK-1), thereby promoting unchecked glycolytic flux and contributing to increased lipogenesis and obesity?",
        "choices": [
            "1) Galactose",
            "2) Fructose",
            "3) Glucose",
            "4) Mannose"
        ],
        "answer": "2",
        "ai_explanation": "과당(Fructose)은 간에서 Fructokinase에 의해 Fructose-1-P가 된 뒤 Aldolase B로 분해되어 당분해과정의 핵심 관문인 PFK-1을 우회합니다."
    },
    {
        "id": "251020_bio_16",
        "source_file": "251020_예2_의학생화학_정답.pdf",
        "subject": "의학생화학",
        "year": 2025,
        "professor": "권태환",
        "type": "single_choice",
        "question": "Which of the following amino acids is classified as essential in humans and must be obtained from the diet?",
        "choices": [
            "1) Alanine",
            "2) Glutamate",
            "3) Leucine",
            "4) Proline"
        ],
        "answer": "3",
        "ai_explanation": "필수 아미노산(Essential amino acids)에는 BCAA(Leucine, Isoleucine, Valine)와 Lysine, Methionine, Phenylalanine, Threonine, Tryptophan, Histidine 등이 해당합니다."
    },
    {
        "id": "251020_bio_28",
        "source_file": "251020_예2_의학생화학_정답.pdf",
        "subject": "의학생화학",
        "year": 2025,
        "professor": "권태환",
        "type": "single_choice",
        "question": "Carbamoyl phosphate synthetase I (CPS-I) is allosterically activated by:",
        "choices": [
            "1) Arginine",
            "2) N-acetylglutamate",
            "3) Ornithine",
            "4) Citrulline"
        ],
        "answer": "2",
        "ai_explanation": "미토콘드리아 내 요소회로 속도조절 효소인 CPS-I은 N-acetylglutamate(NAG)에 의해 allosteric 활성화됩니다."
    },
    {
        "id": "251020_bio_33",
        "source_file": "251020_예2_의학생화학_정답.pdf",
        "subject": "의학생화학",
        "year": 2025,
        "professor": "이재만",
        "type": "single_choice",
        "question": "Which of the following glycogen storage diseases of humans is caused by defective lysosomal glucosidase (acid a-glucosidase)?",
        "choices": [
            "1) Cori disease (Type III)",
            "2) Hers disease (Type VI)",
            "3) Pompe disease (Type II)",
            "4) Andersen disease (Type IV)",
            "5) Von Gierke disease (Type I)"
        ],
        "answer": "3",
        "ai_explanation": "리소좀 내부의 acid a-glucosidase 결핍으로 글리코겐이 축적되는 질환은 Pompe disease(Type II)입니다."
    },
    {
        "id": "251020_bio_45",
        "source_file": "251020_예2_의학생화학_정답.pdf",
        "subject": "의학생화학",
        "year": 2025,
        "professor": "이병헌",
        "type": "single_choice",
        "question": "지방산 베타 산화과정의 4단계 효소 반응 순서로 옳은 것은?\n1: 산화(FAD) -> 2: 수화 -> 3: 산화(NAD+) -> 4: 티올분해(Thiolysis)",
        "choices": [
            "1) enoyl-CoA hydratase -> beta-hydroxyacyl-CoA dehydrogenase -> acyl-CoA acetyltransferase -> acyl-CoA dehydrogenase",
            "2) beta-hydroxyacyl-CoA dehydrogenase -> acyl-CoA acetyltransferase -> acyl-CoA dehydrogenase -> enoyl-CoA hydratase",
            "3) acyl-CoA acetyltransferase -> acyl-CoA dehydrogenase -> enoyl-CoA hydratase -> beta-hydroxyacyl-CoA dehydrogenase",
            "4) acyl-CoA dehydrogenase -> enoyl-CoA hydratase -> beta-hydroxyacyl-CoA dehydrogenase -> acyl-CoA acetyltransferase",
            "5) beta-hydroxyacyl-CoA dehydrogenase -> enoyl-CoA hydratase -> acyl-CoA dehydrogenase -> acyl-CoA acetyltransferase"
        ],
        "answer": "4",
        "ai_explanation": "베타 산화 반응 순서: Acyl-CoA dehydrogenase -> Enoyl-CoA hydratase -> Beta-hydroxyacyl-CoA dehydrogenase -> Thiolase (acyl-CoA acetyltransferase) 입니다."
    },
    {
        "id": "251021_lab_09",
        "source_file": "251021_예2_의생명과학실험_정답.pdf",
        "subject": "의생명과학실험",
        "year": 2025,
        "professor": "남성욱",
        "type": "short_answer",
        "question": "BCA assay에서 BCA는 무엇의 약자인가? Full name을 영어로 적으시오.",
        "choices": [],
        "answer": "Bicinchoninic acid",
        "ai_explanation": "Bicinchoninic acid assay의 약어로, 1가 구리 이온과 BCA 분자간 착체 형성을 통해 562 nm에서 자색 흡광도를 측정합니다."
    },
    {
        "id": "251021_lab_13",
        "source_file": "251021_예2_의생명과학실험_정답.pdf",
        "subject": "의생명과학실험",
        "year": 2025,
        "professor": "남성욱",
        "type": "short_answer",
        "question": "ELISA는 무엇의 약자인가? Full name을 영어로 적으시오.",
        "choices": [],
        "answer": "Enzyme-linked immunosorbent assay",
        "ai_explanation": "ELISA는 항체나 항원에 결합된 효소의 기질 반응을 통해 항원-항체 반응을 정량하는 Enzyme-linked immunosorbent assay입니다."
    },
    {
        "id": "251022_anat_01",
        "source_file": "251022_예2_인체_해부학_정답.pdf",
        "subject": "인체해부학",
        "year": 2025,
        "professor": "박재찬",
        "type": "short_answer",
        "question": "위턱뼈 앞면에 위치하며 Maxillary nerve(V2)의 종말 가지가 안면부로 빠져나오는 구멍의 이름은?\n--- () foramen",
        "choices": [],
        "answer": "infraorbital",
        "ai_explanation": "Maxillary nerve(삼차신경 제2지)의 연속인 infraorbital nerve와 동정맥이 infraorbital foramen(눈확아래구멍)을 통과합니다."
    },
    {
        "id": "221024_bio_02",
        "source_file": "22중간.pdf",
        "subject": "의학생화학",
        "year": 2022,
        "professor": "부용출",
        "type": "single_choice",
        "question": "Choose the one that is NOT correct regarding the citric acid cycle.",
        "choices": [
            "1) Citrate is isomerized to isocitrate by aconitase in two steps: hydration to cis-aconitate and dehydration to isocitrate.",
            "2) Isocitrate undergoes dehydrogenation catalyzed by isocitrate dehydrogenase to form oxalosuccinate, which decarboxylates to a-ketoglutarate.",
            "3) a-Ketoglutarate undergoes oxidative decarboxylation catalyzed by a-ketoglutarate dehydrogenase complex to form succinyl-CoA and CO2.",
            "4) Succinyl-CoA is converted to succinate by succinate thiokinase, which is the only substrate-level phosphorylation in the cycle.",
            "5) Succinate dehydrogenase is bound to the inner surface of the inner mitochondrial membrane."
        ],
        "answer": "1",
        "ai_explanation": "Aconitase에 의한 반응은 탈수(dehydration)로 cis-aconitate를 먼저 만든 후 재수화(hydration)되어 isocitrate가 되므로 설명이 반대입니다."
    }
]

def load_database():
    if os.path.exists("questions_db.json"):
        try:
            with open("questions_db.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                # Ensure source_file key exists
                for item in data:
                    if "source_file" not in item:
                        item["source_file"] = f"{item.get('year', '')}_{item.get('subject', '기출문제')}.pdf"
                return data
        except Exception:
            pass
    return DEFAULT_QUESTIONS

questions_pool = load_database()

# -------------------------------------------------------------
# 2. 유연한 단답형 정답 판별 함수 (Fuzzy Normalization)
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
# 화면 라우트: 'home' | 'selector' | 'quiz'
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
if "show_ai" not in st.session_state:
    st.session_state.show_ai = False

# 필터 상태
if "filter_source_file" not in st.session_state:
    st.session_state.filter_source_file = "전체 파일 보기"
if "filter_subject" not in st.session_state:
    st.session_state.filter_subject = "전체 과목"
if "filter_years" not in st.session_state:
    st.session_state.filter_years = []
if "filter_profs" not in st.session_state:
    st.session_state.filter_profs = []
if "study_mode" not in st.session_state:
    st.session_state.study_mode = "전체 기출"

def go_home():
    st.session_state.current_page = "home"
    st.session_state.answered_state = False
    st.session_state.show_ai = False

def go_selector():
    st.session_state.current_page = "selector"
    st.session_state.answered_state = False
    st.session_state.show_ai = False

def start_quiz(idx=0):
    st.session_state.current_idx = idx
    st.session_state.current_page = "quiz"
    st.session_state.answered_state = False
    st.session_state.show_ai = False
    st.session_state.user_selected_ans = ""

# -------------------------------------------------------------
# 4. 상단 네비게이션 헤더 (어디서나 Med-Lingo를 눌러 홈으로 이동)
# -------------------------------------------------------------
col_h1, col_h2, col_h3 = st.columns([4, 4, 4])
with col_h1:
    if st.button("⚡ Med-Lingo (홈으로)", key="global_home_btn", use_container_width=False):
        go_home()
        st.rerun()

with col_h2:
    if st.session_state.current_page != "home":
        if st.button("📂 기출/문제 선택창 이동", key="global_selector_btn"):
            go_selector()
            st.rerun()

with col_h3:
    st.markdown(
        f"<div style='text-align: right; padding-top: 6px; font-weight:700; color:#4F46E5;'>"
        f"🔥 {st.session_state.streak}연승 | ⭐ {len(st.session_state.starred_ids)} | ❌ {len(st.session_state.wrong_ids)}"
        f"</div>",
        unsafe_allow_html=True
    )

st.markdown("<hr style='margin-top: 8px; margin-bottom: 20px; border-color: #E2E8F0;'>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 5. 화면 1: 홈 화면 (HOME)
# -------------------------------------------------------------
if st.session_state.current_page == "home":
    st.markdown("""
    <div class="hero-card">
        <div style="font-size: 48px; margin-bottom: 8px;">🩺</div>
        <div class="hero-title">Med-Lingo 기출 마스터</div>
        <div class="hero-sub">
            방대한 의대 족보와 기출문제를 듀오링고처럼 가볍고 확실하게 정복하세요.<br>
            파일별, 교수님별, 년도별로 큐레이션된 문항을 풀고 AI 핵심 기전으로 단권화하세요.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 빅 메인 액션 버튼
    c_btn1, c_btn2, c_btn3 = st.columns([3, 4, 3])
    with c_btn2:
        if st.button("🚀 Med-Lingo 기출 풀러가기", type="primary", use_container_width=True):
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
        st.markdown("**📁 기출문제 파일별 풀이**\n\n'251020 의학생화학', '인체해부학', '22중간' 등 족보 PDF 파일 단위로 선택하여 풀 수 있습니다.")
    with g2:
        st.markdown("**🎯 듀오링고식 1문항 루프**\n\n한 문제씩 답안을 제출하고 피드백을 확인한 후 다음 문제로 넘어가는 몰입형 학습 환경을 제공합니다.")
    with g3:
        st.markdown("**🤖 AI 핵심 기전 & 구제 버튼**\n\n풀이 후 즉시 1-2줄 핵심 기전을 확인하고, 표기 차이로 인한 억울한 오답은 '맞았다' 버튼으로 즉시 인정할 수 있습니다.")

# -------------------------------------------------------------
# 6. 화면 2: 기출문제 선택 창 (SELECTOR)
# -------------------------------------------------------------
elif st.session_state.current_page == "selector":
    st.markdown("## 📂 기출문제 선택 & 필터")
    st.caption("풀고 싶은 기출문제 파일 또는 과목/년도/교수님 조건을 선택하세요.")
    
    # 탭 구성: [기출문제 파일별로 선택] vs [조건별 상세 필터]
    tab_files, tab_custom = st.tabs(["📁 기출문제 파일별 선택", "🔍 과목/년도/교수님 상세 필터"])
    
    selected_subset = []
    
    with tab_files:
        st.write("")
        all_files = sorted(list(set(q.get("source_file", "기타 기출.pdf") for q in questions_pool)))
        
        f_cols = st.columns([4, 8])
        with f_cols[0]:
            st.markdown("<p style='font-size: 16px; font-weight: 800; color: #1E293B; margin-bottom: 8px;'>📁 기출 파일 목록</p>", unsafe_allow_html=True)
            picked_file = st.radio("기출 파일 목록", all_files, label_visibility="collapsed")
        with f_cols[1]:
            file_qs = [q for q in questions_pool if q.get("source_file") == picked_file]
            st.markdown(f"#### 📄 {picked_file}")
            st.markdown(f"- **문항 수:** {len(file_qs)}문항")
            st.markdown(f"- **포함 교수님:** {', '.join(sorted(list(set(q['professor'] for q in file_qs))))}")
            st.markdown(f"- **과목/년도:** {file_qs[0]['subject']} ({file_qs[0]['year']}년)")
            
            st.write("")
            btn_col1, btn_col2 = st.columns([5, 5])
            with btn_col1:
                if st.button("🚀 이 파일 처음부터 풀기 (Q1)", type="primary", use_container_width=True):
                    st.session_state.filter_source_file = picked_file
                    st.session_state.study_mode = "파일별 풀기"
                    start_quiz(0)
                    st.rerun()
            with btn_col2:
                if st.button("📋 이 파일 문제 목록 펼치기", use_container_width=True):
                    st.session_state.filter_source_file = picked_file
                    st.session_state.study_mode = "파일별 풀기"
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
        if st.button(f"🎯 조건 만족 문제 풀기 ({len(custom_matched)}문항)", type="primary"):
            st.session_state.filter_source_file = "커스텀 필터"
            st.session_state.study_mode = s_mode
            st.session_state.custom_list = [q["id"] for q in custom_matched]
            start_quiz(0)
            st.rerun()

    # ---------------------------------------------------------
    # 문제 리스트 뷰어 (문항 번호 직접 클릭하여 바로 진입)
    # ---------------------------------------------------------
    st.write("")
    st.markdown("---")
    st.markdown("### 📑 문항 직접 선택 창")
    st.caption("원하는 문항 번호를 클릭하면 해당 문제로 즉시 이동합니다.")
    
    # 현재 선택된 소스에 따른 문항 목록
    if st.session_state.filter_source_file != "커스텀 필터" and st.session_state.filter_source_file != "전체 파일 보기":
        display_qs = [q for q in questions_pool if q.get("source_file") == st.session_state.filter_source_file]
    else:
        display_qs = questions_pool

    if not display_qs:
        st.info("선택된 파일이나 조건에 해당하는 문제가 없습니다.")
    else:
        # 그리드 형태로 문항 버튼 배치 (한 줄에 5개씩)
        grid_cols = st.columns(5)
        for i, q in enumerate(display_qs):
            col_target = grid_cols[i % 5]
            q_id = q["id"]
            
            # 문항 상태 태그
            status_emoji = "⚪"
            if q_id in st.session_state.correct_ids:
                status_emoji = "🟢"
            elif q_id in st.session_state.wrong_ids:
                status_emoji = "🔴"
            if q_id in st.session_state.starred_ids:
                status_emoji += "⭐"
                
            btn_title = f"{status_emoji} Q{i+1}. {q['subject'][:4]} ({q['professor']})"
            if col_target.button(btn_title, key=f"jump_btn_{q_id}", use_container_width=True):
                st.session_state.target_pool_file = q.get("source_file")
                start_quiz(i)
                st.rerun()

# -------------------------------------------------------------
# 7. 화면 3: 문제 풀이 화면 (QUIZ)
# -------------------------------------------------------------
elif st.session_state.current_page == "quiz":
    # 풀이 대상 문제군 확정
    if st.session_state.filter_source_file not in ["전체 파일 보기", "커스텀 필터"]:
        current_active_pool = [q for q in questions_pool if q.get("source_file") == st.session_state.filter_source_file]
    elif st.session_state.study_mode == "⭐ 별표 문제만":
        current_active_pool = [q for q in questions_pool if q["id"] in st.session_state.starred_ids]
    elif st.session_state.study_mode == "❌ 오답 문제만":
        current_active_pool = [q for q in questions_pool if q["id"] in st.session_state.wrong_ids]
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

    # 진행률 및 네비게이션 서브 헤더
    p_val = (st.session_state.current_idx + 1) / len(current_active_pool)
    st.progress(p_val)

    sub_c1, sub_c2, sub_c3 = st.columns([5, 3, 2])
    with sub_c1:
        st.markdown(f"**진행도 {st.session_state.current_idx + 1} / {len(current_active_pool)}** | 출처: `{current_q.get('source_file', '기출문제')}`")
    with sub_c2:
        if st.button("📋 문제 목록으로 돌아가기"):
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

    # 문항 이미지 렌더링 지원 (로컬 경로 / Base64 / 웹 URL 모두 자동 감지)
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
            # 풀기 전: 네모 박스 형태의 선택지 (클릭 시 초록색 하이라이트)
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
            # 정답 확인 후: 전체 선지를 네모 박스로 유지하고 정답(파란색) / 오답(빨간색) 시각화
            st.markdown("<p style='font-weight:700; color:#334155; margin-bottom:12px; font-size:15px;'>📋 전체 선지 및 정답 결과:</p>", unsafe_allow_html=True)
            target_ans = str(current_q["answer"]).strip()
            user_ans = str(st.session_state.user_selected_ans).strip()

            for choice_text in current_q["choices"]:
                c_num = choice_text.strip()[0]
                is_correct_choice = (c_num == target_ans or choice_text.strip().startswith(target_ans))
                is_user_choice = (c_num == user_ans or choice_text.strip().startswith(user_ans))

                if is_correct_choice:
                    # 정답 선지: 파란색 테두리/배경 + 파란색 정답 뱃지
                    st.markdown(f"""
                    <div class="choice-card-correct">
                        <div>{choice_text}</div>
                        <span style="background:#2563EB; color:white; font-size:12px; font-weight:700; padding:4px 10px; border-radius:8px; white-space:nowrap; margin-left:12px;">✅ 정답</span>
                    </div>
                    """, unsafe_allow_html=True)
                elif is_user_choice and not is_correct_choice:
                    # 내가 고른 오답 선지: 빨간색 테두리/배경 + 빨간색 오답 뱃지
                    st.markdown(f"""
                    <div class="choice-card-wrong">
                        <div>{choice_text}</div>
                        <span style="background:#EF4444; color:white; font-size:12px; font-weight:700; padding:4px 10px; border-radius:8px; white-space:nowrap; margin-left:12px;">❌ 내가 고른 오답</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # 나머지 일반 선지
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

    # 액션 버튼 영역
    st.write("")
    if not st.session_state.answered_state:
        # 풀기 전: 이전 문제 / 스킵(모르겠어요) / 정답 확인하기
        nav_col1, nav_col2, nav_col3 = st.columns([3, 3.5, 3.5])
        with nav_col1:
            if st.button("⬅️ 이전 문제", disabled=(st.session_state.current_idx == 0), use_container_width=True):
                st.session_state.current_idx -= 1
                st.session_state.answered_state = False
                st.session_state.is_skipped = False
                st.session_state.show_ai = False
                st.session_state.is_skipped = False
                st.session_state.user_selected_ans = ""
                st.rerun()
                
        with nav_col2:
            if st.button("⏭️ 잘 모르겠어요 (스킵)", use_container_width=True):
                st.session_state.answered_state = True
                st.session_state.is_skipped = True
                st.session_state.is_correct = False
                st.session_state.user_selected_ans = "건너뜀 (모름)"
                st.session_state.streak = 0
                st.session_state.wrong_ids.add(q_id)
                st.session_state.show_ai = True  # 스킵 시 바로 기전 해설 자동 개방
                st.rerun()
                
        with nav_col3:
            check_btn = st.button("정답 확인하기 ✔️", use_container_width=True, type="primary")

        if check_btn:
            if not user_answer_raw:
                st.warning("답안을 먼저 선택하거나 입력해 주세요! (모를 때는 스킵 버튼을 누르세요)")
            else:
                st.session_state.user_selected_ans = user_answer_raw
                st.session_state.is_skipped = False
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
        # 푼 후: 피드백, 정답 인정, AI 해설, 다음 문제
        is_skipped_mode = getattr(st.session_state, "is_skipped", False)
        
        if is_skipped_mode:
            st.markdown(f"""
            <div style="background-color: #FEF3C7; border: 2px solid #F59E0B; border-radius: 16px; padding: 18px 22px; margin-top: 16px; color: #92400E;">
                <h4 style="margin:0; font-size: 18px;">⏭️ 건너뛴 문제입니다.</h4>
                <p style="margin: 4px 0 0 0; font-size: 14px;">정답: <b>{current_q['answer']}</b> (복습을 위해 오답노트에 자동 저장되었습니다)</p>
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.is_correct:
            st.markdown(f"""
            <div class="feedback-correct">
                <h4 style="margin:0; font-size: 18px;">🎉 정답입니다! 계속 집중해 볼까요?</h4>
                <p style="margin: 4px 0 0 0; font-size: 14px;">정답: <b>{current_q['answer']}</b></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="feedback-wrong">
                <h4 style="margin:0; font-size: 18px;">❌ 오답 처리되었습니다.</h4>
                <p style="margin: 4px 0 0 0; font-size: 14px;">기준 정답: <b>{current_q['answer']}</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🙋 맞았는데 틀렸어요! (정답으로 인정)", key="override_btn"):
                st.session_state.is_correct = True
                st.session_state.streak += 1
                st.session_state.correct_ids.add(q_id)
                if q_id in st.session_state.wrong_ids:
                    st.session_state.wrong_ids.remove(q_id)
                st.toast("정답으로 인정되어 오답노트에서 제외되었습니다!")
                st.rerun()

        st.write("")
        b_c1, b_c2, b_c3 = st.columns([3, 4, 3])
        with b_c1:
            if st.button("⬅️ 이전 문제", disabled=(st.session_state.current_idx == 0), use_container_width=True):
                st.session_state.current_idx -= 1
                st.session_state.answered_state = False
                st.session_state.show_ai = False
                st.session_state.is_skipped = False
                st.session_state.user_selected_ans = ""
                st.rerun()
        with b_c2:
            if st.button("🤖 AI 핵심 기전 해설", key="quiz_ai_btn", use_container_width=True):
                st.session_state.show_ai = not st.session_state.show_ai
        with b_c3:
            if st.button("다음 문제 ➡️", type="primary", use_container_width=True):
                st.session_state.current_idx += 1
                st.session_state.answered_state = False
                st.session_state.show_ai = False
                st.session_state.is_skipped = False
                st.session_state.user_selected_ans = ""
                st.rerun()

        if st.session_state.show_ai:
            st.markdown(f"""
            <div class="ai-box">
                <b>🩺 AI Medical Assistant 기전 요약:</b><br>
                {current_q['ai_explanation']}
            </div>
            """, unsafe_allow_html=True)
