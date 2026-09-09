import streamlit as st
import time
import random

# 페이지 기본 설정
st.set_page_config(page_title="스피드 상식 퀴즈", page_icon="🧠", layout="centered")

# -----------------------------------------------------------------------------
# 퀴즈 데이터베이스 (카테고리 및 난이도별)
# -----------------------------------------------------------------------------
QUIZ_BANK = {
    "일반상식": {
        "쉬움": [
            {"q": "세계에서 가장 큰 바다는 어디일까요?", "options": ["태평양", "대서양", "인도양", "북극해"], "a": "태평양"},
            {"q": "대한민국의 수도는 어디일까요?", "options": ["부산", "서울", "인천", "대구"], "a": "서울"},
        ],
        "보통": [
            {"q": "지구에서 가장 넓은 면적을 가진 국가의 이름은?", "options": ["캐나다", "중국", "미국", "러시아"], "a": "러시아"},
            {"q": "노벨 평화상이 수여되는 도시는 어디일까요?", "options": ["스톡홀름", "오슬로", "제네바", "런던"], "a": "오슬로"},
        ]
    },
    "과학/IT": {
        "쉬움": [
            {"q": "물 분자를 이루는 원소 중 가장 개수가 많은 것은?", "options": ["수소", "산소", "탄소", "질소"], "a": "수소"},
            {"q": "지구 태양계에서 가장 큰 행성은 무엇일까요?", "options": ["토성", "목성", "천왕성", "해왕성"], "a": "목성"},
        ],
        "보통": [
            {"q": "광합성을 할 때 식물이 흡수하는 기체는?", "options": ["산소", "이산화탄소", "질소", "수소"], "a": "이산화탄소"},
            {"q": "컴퓨터의 핵심 연산 장치를 뜻하는 약어는?", "options": ["RAM", "GPU", "CPU", "HDD"], "a": "CPU"},
        ]
    }
}

# -----------------------------------------------------------------------------
# 세션 상태 초기화
# -----------------------------------------------------------------------------
if 'game_status' not in st.session_state:
    st.session_state.game_status = 'ready'  # 'ready', 'playing', 'ended'
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'combo' not in st.session_state:
    st.session_state.combo = 0
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'start_time' not in st.session_state:
    st.session_state.start_time = 0

# -----------------------------------------------------------------------------
# 게임 제어 함수
# -----------------------------------------------------------------------------
def start_game(category, difficulty):
    st.session_state.questions = random.sample(
        QUIZ_BANK[category][difficulty], 
        len(QUIZ_BANK[category][difficulty])
    )
    st.session_state.score = 0
    st.session_state.combo = 0
    st.session_state.current_idx = 0
    st.session_state.start_time = time.time()
    st.session_state.game_status = 'playing'

def submit_answer(user_answer, correct_answer):
    if user_answer == correct_answer:
        st.session_state.combo += 1
        # 연속 정답(콤보) 가산점 계산
        points = 100 + (st.session_state.combo * 20)
        st.session_state.score += points
        st.toast(f"⭕ 정답입니다! (+{points}점, {st.session_state.combo}연속!)", icon="🎉")
    else:
        st.session_state.combo = 0
        st.toast(f"❌ 오답입니다! (정답: {correct_answer})", icon="⚠️")

    st.session_state.current_idx += 1
    if st.session_state.current_idx >= len(st.session_state.questions):
        st.session_state.game_status = 'ended'

# -----------------------------------------------------------------------------
# UI 화면 구성
# -----------------------------------------------------------------------------
st.title("🧠 스피드 상식 퀴즈")

# 1. 게임 시작 대기 화면
if st.session_state.game_status == 'ready':
    st.subheader("⚙️ 게임 설정")
    selected_cat = st.selectbox("카테고리 선택", list(QUIZ_BANK.keys()))
    selected_diff = st.radio("난이도 선택", ["쉬움", "보통"], horizontal=True)
    time_limit = st.slider("제한시간 (초)", 10, 60, 30)

    if st.button("🚀 퀴즈 시작", use_container_width=True, type="primary"):
        st.session_state.time_limit = time_limit
        start_game(selected_cat, selected_diff)
        st.rerun()

# 2. 게임 진행 화면
elif st.session_state.game_status == 'playing':
    # 제한시간 체크
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, int(st.session_state.time_limit - elapsed_time))

    if remaining_time <= 0:
        st.session_state.game_status = 'ended'
        st.rerun()

    # 상단 대시보드
    col1, col2, col3 = st.columns(3)
    col1.metric("⏱️ 남은 시간", f"{remaining_time}초")
    col2.metric("🏆 현재 점수", f"{st.session_state.score}점")
    col3.metric("🔥 연속 정답", f"{st.session_state.combo}회")

    st.progress(remaining_time / st.session_state.time_limit)
    st.write("---")

    # 현재 문제 출력
    q_data = st.session_state.questions[st.session_state.current_idx]
    st.markdown(f"### Q{st.session_state.current_idx + 1}. {q_data['q']}")

    # 보기 버튼 배치
    cols = st.columns(2)
    for idx, option in enumerate(q_data['options']):
        with cols[idx % 2]:
            if st.button(option, key=f"opt_{idx}", use_container_width=True):
                submit_answer(option, q_data['a'])
                st.rerun()

# 3. 게임 종료 화면
elif st.session_state.game_status == 'ended':
    st.balloons()
    st.subheader("🏁 게임 종료!")
    st.metric(label="최종 점수", value=f"{st.session_state.score} 점")

    st.write("---")
    if st.button("🔄 다시 도전하기", use_container_width=True, type="primary"):
        st.session_state.game_status = 'ready'
        st.rerun()
