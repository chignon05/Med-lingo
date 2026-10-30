import streamlit as st
import json
import os

# Page Configuration
st.set_page_config(
    page_title="MedLingo - 의대 기출 퀘스트",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for Duolingo-like UX
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
    /* Main container styling */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Top status bar */
    .status-card {
        background: white;
        padding: 14px 20px;
        border-radius: 16px;
        border: 2px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    
    /* Duolingo style Question Card */
    .question-card {
        background: white;
        border: 2px solid #E2E8F0;
        border-radius: 20px;
        padding: 24px 24px 20px 24px;
        box-shadow: 0 6px 12px -2px rgba(0,0,0,0.06);
        margin-bottom: 24px;
        position: relative;
    }
    
    .question-badge {
        display: inline-block;
        background-color: #E0E7FF;
        color: #4338CA;
        font-size: 13px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 8px;
        margin-bottom: 12px;
    }

    .question-text {
        font-size: 18px;
        font-weight: 700;
        color: #1E293B;
        line-height: 1.6;
        margin-bottom: 8px;
    }
    
    /* Bottom feedback bar */
    .feedback-correct {
        background-color: #D1FAE5;
        border: 2px solid #10B981;
        border-radius: 16px;
        padding: 16px 20px;
        margin-top: 16px;
        color: #065F46;
        animation: fadeIn 0.3s ease;
    }
    
    .feedback-wrong {
        background-color: #FEE2E2;
        border: 2px solid #EF4444;
        border-radius: 16px;
        padding: 16px 20px;
        margin-top: 16px;
        color: #991B1B;
        animation: fadeIn 0.3s ease;
    }
    
    .ai-box {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
        padding: 14px 16px;
        border-radius: 0 12px 12px 0;
        margin-top: 12px;
        font-size: 14px;
        color: #1E3A8A;
        line-height: 1.5;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. 기출 데이터베이스 (첨부 PDF 기반 실제 기출 문항 포함)
# -------------------------------------------------------------
DEFAULT_QUESTIONS = [
    {
        "id": "251020_bio_01",
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
        "ai_explanation": "인슐린(Insulin)은 췌장의 a-cell(알파세포)이 아니라 B-cell(베타세포)에서 분비됩니다. 또한 포도당 자극 시 ATP-sensitive K+ 채널은 '닫히며(closure)', 탈분극 후 칼슘 유입이 유도됩니다."
    },
    {
        "id": "251020_bio_03",
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
        "ai_explanation": "과당(Fructose)은 간에서 Fructokinase에 의해 인산화된 후 Aldolase B를 거쳐 DHAP와 Glyceraldehyde로 전환되므로, 당분해과정의 핵심 속도조절 단계인 PFK-1 단계를 우회합니다."
    },
    {
        "id": "251020_bio_16",
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
        "ai_explanation": "필수 아미노산(Essential amino acids)에는 Leucine, Isoleucine, Valine(BCAA)과 Lysine, Methionine, Phenylalanine, Threonine, Tryptophan, Histidine 등이 포함됩니다."
    },
    {
        "id": "251020_bio_28",
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
        "ai_explanation": "요소회로(Urea cycle)의 속도조절 효소인 CPS-I은 N-acetylglutamate(NAG)에 의해 필수적으로 allosteric 활성화됩니다."
    },
    {
        "id": "251020_bio_33",
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
        "ai_explanation": "리소좀 내부의 acid a-glucosidase(a-1,4-glucosidase) 결핍으로 발생하는 당원축적병은 폼페병(Pompe disease, Type II)입니다."
    },
    {
        "id": "251020_bio_45",
        "subject": "의학생화학",
        "year": 2025,
        "professor": "이병헌",
        "type": "single_choice",
        "question": "지방산 산화과정(Beta-oxidation)의 4단계 효소 반응 순서로 옳은 것은?\n1: 산화(FAD) -> 2: 수화 -> 3: 산화(NAD+) -> 4: 티올분해(Thiolysis)",
        "choices": [
            "1) enoyl-CoA hydratase -> beta-hydroxyacyl-CoA dehydrogenase -> acyl-CoA acetyltransferase -> acyl-CoA dehydrogenase",
            "2) beta-hydroxyacyl-CoA dehydrogenase -> acyl-CoA acetyltransferase -> acyl-CoA dehydrogenase -> enoyl-CoA hydratase",
            "3) acyl-CoA acetyltransferase -> acyl-CoA dehydrogenase -> enoyl-CoA hydratase -> beta-hydroxyacyl-CoA dehydrogenase",
            "4) acyl-CoA dehydrogenase -> enoyl-CoA hydratase -> beta-hydroxyacyl-CoA dehydrogenase -> acyl-CoA acetyltransferase",
            "5) beta-hydroxyacyl-CoA dehydrogenase -> enoyl-CoA hydratase -> acyl-CoA dehydrogenase -> acyl-CoA acetyltransferase"
        ],
        "answer": "4",
        "ai_explanation": "베타 산화 순서: 1) Acyl-CoA dehydrogenase -> 2) Enoyl-CoA hydratase -> 3) Beta-hydroxyacyl-CoA dehydrogenase -> 4) Thiolase (acyl-CoA acetyltransferase) 순서(d-a-b-c)입니다."
    },
    {
        "id": "251021_lab_09",
        "subject": "의생명과학실험",
        "year": 2025,
        "professor": "남성욱",
        "type": "short_answer",
        "question": "BCA assay에서 BCA는 무엇의 약자인가? Full name을 영어로 적으시오.",
        "choices": [],
        "answer": "Bicinchoninic acid",
        "ai_explanation": "BCA assay는 Bicinchoninic acid assay의 약어로, 알칼리 조건에서 Cu2+가 Cu1+로 환원된 후 2분자의 BCA와 결합하여 자색(Purple, 562 nm) 착염을 형성하는 원리입니다."
    },
    {
        "id": "251021_lab_13",
        "subject": "의생명과학실험",
        "year": 2025,
        "professor": "남성욱",
        "type": "short_answer",
        "question": "ELISA는 무엇의 약자인가? Full name을 영어로 적으시오.",
        "choices": [],
        "answer": "Enzyme-linked immunosorbent assay",
        "ai_explanation": "ELISA는 Enzyme-linked immunosorbent assay(효소면역측정법)의 약어입니다."
    },
    {
        "id": "251022_anat_01",
        "subject": "인체해부학",
        "year": 2025,
        "professor": "박재찬",
        "type": "short_answer",
        "question": "위턱뼈(Maxilla) 앞면에 위치하며 Maxillary nerve(V2)의 종말 가지가 안면부로 빠져나오는 구멍의 이름은?\n--- () foramen",
        "choices": [],
        "answer": "infraorbital",
        "ai_explanation": "Maxillary nerve(삼차신경 제2가지)의 주행 가지인 infraorbital nerve와 혈관이 통과하는 구멍은 infraorbital foramen(눈확아래구멍)입니다."
    },
    {
        "id": "221024_bio_02",
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
        "ai_explanation": "Aconitase에 의한 반응은 탈수(dehydration)로 cis-aconitate를 먼저 만든 뒤 다시 수화(hydration)되어 isocitrate가 됩니다. 순서가 반대로 기술되어 오답입니다."
    }
]

def load_database():
    if os.path.exists("questions_db.json"):
        try:
            with open("questions_db.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return DEFAULT_QUESTIONS

questions_pool = load_database()

# -------------------------------------------------------------
# 2. 세션 상태 관리 (Session State)
# -------------------------------------------------------------
if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0
if "answered_state" not in st.session_state:
    st.session_state.answered_state = False  # 문제 제출 여부
if "user_selected_ans" not in st.session_state:
    st.session_state.user_selected_ans = ""
if "is_correct" not in st.session_state:
    st.session_state.is_correct = False
if "starred_ids" not in st.session_state:
    st.session_state.starred_ids = set()    # 별표(즐겨찾기/모르겠는 문제)
if "wrong_ids" not in st.session_state:
    st.session_state.wrong_ids = set()      # 틀린 문제 누적
if "streak" not in st.session_state:
    st.session_state.streak = 0             # 연속 정답 스트릭
if "show_ai" not in st.session_state:
    st.session_state.show_ai = False

# -------------------------------------------------------------
# 3. 사이드바: 모드 및 필터
# -------------------------------------------------------------
with st.sidebar:
    st.title("⚡ MedLingo")
    st.caption("의대생을 위한 인터랙티브 기출 퀘스트")
    
    # 모드 선택
    mode = st.radio(
        "학습 모드",
        ["🎯 전체 기출 풀기", "⭐ 별표 문제 복습", "❌ 오답 집중 복습"],
        index=0
    )
    
    st.markdown("---")
    
    # 1) 과목 선택
    all_subjects = sorted(list(set(q["subject"] for q in questions_pool)))
    selected_subject = st.selectbox("📚 과목 선택", all_subjects)
    
    # 2) 년도 선택
    subject_matched = [q for q in questions_pool if q["subject"] == selected_subject]
    available_years = sorted(list(set(q["year"] for q in subject_matched)), reverse=True)
    selected_years = st.multiselect("📅 년도 선택", available_years, default=available_years)
    
    # 3) 교수님 선택
    year_matched = [q for q in subject_matched if q["year"] in selected_years]
    available_profs = sorted(list(set(q["professor"] for q in year_matched)))
    selected_profs = st.multiselect("👨‍🏫 교수님 선택", available_profs, default=available_profs)
    
    st.markdown("---")
    # 학습 현황 미니 통계
    st.markdown(f"🔥 **현재 연속 정답:** {st.session_state.streak}콤보")
    st.markdown(f"⭐ **별표 표시된 문제:** {len(st.session_state.starred_ids)}개")
    st.markdown(f"❌ **누적 오답:** {len(st.session_state.wrong_ids)}개")

# -------------------------------------------------------------
# 4. 필터링된 문항 리스트 추출
# -------------------------------------------------------------
base_filtered = [
    q for q in questions_pool
    if q["subject"] == selected_subject and q["year"] in selected_years and q["professor"] in selected_profs
]

if mode == "⭐ 별표 문제 복습":
    active_questions = [q for q in base_filtered if q["id"] in st.session_state.starred_ids]
elif mode == "❌ 오답 집중 복습":
    active_questions = [q for q in base_filtered if q["id"] in st.session_state.wrong_ids]
else:
    active_questions = base_filtered

# 문항이 없을 때의 화면
if not active_questions:
    st.markdown("""
        <div style="text-align: center; padding: 60px 20px;">
            <div style="font-size: 54px;">🎉</div>
            <h3 style="color: #334155; margin-top: 10px;">조건에 해당하는 문제가 없습니다!</h3>
            <p style="color: #64748B;">좌측 사이드바 필터를 변경하거나 다른 학습 모드를 선택해 주세요.</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# 인덱스 안전장치
if st.session_state.current_idx >= len(active_questions):
    st.session_state.current_idx = 0

current_q = active_questions[st.session_state.current_idx]
q_id = current_q["id"]
is_starred = q_id in st.session_state.starred_ids

# -------------------------------------------------------------
# 5. 상단 듀오링고 스타일 진행 게이지 및 별표 버튼
# -------------------------------------------------------------
progress_val = (st.session_state.current_idx + 1) / len(active_questions)
st.progress(progress_val)

top_col1, top_col2, top_col3 = st.columns([6, 2, 2])
with top_col1:
    st.markdown(f"**진행도 {st.session_state.current_idx + 1} / {len(active_questions)}**")
with top_col2:
    st.markdown(f"🔥 **{st.session_state.streak}** 연승")
with top_col3:
    # 별모양 토글 버튼
    star_label = "⭐ 별표됨" if is_starred else "☆ 별표하기"
    if st.button(star_label, key=f"star_btn_{q_id}"):
        if is_starred:
            st.session_state.starred_ids.remove(q_id)
        else:
            st.session_state.starred_ids.add(q_id)
        st.rerun()

# -------------------------------------------------------------
# 6. 문제 카드 렌더링
# -------------------------------------------------------------
st.markdown(f"""
<div class="question-card">
    <span class="question-badge">{current_q['year']}년도 | {current_q['professor']} 교수님 | {current_q['subject']}</span>
    <div class="question-text">Q{st.session_state.current_idx + 1}. {current_q['question']}</div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 7. 선택지 입력 영역
# -------------------------------------------------------------
user_answer_raw = ""

if current_q["type"] == "single_choice":
    if not st.session_state.answered_state:
        # 풀기 전: 선택 가능
        user_choice = st.radio(
            "정답을 선택하세요:",
            current_q["choices"],
            index=None,
            key=f"radio_{q_id}_{st.session_state.current_idx}"
        )
        if user_choice:
            user_answer_raw = user_choice.strip()[0]  # '1', '2' 등 첫 글자 추출
    else:
        # 풀고 난 후: 잠금 상태로 렌더링
        st.markdown(f"**내가 고른 답:** {st.session_state.user_selected_ans}번")

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

# -------------------------------------------------------------
# 8. 액션 버튼 (정답 확인 / 다음 문제)
# -------------------------------------------------------------
st.write("")
if not st.session_state.answered_state:
    # 정답 제출 버튼
    submit_col1, submit_col2 = st.columns([7, 3])
    with submit_col2:
        check_btn = st.button("정답 확인하기 ✔️", use_container_width=True, type="primary")
        
    if check_btn:
        if not user_answer_raw:
            st.warning("답안을 먼저 선택하거나 입력해 주세요!")
        else:
            st.session_state.user_selected_ans = user_answer_raw
            # 채점 검증
            correct_ans = str(current_q["answer"]).strip()
            if current_q["type"] == "single_choice":
                matched = (user_answer_raw == correct_ans)
            else:
                matched = (user_answer_raw.lower() == correct_ans.lower())
                
            st.session_state.is_correct = matched
            st.session_state.answered_state = True
            
            if matched:
                st.session_state.streak += 1
                if q_id in st.session_state.wrong_ids:
                    st.session_state.wrong_ids.remove(q_id)
            else:
                st.session_state.streak = 0
                st.session_state.wrong_ids.add(q_id)
            st.rerun()

else:
    # 결과 피드백 바
    if st.session_state.is_correct:
        st.markdown(f"""
        <div class="feedback-correct">
            <h4 style="margin:0; font-size: 18px;">🎉 정답입니다! 계속 집중해 볼까요?</h4>
            <p style="margin: 4px 0 0 0; font-size: 14px;">정답: <b>{current_q['answer']}</b></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="feedback-wrong">
            <h4 style="margin:0; font-size: 18px;">❌ 아쉽네요! 오답 노트에 자동 저장되었습니다.</h4>
            <p style="margin: 4px 0 0 0; font-size: 14px;">정답: <b>{current_q['answer']}</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    # AI 기전 해설 토글 및 다음 문제 버튼
    col_ai, col_next = st.columns([6, 4])
    with col_ai:
        if st.button("🤖 AI 핵심 기전 해설 보기", key="ai_btn", use_container_width=True):
            st.session_state.show_ai = not st.session_state.show_ai
            
    with col_next:
        next_btn = st.button("다음 문제 넘어가기 ➡️", type="primary", use_container_width=True)
        if next_btn:
            st.session_state.current_idx += 1
            st.session_state.answered_state = False
            st.session_state.show_ai = False
            st.session_state.user_selected_ans = ""
            st.rerun()
            
    # AI 해설 박스 렌더링
    if st.session_state.show_ai:
        st.markdown(f"""
        <div class="ai-box">
            <b>🩺 AI Medical Assistant 기전 요약:</b><br>
            {current_q['ai_explanation']}
        </div>
        """, unsafe_allow_html=True)
