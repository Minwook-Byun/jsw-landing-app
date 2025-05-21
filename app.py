import streamlit as st
# import pandas as pd # 현재 사용 안 함
# from datetime import datetime # 현재 사용 안 함
import base64
from pathlib import Path

# --- 페이지 설정 ---
st.set_page_config(
    page_title="사회서비스 투자역량 강화 아카데미 소링아 3기",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

KEY_ORANGE_COLOR = "#FF7043"
TEXT_COLOR_BODY_STRONG = "#2c3e50"
TEXT_COLOR_CAPTION = "#555555"
CARD_BACKGROUND_COLOR = "#ffffff"
TEXT_COLOR_HEADINGS = "#1A1B1E" # 사용될 수 있으므로 유지
HOVER_TEXT_COLOR_WHITE = "#FFFFFF" # 사용될 수 있으므로 유지
GRADIENT_START_COLOR = "#FFA07A" # 연한 주황
GRADIENT_END_COLOR = KEY_ORANGE_COLOR # 진한 주황

# --- 이미지 Base64 인코딩 함수 ---
def image_to_data_uri(file_path_str):
    file_path = Path(file_path_str)
    if not file_path.is_file(): return None
    try:
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        ext = file_path.suffix.lower()
        mime_type = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", 
                     ".gif": "image/gif", ".svg": "image/svg+xml"}.get(ext, "application/octet-stream")
        return f"data:{mime_type};base64,{encoded_string}"
    except Exception: return None

# --- 전역 상수 ---
HEADER_HEIGHT_PX = 65
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/12THQKNTcyzoK95dObbgmrOGJfjqAvkvpyMbB6JAeBk8/viewform"
KEY_ORANGE_COLOR = "#FF7043"
KEY_LIME_GREEN_COLOR = "#8BC34A" 
TEXT_COLOR_HEADINGS = "#1A1B1E"
TEXT_COLOR_BODY_STRONG = "#2c3e50"
TEXT_COLOR_BODY = "#333D4B" # display_post_hero_section 에서는 #34495e 사용
TEXT_COLOR_CAPTION = "#555555"
TEXT_COLOR_PLACEHOLDER = "#888888"
BACKGROUND_COLOR_SECTION_LIGHT_GRAY = "#f9fafb"
BACKGROUND_COLOR_SECTION_MEDIUM_GRAY = "#f0f2f5"
BACKGROUND_COLOR_SECTION_WHITE = "#ffffff"
CARD_BACKGROUND_COLOR = "#ffffff"
HEADER_NAV_TEXT_COLOR = "#4A4A4A"

# === 섹션 0: 고정 헤더 및 FAB (헤더 메뉴 및 앵커 스크롤 수정) ===
def inject_custom_elements(google_form_url_param):
    logo_bogun_filename = "bogun.jpg" # 실제 파일 경로에 맞게 수정 필요
    logo_mysc_filename = "[MYSC]로고_placeholder.png" # 실제 파일 경로에 맞게 수정 필요
    logo_bogun_data_uri = image_to_data_uri(logo_bogun_filename)
    logo_mysc_data_uri = image_to_data_uri(logo_mysc_filename)
    logo_bogun_html = f'<img src="{logo_bogun_data_uri}" alt="보건복지부 로고" class="header-logo logo-bogun">' if logo_bogun_data_uri else '<span class="logo-placeholder">보건복지부</span>'
    logo_mysc_html = f'<img src="{logo_mysc_data_uri}" alt="MYSC 로고" class="header-logo logo-mysc">' if logo_mysc_data_uri else '<span class="logo-placeholder">MYSC</span>'
    
    nav_items_data = [
        {"label": "지원 대상", "id_target": "who-can-apply-section"},
        {"label": "지원 혜택", "id_target": "benefits-section"},
        {"label": "프로그램", "id_target": "section-program"}, 
        {"label": "접수 방법", "id_target": "application-method-section"},
        {"label": "문의하기", "id_target": "contact-info-section"}
    ]
    nav_html_elements = "".join([f'<a href="#{item["id_target"]}" class="header-nav-item">{item["label"]}</a>' for item in nav_items_data])

    section_ids_for_scroll_margin = [item["id_target"] for item in nav_items_data] + ["post-hero-section", "hero-banner"]
    scroll_margin_selectors = ", ".join([f"#{id_name}" for id_name in section_ids_for_scroll_margin if id_name])

    custom_elements_html = f"""
    <style>
        /* Pretendard 웹폰트 로드 */
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css');
        
        /* 전체 페이지 기본 폰트 설정 (필요시) */
        body, .stApp {{ /* .stApp은 Streamlit의 최상위 앱 컨테이너를 타겟할 수 있습니다 */
            font-family: 'Pretendard', sans-serif !important;
        }}

        {scroll_margin_selectors} {{
            scroll-margin-top: {HEADER_HEIGHT_PX + 20}px !important;
        }}
        html {{
            scroll-behavior: smooth;
        }}

        .fixed-header {{
            position: fixed; top: 0; left: 0; width: 100%; height: {HEADER_HEIGHT_PX}px;
            background-color: rgba(255, 255, 255, 0.97);
            padding: 0 25px; 
            border-bottom: 1px solid #EAEAEA;
            z-index: 1000;
            display: flex; 
            justify-content: center; 
            align-items: center;
            box-sizing: border-box;
            -webkit-backdrop-filter: blur(6px);
            backdrop-filter: blur(6px); 
        }}
        .header-content {{ 
            display: flex;
            justify-content: space-between; 
            align-items: center;
            width: 100%;
            max-width: 1160px;
            height: 100%;
        }}
        .header-logo-group {{ display: flex; align-items: center; }}
        .header-logo {{ height: 36px; object-fit: contain; display: block; }}
        .logo-mysc {{ margin-left: 15px; }}
        .logo-placeholder {{ font-weight: bold; color: #333; }}

        .header-nav {{ display: flex; align-items: center; }}
        .header-nav-item {{
            text-decoration: none;
            color: {HEADER_NAV_TEXT_COLOR};
            font-size: 15px; 
            font-weight: 500; 
            padding: 8px 14px; 
            margin-left: 10px; 
            border-radius: 6px;
            transition: color 0.2s ease, background-color 0.2s ease;
        }}
        .header-nav-item:hover, .header-nav-item:focus {{ 
            color: {KEY_ORANGE_COLOR}; 
            background-color: rgba(255, 112, 67, 0.08); 
            outline: none; 
        }}
        
        @media (max-width: 992px) {{ 
            .header-nav {{ display: none; }} 
            .header-content {{ justify-content: center; }} 
        }}
        @media (max-width: 480px) {{
             .header-logo {{ height: 32px; }} 
        }}

        .fab {{
            position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
            width: 90%; max-width: 480px; 
            background-color: {KEY_LIME_GREEN_COLOR}; color: white !important; 
            padding: 16px 20px; 
            border-radius: 10px; 
            text-decoration: none; font-size: 1.1em; 
            font-weight: 600; text-align: center;
            box-shadow: 0 5px 12px rgba(0,0,0,0.18); 
            z-index: 999; 
            transition: background-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .fab:hover {{ 
            background-color: #7CB342; transform: translateX(-50%) translateY(-2px); 
            box-shadow: 0 7px 18px rgba(0,0,0,0.22); 
        }}
        
        div[data-testid="stAppViewContainer"] > section.main {{ 
            padding-top: {HEADER_HEIGHT_PX + 10}px !important; 
        }}
    </style>
    <div class="fixed-header">
        <div class="header-content">
            <div class="header-logo-group">{logo_bogun_html}{logo_mysc_html}</div>
            <nav class="header-nav">{nav_html_elements}</nav>
        </div>
    </div>
    <a href="{google_form_url_param}" target="_blank" class="fab">📝 지원하기</a>"""
    st.markdown(custom_elements_html, unsafe_allow_html=True)

# === 섹션 1: 히어로 배너 ===
def display_hero_banner():
    background_image_filename = "bg.jpg"
    image_data_uri = image_to_data_uri(background_image_filename)
    background_style = f"background-image: url(\"{image_data_uri}\");" if image_data_uri else "background-color: #333333;"
    hero_text_top_padding = f"{HEADER_HEIGHT_PX + 40}px" 
    hero_html = f"""
    <style>
        #hero-banner {{ 
            height: 100vh; {background_style} background-size: cover; background-position: center; 
            display: flex; flex-direction: column; align-items: center; justify-content: flex-start; 
            text-align: center; padding-top: {hero_text_top_padding}; padding-left: 20px; padding-right: 20px; 
            box-sizing: border-box; position: relative; 
            font-family: 'Pretendard', sans-serif; /* 명시적 폰트 설정 */
        }}
        #hero-banner .hero-text-container {{ opacity: 0; animation: fadeInAppearHeroText 1.5s ease-out 0.5s forwards; }}
        #hero-banner .hero-main-text {{ color: white; font-size: 2.8em; font-weight: bold; line-height: 1.4; text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.75); }}
        @keyframes fadeInAppearHeroText {{ 0% {{ opacity: 0; transform: scale(0.95) translateY(15px); }} 100% {{ opacity: 1; transform: scale(1) translateY(0); }} }}
        @media (max-width: 992px) {{ #hero-banner .hero-main-text {{ font-size: 2.4em; }} }} 
        @media (max-width: 768px) {{ #hero-banner .hero-main-text {{ font-size: 2.0em; }} }} 
        @media (max-width: 576px) {{ #hero-banner .hero-main-text {{ font-size: 1.7em; }} }}
    </style>
    <div id="hero-banner"><div class="hero-text-container"><div class="hero-main-text">연결을 통해 확장을 꿈꾸는<br>국내 최초 사회서비스 전문 액셀러레이팅 <br> 소셜 링크 아카데미(Social Link Academy) 3기</div></div></div>"""
    st.markdown(hero_html, unsafe_allow_html=True)

# === 섹션 2: "막막했던 투자유치..." (디자인 개선) ===
def display_post_hero_section():
    program_name = "소셜 링크 아카데미"
    
    # 기존 설명 텍스트
    original_base_text = "는 사회서비스 분야 전문 교육과정입니다. <br> 우수한 기술력과 잠재력을 보유한 사회서비스 기업*의 사회서비스 이해를 돕고,<br>투자 유치 역량을 강화해 국민의 삶을 HEAL하는 소셜 링커(Social Linker)로의 성장에 함께합니다."
    
    # 강조할 부분
    target_phrase = "국민의 삶을 HEAL하는 소셜 링커(Social Linker)로의 성장"
    # 강조 스타일 적용된 부분
    highlighted_phrase = f"<span style='color: {KEY_ORANGE_COLOR}; font-weight: 600;'>{target_phrase}</span>"
    
    # 원본 텍스트에서 해당 부분을 교체
    modified_base_text = original_base_text.replace(target_phrase, highlighted_phrase)

    # 법적 근거 텍스트
    legal_note_text = "*사회서비스 기업이란? : 사회서비스 이용 및 이용권 관리에 관한 법률 제2조1항 」 및 「사회보장기본법 제3조4항」에 근거하여 복지, 보건·의료, 교육, 고용, 주거, 문화, 환경 등의 분야에서 상담, 재활 돌봄, 정보제공, 시설 이용, 역량 개발, 사회참여 등을 통해 국민의 삶의 질 개선·향상을 지원하는 서비스 제공기업"

    TEXT_COLOR_BODY_FOR_P = "#34495e" 

    section_html = f"""
    <style>
        #post-hero-section {{
            background-color: {BACKGROUND_COLOR_SECTION_LIGHT_GRAY};
            padding: 80px 25px; /* 상하 패딩 조정 */
            text-align: center;
            margin-top: 0; 
            font-family: 'Pretendard', sans-serif;
        }}
        #post-hero-section .content-wrapper {{
            max-width: 850px; 
            margin: 0 auto;
        }}
        #post-hero-section .section-icon {{
            font-size: 2.8em; 
            color: {KEY_ORANGE_COLOR}; 
            margin-bottom: 20px; 
            line-height: 1;
            display: block; 
        }}
        #post-hero-section h2 {{
            font-size: 2.4em; /* 폰트 크기 조정 */
            font-weight: 700;
            color: {TEXT_COLOR_BODY_STRONG}; 
            margin-bottom: 25px; /* 간격 조정 */
            line-height: 1.45; 
        }}
        #post-hero-section p.subtitle-text {{
            font-size: 1.25em; /* 폰트 크기 조정 */
            color: {TEXT_COLOR_BODY_FOR_P}; 
            line-height: 1.8; /* 행간 조정 */
            margin: 0 auto;
            max-width: 780px; 
            margin-bottom: 30px; /* 법적 근거 텍스트와의 간격 */
        }}
        #post-hero-section p.subtitle-text .highlight-program {{
            color: {KEY_ORANGE_COLOR};
            font-weight: 600; 
        }}
        /* 법적 근거 텍스트 스타일 */
        #post-hero-section .legal-note {{
            font-size: 0.9em; /* 작은 글씨 */
            color: {TEXT_COLOR_CAPTION}; /* 회색 계열 */
            line-height: 1.65;
            margin-top: 20px; 
            max-width: 750px; 
            margin-left: auto;
            margin-right: auto;
            text-align: justify; /* 양쪽 정렬 또는 left */
            padding: 15px 20px;
            background-color: rgba(0,0,0,0.03); /* 매우 연한 배경으로 구분 */
            border-left: 4px solid #dddddd; /* 연한 회색 좌측 바 */
            border-radius: 4px;
        }}

        @media (max-width: 992px) {{
            #post-hero-section h2 {{ font-size: 2.1em; }}
            #post-hero-section p.subtitle-text {{ font-size: 1.15em; }}
            #post-hero-section .section-icon {{ font-size: 2.6em; }}
            #post-hero-section .legal-note {{ font-size: 0.85em; }}
        }}
        @media (max-width: 768px) {{
            #post-hero-section {{ padding: 70px 20px; }}
            #post-hero-section h2 {{ font-size: 1.9em; margin-bottom: 20px; }}
            #post-hero-section p.subtitle-text {{ font-size: 1.1em; margin-bottom:25px; }}
            #post-hero-section .section-icon {{ font-size: 2.4em; margin-bottom: 15px; }}
            #post-hero-section .legal-note {{ font-size: 0.8em; padding: 12px 15px;}}
        }}
        @media (max-width: 576px) {{
            #post-hero-section h2 {{ font-size: 1.7em; }}
            #post-hero-section p.subtitle-text {{ font-size: 1.0em; }}
            #post-hero-section .section-icon {{ font-size: 2.2em; }}
            #post-hero-section .legal-note {{ font-size: 0.75em; }}
        }}
    </style>
    <div id="post-hero-section">
        <div class="content-wrapper">
            <span class="section-icon">💡</span>
            <h2>사회서비스 분야에서 다양하고 <br> 혁신적인 아이디어를 통해<br>국민의 삶의 질 향상을 꿈꾸고 계신가요?</h2>
            <p class="subtitle-text">
                <span class="highlight-program">{program_name}</span>{modified_base_text}
            </p>
            <p class="legal-note">
                {legal_note_text}
            </p>
        </div>
    </div>
    """
    st.markdown(section_html, unsafe_allow_html=True)

# 다이어그램에 필요한 전역 상수 (실제 사용 시에는 전체 코드 상단에 이미 정의되어 있을 것입니다)
KEY_ORANGE_COLOR = "#FF7043"
TEXT_COLOR_BODY_STRONG = "#2c3e50"
TEXT_COLOR_CAPTION = "#555555"
CARD_BACKGROUND_COLOR = "#ffffff"
HUB_BACKGROUND_COLOR = "rgba(255, 245, 238, 0.95)"

def display_program_diagram():
    # 사용할 색상 (주황색 계열 그라데이션 및 텍스트)
    gradient_start_color = "#FFA07A" # Light Salmon (연한 주황)
    gradient_end_color = KEY_ORANGE_COLOR # 기존 주황색
    box_text_color = TEXT_COLOR_BODY_STRONG
    hub_text_color = KEY_ORANGE_COLOR
    hub_background_color = "rgba(255, 245, 238, 0.8)" # 매우 연한 주황색 배경 (또는 흰색)
    hub_border_color = KEY_ORANGE_COLOR

    diagram_html = f"""
    <style>
        .diagram-container {{
            position: relative;
            width: 100%;
            max-width: 800px; /* 전체 다이어그램 최대 너비 */
            margin: 50px auto; /* 페이지 내 중앙 정렬 및 상하 여백 */
            padding: 20px;
            font-family: 'Pretendard', sans-serif;
        }}
        .top-boxes-row {{
            display: flex;
            justify-content: space-between; /* 박스 간 간격 균등하게 */
            align-items: flex-start; /* 상단 정렬 */
            margin-bottom: 70px; /* 중앙 허브와의 간격 확보 */
        }}
        .program-box {{
            background-color: {CARD_BACKGROUND_COLOR};
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 20px;
            width: 31%; /* 3개의 박스가 적절히 배치되도록 */
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            text-align: left;
            min-height: 180px; /* 최소 높이 */
            position: relative; /* 화살표 위치 기준점 */
        }}
        .program-box h3 {{
            font-size: 1.1em;
            font-weight: 600;
            color: {box_text_color};
            margin-top: 0;
            margin-bottom: 15px;
            text-align: center;
        }}
        .program-box ul {{
            list-style-type: none;
            padding-left: 0;
            margin: 0;
            font-size: 0.9em;
            color: {TEXT_COLOR_CAPTION};
        }}
        .program-box li {{
            margin-bottom: 6px;
            padding-left: 15px;
            position: relative;
        }}
        .program-box li::before {{
            content: "-";
            position: absolute;
            left: 0;
            color: {KEY_ORANGE_COLOR};
            font-weight: bold;
        }}

        .central-hub-box {{
            width: 180px;  /* 크기 증가 */
            height: 180px; /* 크기 증가 */
            background-color: {hub_background_color};
            border: 3px solid {hub_border_color};
            border-radius: 50%; /* 원형 */
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0 auto; /* 가로 중앙 정렬 */
            font-size: 2em; /* "소링아 3기" 텍스트 크기 */
            font-weight: 700; /* Bold */
            color: {hub_text_color};
            text-align: center;
            line-height: 1.2;
            box-shadow: 0 6px 20px rgba(255,112,67,0.25);
            position: relative; /* 화살표가 이 요소까지 닿도록 z-index 관리 */
            z-index: 1;
        }}

        /* 화살표 스타일 */
        .arrow-connector {{
            position: absolute;
            background: linear-gradient(to bottom, {gradient_start_color}, {gradient_end_color});
            z-index: 0; /* 허브 박스보다 뒤에 있도록 */
        }}
        .arrow-connector.arrow-1 {{ /* 왼쪽 박스에서 오는 화살표 */
            width: 6px; height: 120px; /* 길이 조정 필요 */
            right: 10%; top: 110%; /* 박스 하단 중앙에서 시작 */
            transform-origin: top center;
            transform: translateX(10%) rotate(-45deg); /* 각도 조정 */
        }}
        .arrow-connector.arrow-2 {{ /* 가운데 박스에서 오는 화살표 */
            width: 6px; height: 50px; 
            left: 50%; top: 105%;
            transform: translateX(-50%) rotate(0deg); /* 직선 */
        }}
        .arrow-connector.arrow-3 {{ /* 오른쪽 박스에서 오는 화살표 */
            width: 6px; height: 120px; 
            left: 10%; top: 110%;
            transform-origin: top center;
            transform: translateX(-50%) rotate(45deg); /* 각도 조정 */
        }}

        /* 반응형: 작은 화면에서는 상단 박스를 수직으로 쌓기 */
        @media (max-width: 768px) {{
            .top-boxes-row {{
                flex-direction: column;
                align-items: center;
                gap: 25px; /* 박스 간 세로 간격 */
                margin-bottom: 40px;
            }}
            .program-box {{
                width: 80%; /* 모바일에서 너비 확장 */
                max-width: 350px;
                min-height: auto;
            }}
            /* 모바일에서는 화살표 위치/모양 조정이 매우 복잡하므로 단순화하거나 숨길 수 있음 */
            .arrow-connector {{ display: none; }} /* 모바일에서는 화살표 숨김 */
            .central-hub-box {{ width: 150px; height: 150px; font-size: 1.7em; }}
        }}

    </style>
    <div class="diagram-container">
        <div class="top-boxes-row">
            <div class="program-box" style="border-top: 5px solid {gradient_start_color};">
                <h3>전문 컨설턴트의<br>1:1 심화 교육</h3>
                <ul>
                    <li>공공/민간분야 전문가의 맞춤형 멘토링</li><li>기업별 진단을 통한 소셜/비즈니스 KP 설정</li><li>비즈니스 로드맵 설정</li>
                </ul>
                <div class="arrow-connector arrow-1 arrow-head-style"></div>
            </div>
            <div class="program-box" style="border-top: 5px solid {KEY_ORANGE_COLOR};">
                <h3>소셜 링크 아카데미<br>교육 참여</h3>
                <ul>
                    <li>사회 서비스 기업과의 네트워크 확장</li><li>사회 서비스 이해 증진</li><li>혼합금융 및 투자 생태계 교육</li>
                </ul>
                <div class="arrow-connector arrow-2 arrow-head-style"></div>
            </div>
            <div class="program-box" style="border-top: 5px solid {gradient_end_color};">
                <h3>팀 맞춤형 혼합금융<br>컨설팅/연계</h3>
                <ul>
                    <li>TIPS/LIPS 교육</li><li>맞춤형 지원사업 연계</li><li>MYSC 네트워크를 통한 오픈이노베이션 연계</li>
                </ul>
                <div class="arrow-connector arrow-3 arrow-head-style"></div>
            </div>
        </div>
        <div class="central-hub-box">
            소링아<br>3기
        </div>
    </div>
    """
    st.markdown(diagram_html, unsafe_allow_html=True)

# === 섹션 3: 누가 지원할 수 있나요? ===
def display_who_can_apply_section():
    section_html = f"""
    <style>
        #who-can-apply-section {{ 
            background-color: {BACKGROUND_COLOR_SECTION_MEDIUM_GRAY}; padding: 80px 20px; 
            overflow-x: hidden; font-family: 'Pretendard', sans-serif;
        }}
        #who-can-apply-section .content-wrapper {{ max-width: 800px; margin: 0 auto; }}
        #who-can-apply-section .section-main-title-orange {{ font-size: 1.8em; font-weight: 700; color: {KEY_ORANGE_COLOR}; text-align: center; margin-bottom: 10px; }}
        #who-can-apply-section .section-subtitle-emoji {{ font-size: 2.2em; font-weight: 700; color: {TEXT_COLOR_HEADINGS}; text-align: center; margin-bottom: 35px; }}
        #who-can-apply-section .apply-info-card {{ background-color: {CARD_BACKGROUND_COLOR}; text-align: center; padding: 35px 40px; border-radius: 16px; box-shadow: 0 6px 25px rgba(0,0,0,0.07); text-align: left; }}
        #who-can-apply-section .apply-info-card p.apply-details {{ font-size: 1.2em; color: {TEXT_COLOR_BODY}; text-align: center; line-height: 1.8; margin-bottom: 0; }}
        @media (max-width: 992px) {{ #who-can-apply-section .section-main-title-orange {{ font-size: 1.7em; }} #who-can-apply-section .section-subtitle-emoji {{ font-size: 2.0em; }} #who-can-apply-section .apply-info-card p.apply-details {{ font-size: 1.15em; }} }}
        @media (max-width: 768px) {{ #who-can-apply-section {{ padding: 60px 20px; }} #who-can-apply-section .section-main-title-orange {{ font-size: 1.6em; }} #who-can-apply-section .section-subtitle-emoji {{ font-size: 1.8em; margin-bottom: 30px; }} #who-can-apply-section .apply-info-card {{ padding: 30px 25px; }} #who-can-apply-section .apply-info-card p.apply-details {{ font-size: 1.05em; }} }}
        @media (max-width: 576px) {{ #who-can-apply-section .section-main-title-orange {{ font-size: 1.5em; }} #who-can-apply-section .section-subtitle-emoji {{ font-size: 1.6em; }} #who-can-apply-section .apply-info-card p.apply-details {{ font-size: 1.0em; }} }}
    </style>
    <div id="who-can-apply-section"><div class="content-wrapper"><h2 class="section-main-title-orange">지원대상</h2><h3 class="section-subtitle-emoji">🤔 누가 지원할 수 있나요?</h3><div class="apply-info-card"><p class="apply-details">사회서비스 관련 기술‧제품‧서비스 제공 기업으로 <br> <strong>복지, 보건·의료, 교육, 고용, 주거, 문화, 환경</strong> 등의 분야가 포함되며, <strong> 총 13개 사 </strong>를 선발합니다.</p></div></div></div>"""
    st.markdown(section_html, unsafe_allow_html=True)

# === 섹션 4: 지원 혜택 ===
def display_benefits_section():
    checkmark_color = "#27ae60"
    section_html = f"""
    <style>
        #benefits-section {{ 
            background-color: {BACKGROUND_COLOR_SECTION_WHITE}; padding: 80px 20px; 
            overflow-x: hidden; font-family: 'Pretendard', sans-serif;
        }}
        #benefits-section .content-wrapper {{ max-width: 800px; margin: 0 auto; }}
        #benefits-section .benefits-main-title-orange {{ font-size: 1.8em; font-weight: 700; color: {KEY_ORANGE_COLOR}; text-align: center; margin-bottom: 10px; }}
        #benefits-section .benefits-subtitle {{ font-size: 2.2em; font-weight: 700; color: {TEXT_COLOR_HEADINGS}; text-align: center; margin-bottom: 35px; }}
        #benefits-section .benefits-card {{ background-color: {CARD_BACKGROUND_COLOR}; padding: 35px 40px; border-radius: 16px; box-shadow: 0 10px 35px rgba(0,0,0,0.12); text-align: left; }}
        #benefits-section .benefits-card ul {{ list-style-type: none; padding-left: 0; margin: 0; }}
        #benefits-section .benefits-card li {{ display: flex; align-items: flex-start; font-size: 1.2em; color: {TEXT_COLOR_BODY}; line-height: 1.6; margin-bottom: 15px; }}
        #benefits-section .benefits-card li:last-child {{ margin-bottom: 0; }}
        #benefits-section .benefits-card li::before {{ content: '✓'; color: {checkmark_color}; font-size: 1em; font-weight: bold; margin-right: 12px; line-height: inherit; flex-shrink: 0; }}
        @media (max-width: 992px) {{ #benefits-section .benefits-main-title-orange {{ font-size: 1.7em; }} #benefits-section .benefits-subtitle {{ font-size: 2.0em; }} #benefits-section .benefits-card li {{ font-size: 1.15em; }} }}
        @media (max-width: 768px) {{ #benefits-section {{ padding: 60px 20px; }} #benefits-section .benefits-main-title-orange {{ font-size: 1.6em; }} #benefits-section .benefits-subtitle {{ font-size: 1.8em; margin-bottom: 30px; }} #benefits-section .benefits-card {{ padding: 30px 25px; }} #benefits-section .benefits-card li {{ font-size: 1.05em; margin-bottom: 12px; }} }}
        @media (max-width: 576px) {{ #benefits-section .benefits-main-title-orange {{ font-size: 1.5em; }} #benefits-section .benefits-subtitle {{ font-size: 1.6em; }} #benefits-section .benefits-card li {{ font-size: 1.0em; }} }}
    </style>
    <div id="benefits-section"><div class="content-wrapper"><h2 class="benefits-main-title-orange">지원 혜택</h2><h3 class="benefits-subtitle">✨ 소링아 3기에 참여하면 어떤 혜택이 있나요?</h3><div class="benefits-card"><ul><li>MYSC 2억 직접투자 검토 </li><li>전문 컨설턴트의 1:1 심화 교육</li><li>소셜링크아카데미 교육 참여</li></ul></div></div></div>"""
    st.markdown(section_html, unsafe_allow_html=True)

# === 섹션 5: 프로그램 진행 내용 ===
def display_program_flow_section():
    css_styles_html = f"""
    <style>
        /* Pretendard 폰트는 inject_custom_elements에서 로드됨 */
        @keyframes popInEffect {{ 0% {{ opacity: 0; transform: translateY(30px) scale(0.95); }} 70% {{ opacity: 1; transform: translateY(-5px) scale(1.02); }} 100% {{ opacity: 1; transform: translateY(0) scale(1); }} }}
        
        .program-flow-section-container {{ 
            background-color: {BACKGROUND_COLOR_SECTION_WHITE}; padding: 75px 20px; 
            font-family: 'Pretendard', sans-serif; /* 명시적 폰트 설정 */
        }}
        .program-flow-content-wrapper {{ max-width: 820px; margin: 0 auto; }}
        .program-flow-main-title {{ font-size: 1.8em; font-weight: 700; color: {KEY_ORANGE_COLOR}; text-align: center; margin-bottom: 10px; }}
        .program-flow-main-subtitle {{ font-size: 2.2em; font-weight: 700; color: {TEXT_COLOR_HEADINGS}; text-align: center; margin-bottom: 45px; }}
        
        .program-group-title-container {{ text-align: center; margin-bottom: 15px; }}
        .program-group-title {{ font-size: 1.65em; font-weight: 600; color: {TEXT_COLOR_BODY_STRONG}; margin-top: 50px; margin-bottom: 28px; text-align: center; border-bottom: 2px solid {KEY_ORANGE_COLOR}; padding-bottom: 12px; display: inline-block; }}
        .program-group-title-container:first-child .program-group-title {{ margin-top: 0; }}
        
        .activity-card {{
            background-color: {CARD_BACKGROUND_COLOR}; border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.06); margin-bottom: 20px;
            padding: 22px 28px; border-left: 5px solid {KEY_ORANGE_COLOR};
            opacity: 0; animation-name: popInEffect; animation-duration: 0.6s;
            animation-timing-function: ease-out; animation-fill-mode: forwards;
            outline: 0px solid transparent; outline-offset: 0px; 
            transition: background-color 0.3s ease-in-out, border-left-color 0.3s ease-in-out, 
                        box-shadow 0.3s ease-in-out, outline-width 0.3s ease-in-out, 
                        outline-color 0.3s ease-in-out;
            cursor: default; 
        }}
        .activity-card:hover {{
            background-color: {KEY_ORANGE_COLOR}; border-left-color: {CARD_BACKGROUND_COLOR}; 
            box-shadow: 0px 8px 20px rgba(255, 112, 67, 0.35); 
            outline-width: 3px; outline-color: #ffffff; 
        }}
        .activity-card h4 {{ font-size: 1.45em; font-weight: 600; color: {KEY_ORANGE_COLOR}; margin-top: 0; margin-bottom: 12px; transition: color 0.3s ease-in-out; }}
        .activity-card ul {{ list-style-type: none; padding-left: 0; margin: 0; }}
        .activity-card li {{ font-size: 1.05em; color: {TEXT_COLOR_CAPTION}; margin-bottom: 10px; line-height: 1.7; position: relative; padding-left: 22px; transition: color 0.3s ease-in-out; }}
        .activity-card li:last-child {{ margin-bottom: 0; }}
        .activity-card li strong {{ font-weight: 600; color: {TEXT_COLOR_BODY}; transition: color 0.3s ease-in-out; }}
        .activity-card li::before {{ content: "•"; color: {KEY_ORANGE_COLOR}; font-weight: 700; display: inline-block; position: absolute; left: 0; top: 1px; font-size: 1.1em; line-height: 1; transition: color 0.3s ease-in-out; }}
        .placeholder-text {{ color: {TEXT_COLOR_PLACEHOLDER}; font-style: normal; transition: color 0.3s ease-in-out; }}
        .activity-card:hover h4, .activity-card:hover li, .activity-card:hover li strong,
        .activity-card:hover li .placeholder-text, .activity-card:hover li::before {{ color: #ffffff; }}
        
        @media (max-width: 768px) {{
            .program-flow-main-title {{ font-size: 1.7em; }} .program-flow-main-subtitle {{ font-size: 2.0em; }}
            .program-group-title {{ font-size: 1.4em; margin-top: 40px; margin-bottom: 20px; }}
            .activity-card h4 {{ font-size: 1.3em; }} .activity-card li {{ font-size: 1.0em; }}
        }}
    </style>"""
    st.markdown(css_styles_html, unsafe_allow_html=True)
    
    program_elements = [
        {"group_title": "📚 기본 교육", "activities": [
            {"title": "스테이지 1: 법률 및 기본 역량 강화", "items": ["사회서비스의 이해: <span class='placeholder-text'>사회 서비스의 의미와 생태계 소개</span>", "인사노무: 채용 및 취업 규칙/표준 근로계약서 기반의 근로계약서 작성 강의 진행", "법률 교육: 투자 핵심 용어, 유형 계약 시 주의사항 등"]},
            {"title": "스테이지 2: 성장 및 가치 측정", "items": ["AI 기반 임팩트 측정: 사회서비스 기업 대표님으로부터 직접 듣는 정성 지표 수집 및 데이터 자동화 이를 통한 알맞은 파트너십 구축 전략", "AI 인사이트: 글로벌 AI 트렌드와 사회서비스 기업의 향후 AI/DT 전략", "홍보 마케팅: 사회서비스 기업 맞춤형 홍보 및 마케팅 전략"]},
            {"title": "스테이지 3: 투자 유치 및 금융 설계", "items": ["IR 스토리텔링: <span class='placeholder-text'>스토리 기반의 IR 피치덱 구성과 피칭 전략 강의</span>", "투자 생태계 이해: <span class='placeholder-text'> 국내 AC/VC/PE 등 벤처 투자와 관련된 생태계 전반 강의와 형태에 따른 투자 유치 가이드</span>", "혼합금융: <span class='placeholder-text'>MYSC의 실전적인 사례를 통해 알아보는 TIPS/LIPS/지원금을 통해 자본조달 전략 수립 강의</span>"]}
        ]},
        {"group_title": "👊 심화 교육", "activities": [
            {"title": "팀파트너 매칭", "items": ["<strong>팀 파트너:</strong>공공/민간에서 풍부한 경험을 보유한 MYSC 컨설턴트가 진단 미팅과 격월 기업의 전반적인 현황을 파악하고 성장을 지원하는 멘토링을 진행합니다."]},
            {"title": "사업 스케일업", "items": ["<strong>내부 컨설팅:</strong>오픈이노베이션/브랜딩/임팩트 진단/조직문화 및 HR/투자/TIPS/LIPS 등 기업의 스케일업에 꼭 필요한 아젠다에 기업 진단에 맞춰 심층 교육을 진행합니다."]},
            {"title": "파트너 전문 교육", "items": ["<strong>외부 파트너 컨설팅:</strong>특허/법률/노무 등 외부 전문가의 도움이 필요한 경우 스타트업을 다년간 MYSC와 함께 육성해온 파트너와의 심층적인 자문을 제공합니다.(파트너 기관: 특허법인 도담, 법무법인 디엘지, 동화 노무법인인)"]}
        ]},
        {"group_title": "🤝 네트워킹 및 성과공유", "activities": [
            {"title": "발대식", "items": ["아카데미의 첫 시작으로 중앙사회서비스원 소개 및 프로그램 소개, 자가진단 작성 및 선배 기업가 강연,참여 기업 간 네트워킹 진행(6월 중)"]},
            {"title": "동반성장 워크숍", "items": ["우리 기업의 사회문제에 집중하고 다른 기업과 함께 고민할 수 있는 비주얼 띵킹 등이 적용된 워크숍으로 선배 사회서비스 기업가 초청 강연, 네트워킹으로 구성(10월 중)"]},
            {"title": "성과공유회 (데모데이)", "items": ["한 해의 성과를 공유하는 자리로 수료식, 참여 기업 최종 성과 발표, 투자자 및 유관기관 네트워킹(11월 중)"]}
        ]}
    ]
    
    st.markdown('<div id="section-program" class="program-flow-section-container"><div class="program-flow-content-wrapper">', unsafe_allow_html=True)
    st.markdown(f'<h2 class="program-flow-main-title">프로그램 진행 내용</h2>', unsafe_allow_html=True)
    st.markdown(f'<h3 class="program-flow-main-subtitle">✨ 어떤 교육과 프로그램이 있나요?</h3>', unsafe_allow_html=True)
    
    animation_delay_counter = 0
    for group in program_elements:
        st.markdown(f'<div class="program-group-title-container"><h3 class="program-group-title">{group["group_title"]}</h3></div>', unsafe_allow_html=True)
        for activity in group["activities"]:
            items_html_parts = []
            for item_text in activity["items"]:
                parts = item_text.split(":", 1)
                if len(parts) == 2:
                    title_part = parts[0].strip()
                    description_part = parts[1].strip()
                    item_html = f"<li><strong>{title_part}</strong>: {description_part}</li>"
                else:
                    item_html = f"<li>{item_text}</li>"
                items_html_parts.append(item_html)
            
            items_html_result = "".join(items_html_parts)
            current_delay = animation_delay_counter * 0.12 
            
            activity_card_html = f"""
            <div class="activity-card" style="animation-delay: {current_delay}s;">
                <h4>{activity['title']}</h4>
                <ul>{items_html_result}</ul>
            </div>"""
            st.markdown(activity_card_html, unsafe_allow_html=True)
            animation_delay_counter += 1
            
    st.markdown('</div></div>', unsafe_allow_html=True)

   



# === 섹션 7: 접수 방법 ===
def display_application_method_text():
    section_style = f"""
    <style>
        #application-method-section {{ 
            padding: 80px 20px; background-color: {BACKGROUND_COLOR_SECTION_WHITE};
            font-family: 'Pretendard', sans-serif;
        }}
        #application-method-section .content-wrapper {{ max-width: 800px; margin: 0 auto; }}
        #application-method-section .main-title-orange {{ font-size: 1.8em; font-weight: 700; color: {KEY_ORANGE_COLOR}; text-align: center; margin-bottom: 10px; }}
        #application-method-section .subtitle-emoji {{ font-size: 2.2em; font-weight: 700; color: {TEXT_COLOR_HEADINGS}; text-align: center; margin-bottom: 35px; }}
        #application-method-section .info-card {{ background-color: {CARD_BACKGROUND_COLOR}; padding: 30px 35px; border-radius: 16px; box-shadow: 0 8px 25px rgba(0,0,0,0.08); text-align: left; }}
        #application-method-section .info-card p {{ font-size: 1.1em; color: {TEXT_COLOR_BODY}; line-height: 1.75; margin-bottom: 18px; }}
        #application-method-section .info-card p:last-child {{ margin-bottom: 0; }}
        #application-method-section .info-card strong {{ color: {TEXT_COLOR_BODY_STRONG}; }}
        #application-method-section .info-card em {{ font-style: normal; color: {TEXT_COLOR_CAPTION}; font-size: 0.95em; display: inline-block; margin-top: 4px;}}
        #application-method-section .info-card .submission-note {{ color: {TEXT_COLOR_PLACEHOLDER}; font-size: 0.9em; display: block; margin-top: 10px; }}
         @media (max-width: 768px) {{ #application-method-section .main-title-orange {{ font-size: 1.7em; }} #application-method-section .subtitle-emoji {{ font-size: 2.0em; }} #application-method-section .info-card p {{ font-size: 1.05em; }} }}
    </style>"""
    st.markdown(section_style, unsafe_allow_html=True)
    content_html = f"""
    <div id="application-method-section"><div class="content-wrapper">
            <h2 class="main-title-orange">접수 방법</h2><h3 class="subtitle-emoji">🤔 어떻게 지원하면 될까요?</h3>
            <div class="info-card">
                <p>- 화면 하단의 <strong>'📝 지원하기'</strong> 버튼을 클릭하여 온라인 설문 링크에 접속합니다.<br>- 해당 링크에서 신청 양식을 다운로드 받아 작성 후, 기타 제출 서류와 함께 업로드해 주십시오.</p>
            </div></div></div>"""
    st.markdown(content_html, unsafe_allow_html=True)

# === 섹션 8: 문의하기 ===
def display_contact_info():
    contact_email = "social.link.academy@gmail.com"
    section_style = f"""
    <style>
        #contact-info-section {{ 
            padding: 80px 20px; background-color: {BACKGROUND_COLOR_SECTION_LIGHT_GRAY};
            font-family: 'Pretendard', sans-serif;
        }}
        #contact-info-section .content-wrapper {{ max-width: 700px; margin: 0 auto; }}
        #contact-info-section .main-title-orange {{ font-size: 1.8em; font-weight: 700; color: {KEY_ORANGE_COLOR}; text-align: center; margin-bottom: 35px; }}
        .contact-card {{ background-color: {CARD_BACKGROUND_COLOR}; border-radius: 16px; box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.08); padding: 30px 35px; text-align: left; }}
        .contact-card h3 {{ font-size: 1.6em; font-weight: 600; color: {TEXT_COLOR_BODY_STRONG}; margin-top: 0; margin-bottom: 22px; text-align: center; }}
        .contact-card p {{ font-size: 1.15em; color: {TEXT_COLOR_BODY}; line-height: 1.8; margin-bottom: 12px; display: flex; align-items: center; }}
        .contact-card p:last-child {{ margin-bottom: 0; }}
        .contact-card .icon {{ margin-right: 12px; font-size: 1.2em; color: {KEY_ORANGE_COLOR}; width: 22px; text-align:center; }}
        .contact-card strong {{ color: {TEXT_COLOR_BODY_STRONG};}}
        .contact-card a {{ color: {KEY_ORANGE_COLOR}; text-decoration: none; font-weight: 500;}}
        .contact-card a:hover {{ text-decoration: underline; }}
        @media (max-width: 768px) {{ #contact-info-section .main-title-orange {{ font-size: 1.7em; margin-bottom:30px; }} .contact-card h3 {{ font-size: 1.5em; }} .contact-card p {{ font-size: 1.1em; }} }}
    </style>"""
    st.markdown(section_style, unsafe_allow_html=True)
    content_html = f"""
    <div id="contact-info-section"><div class="content-wrapper">
            <h2 class="main-title-orange">문의하기</h2>
            <div class="contact-card">
                <h3>프로그램 운영 사무국 (MYSC)</h3>
                <p><span class="icon">✉️</span><strong>이메일:</strong> <a href="mailto:{contact_email}">{contact_email}</a></p>
                <p><span class="icon">📞</span><strong>연락처:</strong> 02-532-1110 </p>
            </div></div></div>"""
    st.markdown(content_html, unsafe_allow_html=True)
    

# --- 전역 상수 (코드 상단에 이미 정의되어 있다고 가정합니다) ---
# 이 함수 내에서 직접 사용되는 상수들만 아래에 명시하거나, 
# 실제 앱에서는 전역으로 선언된 값을 참조합니다.
KEY_ORANGE_COLOR = "#FF7043"
TEXT_COLOR_HEADINGS = "#1A1B1E"
TEXT_COLOR_BODY_STRONG = "#2c3e50"
TEXT_COLOR_BODY = "#333D4B"
TEXT_COLOR_CAPTION = "#555555"
CARD_BACKGROUND_COLOR = "#ffffff"
BACKGROUND_COLOR_SECTION_WHITE = "#ffffff"

# (image_to_data_uri 함수는 사용자 제공 코드에 이미 있다고 가정합니다.)
# def image_to_data_uri(file_path_str): ...

def display_key_achievements_section():
    # CSS 변수 (실제 값으로 대체되어야 함)
    BACKGROUND_COLOR_SECTION_WHITE = "#ffffff"  # 예시: 흰색 배경
    TEXT_COLOR_HEADINGS = "#2c3e50"             # 예시: 어두운 회색 제목
    CARD_BACKGROUND_COLOR = "#ffffff"           # 예시: 카드 배경 흰색
    TEXT_COLOR_BODY_STRONG = "#34495e"          # 예시: 약간 어두운 회색 본문 강조
    TEXT_COLOR_BODY = "#555555"                 # 예시: 일반 회색 본문
    KEY_ORANGE_COLOR = "#FF7043"              # 예시: 주황색 강조
    TEXT_COLOR_CAPTION = "#7f8c8d"              # 예시: 연한 회색 캡션

    section_html_content = f"""
    <style>
        #key-achievements-section-mvp {{
            background-color: {BACKGROUND_COLOR_SECTION_WHITE};
            padding: 60px 20px;
            text-align: center;
            font-family: 'Pretendard', sans-serif;
        }}
        #key-achievements-section-mvp .content-wrapper-mvp {{
            max-width: 920px;
            margin: 0 auto;
        }}
        #key-achievements-section-mvp .section-title-mvp {{
            font-size: 2.1em;
            font-weight: 700;
            color: {TEXT_COLOR_HEADINGS};
            margin-bottom: 40px;
        }}
        .achievements-grid-mvp {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 25px;
        }}
        .achievement-item-mvp {{
            background-color: {CARD_BACKGROUND_COLOR};
            border: 1px solid #f0f0f0;
            border-radius: 12px;
            padding: 20px 15px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            cursor: pointer; /* 인터랙션 암시 커서 추가 */
            transition: transform 0.3s ease-in-out,
                        background-color 0.3s ease-in-out,
                        border-color 0.3s ease-in-out,
                        box-shadow 0.3s ease-in-out; /* 부드러운 전환 효과 */
        }}
        .achievement-item-mvp:hover {{
            background-color: {KEY_ORANGE_COLOR}; /* 호버 시 배경색 변경 */
            transform: scale(1.05); /* 호버 시 크기 확대 */
            border-color: {KEY_ORANGE_COLOR}; /* 호버 시 테두리색 변경 */
            box-shadow: 0 8px 20px rgba(0,0,0,0.1); /* 호버 시 그림자 강화 */
        }}
        .achievement-item-mvp .icon-mvp {{
            font-size: 2.6em;
            display: block;
            margin-bottom: 15px;
            line-height: 1;
            transition: color 0.3s ease-in-out; /* 아이콘 색상 전환 */
        }}
        .achievement-item-mvp:hover .icon-mvp {{
            color: #ffffff; /* 호버 시 아이콘 색상 변경 (필요시) */
        }}
        .achievement-item-mvp h4 {{
            font-size: 1.15em;
            font-weight: 600;
            color: {TEXT_COLOR_BODY_STRONG};
            margin-top: 0;
            margin-bottom: 6px;
            line-height: 1.4;
            transition: color 0.3s ease-in-out; /* 텍스트 색상 전환 */
        }}
        .achievement-item-mvp:hover h4 {{
            color: #ffffff; /* 호버 시 제목 텍스트 흰색으로 */
        }}
        .achievement-item-mvp .stat-mvp {{
            font-size: 1.0em;
            font-weight: 500;
            color: {TEXT_COLOR_BODY};
            margin-bottom: 4px;
            line-height: 1.5;
            transition: color 0.3s ease-in-out; /* 텍스트 색상 전환 */
        }}
        .achievement-item-mvp:hover .stat-mvp {{
            color: #ffffff; /* 호버 시 통계 텍스트 흰색으로 */
        }}
        .achievement-item-mvp .stat-mvp .stat-highlight {{
            color: {KEY_ORANGE_COLOR};
            font-weight: 700;
            transition: color 0.3s ease-in-out; /* 텍스트 색상 전환 */
        }}
        .achievement-item-mvp:hover .stat-mvp .stat-highlight {{
            color: #ffffff; /* 호버 시 강조 텍스트도 흰색으로 (또는 더 밝은 주황 계열) */
        }}
        .achievement-item-mvp .sub-detail-mvp {{
            font-size: 0.8em;
            color: {TEXT_COLOR_CAPTION};
            line-height: 1.4;
            transition: color 0.3s ease-in-out; /* 텍스트 색상 전환 */
        }}
        .achievement-item-mvp:hover .sub-detail-mvp {{
            color: #f0f0f0; /* 호버 시 부가설명 텍스트 약간 밝은 회색 (흰색도 가능) */
        }}

        @media (max-width: 992px) {{
            .achievements-grid-mvp {{
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
            }}
            #key-achievements-section-mvp .section-title-mvp {{ font-size: 2.0em; margin-bottom: 35px; }}
            .achievement-item-mvp .icon-mvp {{ font-size: 2.4em; }}
            .achievement-item-mvp h4 {{ font-size: 1.1em; }}
            .achievement-item-mvp .stat-mvp {{ font-size: 0.95em; }}
        }}
        @media (max-width: 576px) {{
            .achievements-grid-mvp {{
                grid-template-columns: 1fr;
                gap: 18px;
            }}
            #key-achievements-section-mvp {{ padding: 50px 15px; }}
            #key-achievements-section-mvp .section-title-mvp {{ font-size: 1.8em; margin-bottom: 30px; }}
            .achievement-item-mvp .icon-mvp {{ font-size: 2.2em; }}
            .achievement-item-mvp h4 {{ font-size: 1.05em; }}
            .achievement-item-mvp .stat-mvp {{ font-size: 0.9em; }}
            .achievement-item-mvp .sub-detail-mvp {{ font-size: 0.75em; }}
        }}
    </style>
    <div id="key-achievements-section-mvp">
        <div class="content-wrapper-mvp">
            <h2 class="section-title-mvp">주요 성과 (2023-2024)</h2>
            <div class="achievements-grid-mvp">
                <div class="achievement-item-mvp">
                    <span class="icon-mvp">🎓</span>
                    <h4>소셜 링크 아카데미</h4>
                    <p class="stat-mvp"> <strong class='stat-highlight'>1, 2기</strong> 운영</p>
                </div>
                <div class="achievement-item-mvp">
                    <span class="icon-mvp">🏢</span>
                    <h4>함께한 기업</h4>
                    <p class="stat-mvp">총 <strong class='stat-highlight'>124</strong>개社</p>
                    <p class="sub-detail-mvp">(중복 제외)</p>
                </div>
                <div class="achievement-item-mvp">
                    <span class="icon-mvp">👥</span>
                    <h4>함께한 사람들</h4>
                    <p class="stat-mvp"><strong class='stat-highlight'>500</strong>여 명</p>
                </div>
                <div class="achievement-item-mvp">
                    <span class="icon-mvp">🤝</span>
                    <h4>투자 교류회</h4>
                    <p class="stat-mvp">총 <strong class='stat-highlight'>9</strong>회 운영</p>
                </div>
                <div class="achievement-item-mvp">
                    <span class="icon-mvp">₩</span>
                    <h4>투자 금액</h4>
                    <p class="stat-mvp">총 <strong class='stat-highlight'>145.25</strong>억 원</p>
                </div>
                <div class="achievement-item-mvp">
                    <span class="icon-mvp">📈</span>
                    <h4>참여 투자사</h4>
                    <p class="stat-mvp"><strong class='stat-highlight'>66</strong>개사,</p>
                    <p class="sub-detail-mvp">소속 VC 약 120명 참여</p>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(section_html_content, unsafe_allow_html=True) # Streamlit 등에 출력 시

# ===============================================
# === Streamlit 앱 메인 실행 로직 (호출 순서) ===
# ===============================================
def main():
    inject_custom_elements(GOOGLE_FORM_URL) 
    display_hero_banner()
    display_post_hero_section() # 디자인 개선된 버전 호출
    display_who_can_apply_section() 
    display_key_achievements_section()
    display_benefits_section()      
    display_program_diagram()
    display_program_flow_section() 
    
    
    hr_style = "border:none; border-top:1px solid #eee; margin: 60px auto; width: 80%; max-width: 900px;"
    
    st.markdown(f"<hr style='{hr_style}'>", unsafe_allow_html=True)
    display_application_method_text() 
    st.markdown(f"<hr style='{hr_style}'>", unsafe_allow_html=True)
    display_contact_info() 
    st.markdown(f"<hr style='{hr_style}'>", unsafe_allow_html=True)

    footer_html = f"""
    <style>
        .footer-caption {{ 
            text-align: center; font-size: 0.9em; color: #888888; 
            padding: 25px 0; border-top: 1px solid #eaeaea; margin-top: 0px;
            font-family: 'Pretendard', sans-serif; /* 푸터에도 폰트 적용 */
        }}
        .footer-caption strong {{ color: #666666; }}
    </style>
    <div class="footer-caption">
        © 2025 중앙사회서비스원 & MYSC . All rights reserved. &nbsp;&nbsp;&nbsp;&nbsp;
    </div>"""
    st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
