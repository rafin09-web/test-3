import streamlit as st
import time
import random

# 페이지 기본 설정
st.set_page_config(page_title="스피드 상식 퀴즈", page_icon="🧠", layout="centered")

# -----------------------------------------------------------------------------
# 퀴즈 데이터베이스 (총 32개 문제)
# -----------------------------------------------------------------------------
QUIZ_BANK = {
    "일반상식": {
        "쉬움": [
            {"q": "세계에서 가장 큰 바다는 어디일까요?", "options": ["태평양", "대서양", "인도양", "북극해"], "a": "태평양"},
            {"q": "대한민국의 수도는 어디일까요?", "options": ["부산", "서울", "인천", "대구"], "a": "서울"},
            {"q": "피아노의 건반은 총 몇 개일까요?", "options": ["88개", "76개", "61개", "92개"], "a": "88개"},
            {"q": "사과, 바나나, 포도 중 열매채소가 아닌 나무에서 열리는 과일은?", "options": ["수박", "참외", "사과", "딸기"], "a": "사과"},
            {"q": "1년 12달 중 28일이 있는 달은 모두 몇 개일까요?", "options": ["1개", "6개", "12개", "없음"], "a": "12개"},
            {"q": "우리나라의 국화(國花)는 무엇일까요?", "options": ["진달래", "개나리", "무궁화", "장미"], "a": "무궁화"},
            {"q": "올림픽 기에 있는 고리의 개수는 몇 개일까요?", "options": ["4개", "5개", "6개", "7개"], "a": "5개"},
            {"q": "세계에서 인구가 가장 많은 국가로 올라선 나라는?", "options": ["중국", "인도", "미국", "인도네시아"], "a": "인도"},
        ],
        "보통": [
            {"q": "지구에서 가장 넓은 면적을 가진 국가의 이름은?", "options": ["캐나다", "중국", "미국", "러시아"], "a": "러시아"},
            {"q": "노벨 평화상이 수여되는 도시는 어디일까요?", "options": ["스톡홀름", "오슬로", "제네바", "런던"], "a": "오슬로"},
            {"q": "남극대륙에 대한 최초의 영유권을 주장할 수 없도록 만든 협정은?", "options": ["남극조약", "파리협정", "제네바협정", "교토의정서"], "a": "남극조약"},
            {"q": "세계에서 가장 길게 이어지는 산맥은?", "options": ["히말라야 산맥", "알프스 산맥", "안데스 산맥", "로키 산맥"], "a": "안데스 산맥"},
            {"q": "프랑스 혁명이 일어난 연도는 언제일까요?", "options": ["1776년", "1789년", "1812년", "1914년"], "a": "1789년"},
            {"q": "유엔(UN) 상임이사국이 아닌 나라는 어디일까요?", "options": ["독일", "일본", "한국", "위의 셋 다 아님"], "a": "위의 셋 다 아님"},
            {"q": "화폐 단위로 '엔'을 사용하는 나라는?", "options": ["중국", "일본", "베트남", "태국"], "a": "일본"},
            {"q": "에펠탑이 위치한 도시 프랑스 파리의 젖줄이 되는 강 이름은?", "options": ["템스강", "다뉴브강", "센강", "라인강"], "a": "센강"},
        ]
    },
    "과학/IT": {
        "쉬움": [
            {"q": "물 분자를 이루는 원소 중 가장 개수가 많은 것은?", "options": ["수소", "산소", "탄소", "질소"], "a": "수소"},
            {"q": "지구 태양계에서 가장 큰 행성은 무엇일까요?", "options": ["토성", "목성", "천왕성", "해왕성"], "a": "목성"},
            {"q": "사람의 몸에서 혈액을 온몸으로 보내는 펌프 역할을 하는 기관은?", "options": ["간", "폐", "심장", "위"], "a": "심장"},
            {"q": "빛이 1년 동안 진행하는 거리를 나타내는 단위는?", "options": ["파섹", "광년", "천문단위(AU)", "킬로미터"], "a": "광년"},
            {"q": "지구 자기장의 원인이 되며 가장 내부에 위치한 부분은?", "options": ["지각", "맨틀", "외핵", "내핵"], "a": "내핵"},
            {"q": "스마트폰, 컴퓨터 등에서 웹사이트를 볼 때 쓰는 프로그램은?", "options": ["웹 브라우저", "백신", "운영체제", "컴파일러"], "a": "웹 브라우저"},
            {"q": "식물이 빛을 받아 양분을 만드는 작용은?", "options": ["호흡 작용", "증산 작용", "광합성 작용", "소화 작용"], "a": "광합성 작용"},
            {"q": "소금의 화학식(NaCl)에서 Cl이 뜻하는 원소는?", "options": ["나트륨", "염소", "칼슘", "구리"], "a": "염소"},
        ],
        "보통": [
            {"q": "광합성을 할 때 식물이 흡수하는 기체는?", "options": ["산소", "이산화탄소", "질소", "수소"], "a": "이산화탄소"},
            {"q": "컴퓨터의 핵심 연산 장치를 뜻하는 약어는?", "options": ["RAM", "GPU", "CPU", "HDD"], "a": "CPU"},
            {"q": "원소 기호 'Au'가 나타내는 금속은 무엇일까요?", "options": ["은", "금", "구리", "철"], "a": "금"},
            {"q": "지구 대기 성분 중 가장 많은 비율을 차지하는 기체는?", "options": ["산소", "질소", "이산화탄소", "아르곤"], "a": "질소"},
            {"q": "전자의 흐름을 방해하는 성질을 뜻하는 전기 용어는?", "options": ["전압", "전류", "저항", "전력"], "a": "저항"},
            {"q": "파이썬(Python) 프로그래밍 언어의 마스코트 동물은?", "options": ["고양이", "뱀", "코끼리", "돌고래"], "a": "뱀"},
            {"q": "빛이 파동의 성질을 가지고 있음을 보여주는 현상이 아닌 것은?", "options": ["굴절", "간섭", "회절", "광전효과"], "a": "광전효과"},
            {"q": "인간의 DNA 이중 헬릭스 구조를 이루는 염기쌍의 수가 아닌 것은?", "options": ["아데닌(A)", "구아닌(G)", "시토신(C)", "우라실(U)"], "a": "우라실(U)"},
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
if 'time_limit' not in st.session_state:
    st.session_state.time_limit = 30

# -----------------------------------------------------------------------------
# 게임 제어 함수
# -----------------------------------------------------------------------------
def start_game(category, difficulty):
    pool = QUIZ_BANK[category][difficulty]
    st.session_state.questions = random.sample(pool, len(pool))
    st.session_state.score = 0
    st.session_state.combo = 0
    st.session_state.current_idx = 0
    st.session_state.start_time = time.time()
    st.session_state.game_status = 'playing'

def submit_answer(user_answer, correct_answer):
    if user_answer == correct_answer:
        st.session_state.combo += 1
        points = 100 + (st.session_state.combo * 20)
        st.session_state.score += points
        st.toast(f"⭕ 정답입니다! (+{points}점, {st.session_state.combo}연속!)", icon="🎉")
    else:
        st.session_state.combo = 0
        # 틀렸을 때 감점 (-30점), 최소 점수는 0점으로 보장
        st.session_state.score = max(0, st.session_state.score - 30)
        st.toast(f"❌ 오답입니다! (-30점) [정답: {correct_answer}]", icon="⚠️")

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

    if remaining_time <= 0 or st.session_state.current_idx >= len(st.session_state.questions):
        st.session_state.game_status = 'ended'
        st.rerun()

    # 스탯 대시보드
    col1, col2, col3 = st.columns(3)
    col1.metric("⏱️ 남은 시간", f"{remaining_time}초")
    col2.metric("🏆 현재 점수", f"{st.session_state.score}점")
    col3.metric("🔥 연속 정답", f"{st.session_state.combo}회")

    # 실시간 진행바 (Progress Bar)
    progress_val = remaining_time / st.session_state.time_limit
    st.progress(progress_val)
    
    st.write("---")

    # 문제 출력
    q_data = st.session_state.questions[st.session_state.current_idx]
    st.markdown(f"### Q{st.session_state.current_idx + 1}. {q_data['q']}")

    # 보기 버튼
    cols = st.columns(2)
    for idx, option in enumerate(q_data['options']):
        with cols[idx % 2]:
            if st.button(option, key=f"opt_{idx}", use_container_width=True):
                submit_answer(option, q_data['a'])
                st.rerun()

    # 타이머 실시간 자동 갱신 (1초 후 rerun)
    time.sleep(1)
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
