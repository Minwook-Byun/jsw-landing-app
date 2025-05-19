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
    <div id="hero-banner"><div class="hero-text-container"><div class="hero-main-text">연결을 통해 확장을 꿈꾸는<br>국내 최초 사회서비스 전문 액셀러레이팅 3기</div></div></div>"""
    st.markdown(hero_html, unsafe_allow_html=True)

# === 섹션 2: "막막했던 투자유치..." (디자인 개선) ===
def display_post_hero_section():
    program_name = "소링아 3기"
    base_text_start = "는 사회서비스 분야 기업의 투자 유치 역량을 강화하고, <br> 실질적인 투자 연계 기회를 제공하여 사회서비스 시장의 지속 가능한 성장을 지원합니다."
    # TEXT_COLOR_BODY_FOR_P는 이 섹션의 p 태그에만 특별히 사용된 #34495e 값입니다.
    TEXT_COLOR_BODY_FOR_P = "#34495e" 

    section_html = f"""
    <style>
        #post-hero-section {{
            background-color: {BACKGROUND_COLOR_SECTION_LIGHT_GRAY};
            padding: 90px 25px; 
            text-align: center;
            margin-top: 0; 
            font-family: 'Pretendard', sans-serif; /* 폰트 상속 또는 명시적 설정 */
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
            font-size: 2.5em; 
            font-weight: 700;
            color: {TEXT_COLOR_BODY_STRONG}; 
            margin-bottom: 30px; 
            line-height: 1.45; 
        }}
        #post-hero-section p.subtitle-text {{
            font-size: 1.28em; 
            color: {TEXT_COLOR_BODY_FOR_P}; /* 이 섹션 특정 p 태그 색상 사용 */
            line-height: 1.85; 
            margin: 0 auto;
            max-width: 780px; 
        }}
        #post-hero-section p.subtitle-text .highlight-program {{
            color: {KEY_ORANGE_COLOR};
            font-weight: 600; 
        }}

        @media (max-width: 992px) {{
            #post-hero-section h2 {{ font-size: 2.2em; }}
            #post-hero-section p.subtitle-text {{ font-size: 1.2em; }}
            #post-hero-section .section-icon {{ font-size: 2.6em; }}
        }}
        @media (max-width: 768px) {{
            #post-hero-section {{ padding: 70px 20px; }}
            #post-hero-section h2 {{ font-size: 2.0em; margin-bottom: 25px; }}
            #post-hero-section p.subtitle-text {{ font-size: 1.1em; }}
            #post-hero-section .section-icon {{ font-size: 2.4em; margin-bottom: 15px; }}
        }}
        @media (max-width: 576px) {{
            #post-hero-section h2 {{ font-size: 1.8em; }}
            #post-hero-section p.subtitle-text {{ font-size: 1.0em; }}
            #post-hero-section .section-icon {{ font-size: 2.2em; }}
        }}
    </style>
    <div id="post-hero-section">
        <div class="content-wrapper">
            <span class="section-icon">💡</span>
            <h2>막막했던 투자 유치 이제 걱정하지마세요!</h2>
            <p class="subtitle-text">
                <span class="highlight-program">{program_name}</span>{base_text_start}
            </p>
        </div>
    </div>
    """
    st.markdown(section_html, unsafe_allow_html=True)

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
    <div id="benefits-section"><div class="content-wrapper"><h2 class="benefits-main-title-orange">지원 혜택</h2><h3 class="benefits-subtitle">✨ 소링아 3기에 참여하면 어떤 혜택이 있나요?</h3><div class="benefits-card"><ul><li>소셜링크아카데미 교육 참여</li><li>우수기업에게 MYSC 직접 투자 2억원 이상 진행</li><li>TIPS/LIPS 추천 검토</li></ul></div></div></div>"""
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
        {"group_title": "🤝 네트워킹 및 성과공유", "activities": [
            {"title": "발대식식", "items": ["아카데미 시작, 오리엔테이션 및 참여 기업 간 네트워킹 세션(6월 중)"]},
            {"title": "동반성장 워크숍", "items": ["선배 사회서비스 기업가 초청 강연, 경험 공유 및 그룹 워크숍(10월 중)"]},
            {"title": "성과공유회 (데모데이)", "items": ["프로그램 참여 기업 최종 성과 발표, 투자자 및 관계자 초청, 네트워킹 기회 제공, 우수팀 시상(11월 중)"]}
        ]}
    ]
    
    st.markdown('<div id="section-program" class="program-flow-section-container"><div class="program-flow-content-wrapper">', unsafe_allow_html=True)
    st.markdown(f'<h2 class="program-flow-main-title">프로그램 진행 내용</h2>', unsafe_allow_html=True)
    st.markdown(f'<h3 class="program-flow-main-subtitle">✨ 어떤 교육과 활동이 있나요?</h3>', unsafe_allow_html=True)
    
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

# ===============================================
# === Streamlit 앱 메인 실행 로직 (호출 순서) ===
# ===============================================
def main():
    inject_custom_elements(GOOGLE_FORM_URL) 
    display_hero_banner()
    display_post_hero_section() # 디자인 개선된 버전 호출
    display_who_can_apply_section() 
    display_benefits_section()      
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
        © 2025 MYSC & 중앙사회서비스원. All rights reserved. &nbsp;&nbsp;&nbsp;&nbsp;
        <strong>주관:</strong> 중앙사회서비스원 &nbsp;|&nbsp; <strong>운영:</strong> MYSC (주식회사 엠와이소셜컴퍼니)
    </div>"""
    st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
