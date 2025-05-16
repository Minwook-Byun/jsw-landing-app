# streamlit_app_final_v1.py

import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import base64 # 로고 이미지 인코딩을 위해 추가
from pathlib import Path # 파일 경로 처리를 위해 추가

# --- 페이지 설정 (가장 먼저 호출되어야 함) ---
st.set_page_config(
    page_title="사회서비스 투자유치 지원 프로그램", # 브라우저 탭에 표시될 제목
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed" # 사이드바 사용 안 함 (옵션)
)

# --- 데이터 로드 (이전과 동일) ---
schedule_data = {
    "행사명": ["소셜링크 아카데미 Kick-off", "1차 아카데미 워크숍", "투자 기초 교육", "투자교류회 설명회", "2차 아카데미 워크숍", "동반성장 워크숍", "투자교류회 본행사", "성과공유회"],
    "시작일": [datetime(2025, 3, 1), datetime(2025, 3, 15), datetime(2025, 4, 5), datetime(2025, 4, 20), datetime(2025, 5, 10), datetime(2025, 6, 5), datetime(2025, 7, 15), datetime(2025, 8, 20)],
    "종료일": [datetime(2025, 3, 1), datetime(2025, 3, 16), datetime(2025, 4, 6), datetime(2025, 4, 20), datetime(2025, 5, 11), datetime(2025, 6, 6), datetime(2025, 7, 16), datetime(2025, 8, 20)],
    "주요 내용": ["아카데미 시작 및 네트워킹", "사회서비스 특화 모듈", "임팩트 투자 이해", "참여 기업/투자자 모집 안내", "사업계획서 작성 심화", "선배 기업과의 만남", "기업 IR 및 투자자 매칭", "프로그램 성과 발표 및 시상"]
}
schedule_df = pd.DataFrame(schedule_data)
schedule_df["시작일"] = pd.to_datetime(schedule_df["시작일"])
schedule_df["종료일"] = pd.to_datetime(schedule_df["종료일"])

# --- 로고 이미지 Base64 인코딩 함수 ---
def img_to_base64(img_path_str):
    img_path = Path(img_path_str)
    if not img_path.is_file():
        # st.error(f"로고 파일을 찾을 수 없습니다: {img_path_str}") # 디버깅 시 사용
        return None
    try:
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception as e:
        # st.error(f"로고 파일 로딩 중 오류 발생 ({img_path_str}): {e}") # 디버깅 시 사용
        return None

# --- 고정 헤더 및 플로팅 버튼 HTML/CSS 삽입 함수 ---
def inject_custom_elements(logo_base64, google_form_url):
    HEADER_HEIGHT_PX = 65 # 헤더 높이 (CSS와 일치시켜야 함)
    
    logo_html_element = ""
    if logo_base64:
        logo_html_element = f'<img src="data:image/png;base64,{logo_base64}" alt="로고" class="header-logo">'
    else:
        # 로고 없을 경우 빈 공간 유지 또는 텍스트 로고
        logo_html_element = '<span class="header-logo-placeholder"></span>'

    custom_elements_html = f"""
    <style>
        .fixed-header {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: {HEADER_HEIGHT_PX}px;
            background-color: #FFFFFF; /* 흰색 배경 */
            padding: 0 25px; /* 좌우 패딩 */
            border-bottom: 1px solid #E0E0E0; /* 구분선 */
            z-index: 999;
            display: flex;
            align-items: center; /* 수직 중앙 정렬 */
            box-sizing: border-box;
        }}
        .header-logo {{
            height: 35px; /* 로고 높이 */
            margin-right: 15px;
            object-fit: contain;
        }}
        .header-logo-placeholder {{
            display: inline-block; /* 로고 없을 때 공간 차지 */
            width: 1px; /* 최소 너비 */
            height: 35px;
            margin-right: 15px;
        }}
        .header-title {{
            font-size: 1.15em; /* 제목 폰트 크기 */
            font-weight: 600; /* 폰트 두께 */
            color: #1E1E1E; /* 글자 색상 */
        }}

        .fab {{ /* 플로팅 액션 버튼 */
            position: fixed;
            bottom: 25px;
            right: 25px;
            background-color: #FF4B4B; /* Streamlit 테마 레드 */
            color: white !important; /* 글자색 흰색, !important로 우선순위 */
            padding: 12px 18px;
            border-radius: 8px; /* 살짝 둥근 모서리 */
            text-decoration: none;
            font-size: 0.95em;
            font-weight: 500;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            z-index: 1000;
            transition: background-color 0.2s ease, transform 0.2s ease;
        }}
        .fab:hover {{
            background-color: #E03C3C; /* 호버 시 약간 어둡게 */
            color: white !important;
            text-decoration: none;
            transform: translateY(-2px); /* 살짝 위로 이동 */
        }}
        /* Streamlit 메인 콘텐츠 상단에 헤더 높이만큼 여백 추가 */
        div[data-testid="stAppViewContainer"] > section {{
            padding-top: {HEADER_HEIGHT_PX + 15}px; /* 헤더 높이 + 약간의 추가 여백 */
        }}
    </style>

    <div class="fixed-header">
        {logo_html_element}
        <div class="header-title">2025년 사회서비스 투자 유치 역량 강화 프로그램</div>
    </div>
    
    <a href="{google_form_url}" target="_blank" class="fab">📝 여기서 지원하기</a>
    """
    st.markdown(custom_elements_html, unsafe_allow_html=True)

# --- 메인 로직: 커스텀 요소 삽입 ---
LOGO_PATH = "[MYSC]로고_placeholder.png" # 로고 파일 경로
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/12THQKNTcyzoK95dObbgmrOGJfjqAvkvpyMbB6JAeBk8/viewform"

logo_b64 = img_to_base64(LOGO_PATH)
inject_custom_elements(logo_b64, GOOGLE_FORM_URL)


# --- 각 섹션별 콘텐츠 함수 정의 (이전과 유사, display_registration_form 삭제) ---

def display_introduction():
    # st.title 제거 또는 변경 (헤더에 이미 프로그램명 있음)
    st.markdown(
        """
        ### 사회서비스의 새로운 가치를 위한 투자, MYSC와 함께 시작하세요!
        본 프로그램은 사회서비스 분야 기업의 투자 유치 역량을 강화하고,
        실질적인 투자 연계 기회를 제공하여 사회서비스 시장의 지속 가능한 성장을 지원합니다.

        **주요 목표:**
        - 사회서비스 기업의 투자 이해도 제고 및 IR 역량 강화
        - 투자자와 사회서비스 기업 간의 네트워킹 활성화
        - 성공적인 투자 유치 사례 발굴 및 확산

        제안서에 언급된 **L.E.N.S (Linkage, Expertise, Network, Support)** 접근법을 통해
        국민 삶의 질 향상이라는 실질적 임팩트에 집중합니다.
        """
    )
    try:
        st.image("social_investment_placeholder.jpg", caption="사회서비스 분야의 혁신과 성장을 지원합니다.", use_container_width=True)
    except Exception as e:
        st.warning(f"관련 이미지를 불러올 수 없습니다. 파일 경로를 확인하세요. (오류: {e})")
        st.markdown("_(프로그램 관련 이미지 영역)_")

def display_program_info():
    st.header("📚 프로그램 상세 소개")
    tab1, tab2, tab3 = st.tabs(["💡 소셜링크 아카데미", "🤝 투자교류회", "🌱 기타 주요 활동"])
    with tab1:
        st.subheader("💡 소셜링크 아카데미")
        st.markdown("소셜링크 아카데미 상세 내용...")
        st.info("세부 커리큘럼 및 일정은 추후 확정 공지됩니다.")
    with tab2:
        st.subheader("🤝 투자교류회")
        st.markdown("투자교류회 상세 내용...")
        st.warning("투자교류회 참가 기업/투자자 모집은 별도 공지를 통해 진행됩니다.")
    with tab3:
        st.subheader("🌱 기타 주요 활동")
        st.markdown("기타 주요 활동 상세 내용...")

def display_eligibility_criteria():
    st.header("🎟️ 지원 대상")
    st.markdown(
        """
        비즈니스모델 고도화 및 투자 유치 역량 강화를 필요로 하는 사회서비스 기업.
        *(예: 소셜벤처, (예비)사회적기업, 사회적협동조합, 자활기업 등 법인격 무관)*
        """
    )
    st.markdown("---")
    st.markdown("##### 선발 대상 및 규모")
    st.markdown("- 총 **13개 기업** 내외")

def display_schedule(): # 이전 버전의 Plotly 차트 함수 사용
    st.header("🗓️ 소셜링크 아카데미 주요 일정")
    st.info("아래 일정은 예시이며, 실제 진행 시 변동될 수 있습니다. 타임라인의 막대 위에 마우스를 올리면 세부 내용을 확인할 수 있습니다.")
    social_link_story_events = ["소셜링크 아카데미 Kick-off", "1차 아카데미 워크숍", "2차 아카데미 워크숍", "동반성장 워크숍", "성과공유회"]
    filtered_schedule = schedule_df[schedule_df["행사명"].isin(social_link_story_events)].copy()
    if filtered_schedule.empty:
        st.warning("표시할 아카데미 관련 일정이 없습니다.")
        return
    filtered_schedule = filtered_schedule.sort_values(by="시작일").reset_index(drop=True)
    plot_data = filtered_schedule.copy()
    plot_data['시각화_종료일'] = plot_data['종료일'] + pd.Timedelta(days=1)
    fig = px.timeline(plot_data, x_start="시작일", x_end="시각화_종료일", y="행사명", color="행사명", custom_data=['시작일', '종료일', '주요 내용'])
    fig.update_layout(title_text='소셜링크 아카데미 타임라인', title_x=0.5, xaxis_title="날짜", yaxis_title="행사명", showlegend=False, font=dict(family="Malgun Gothic, Apple SD Gothic Neo, Arial, sans-serif", size=12))
    fig.update_yaxes(categoryorder="array", categoryarray=plot_data["행사명"].tolist())
    fig.update_traces(hovertemplate="<b>%{y}</b><br><br>시작일: %{customdata[0]|%Y년 %m월 %d일}<br>종료일: %{customdata[1]|%Y년 %m월 %d일}<br>주요 내용: %{customdata[2]}<extra></extra>")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    st.markdown("##### 각 행사 세부 정보")
    display_table_data = filtered_schedule[['행사명', '시작일', '종료일', '주요 내용']].copy()
    display_table_data['시작일'] = display_table_data['시작일'].dt.strftime('%Y-%m-%d')
    display_table_data['종료일'] = display_table_data['종료일'].dt.strftime('%Y-%m-%d')
    st.table(display_table_data.set_index('행사명'))

def display_contact_info():
    st.header("📞 문의하기")
    st.subheader("프로그램 운영 사무국 (MYSC)")
    st.markdown(
        """
        **주소:** (MYSC 주소) 서울특별시 성동구 왕십리로 88 (실제 주소로 변경 필요)
        **이메일:** (MYSC 담당자 이메일) contact@mysc.co.kr
        **연락처:** (MYSC 담당자 연락처) 02-XXX-XXXX
        """
    )

# --- 메인 페이지 레이아웃 (st.title 제거, display_registration_form 제거) ---
# st.title("🚀 2025년 사회서비스 투자 유치 역량 강화 프로그램") # 헤더에 유사한 제목이 있으므로 제거 또는 수정

display_introduction()
st.markdown("---")

display_program_info()
st.markdown("---")

display_eligibility_criteria()
st.markdown("---")

display_schedule()
st.markdown("---")

# display_registration_form() # 이 섹션 제거됨

display_contact_info()
st.markdown("---")

# --- 푸터 정보 (주관/운영 정보 추가) ---
st.caption(
    """
    © 2025 MYSC & 중앙사회서비스원. All rights reserved.  
    **주관:** 중앙사회서비스원  |  **운영:** MYSC (주식회사 엠와이소셜컴퍼니)
    """
)