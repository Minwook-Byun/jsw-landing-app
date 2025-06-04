import streamlit as st
import base64
from pathlib import Path
import sqlite3 # SQLite 사용
import json    # 상세 정보 저장을 위해
from datetime import datetime # 타임스탬프 기록을 위해 (선택적, DB에서 자동 생성 가능)
from streamlit.components.v1 import html as st_html # 이름 충돌 방지 및 JS 실행


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
TEXT_COLOR_HEADINGS = "#1A1B1E"
HOVER_TEXT_COLOR_WHITE = "#FFFFFF"
GRADIENT_START_COLOR = "#FFA07A"
GRADIENT_END_COLOR = KEY_ORANGE_COLOR
# APPLICATION_FORM_DOWNLOAD_URL은 display_application_method_text 함수 내부에서 직접 사용되도록 수정됨

matomo_tracking_code = """
<script>
  var _paq = window._paq = window._paq || [];
  /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  (function() {
    var u="https://sociallink3streamlitapp.matomo.cloud/";
    _paq.push(['setTrackerUrl', u+'matomo.php']);
    _paq.push(['setSiteId', '1']);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
    g.async=true; g.src='https://cdn.matomo.cloud/sociallink3streamlitapp.matomo.cloud/matomo.js'; s.parentNode.insertBefore(g,s);
  })();
</script>
"""

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
KEY_LIME_GREEN_COLOR = "#8BC34A"
TEXT_COLOR_BODY = "#333D4B"
TEXT_COLOR_PLACEHOLDER = "#888888"
BACKGROUND_COLOR_SECTION_LIGHT_GRAY = "#f9fafb"
BACKGROUND_COLOR_SECTION_MEDIUM_GRAY = "#f0f2f5"
BACKGROUND_COLOR_SECTION_WHITE = "#ffffff"
HEADER_NAV_TEXT_COLOR = "#4A4A4A"
# HIGHLIGHT_YELLOW_BACKGROUND = "#FFF9C4" # 이전 버전에서 사용, 필요시 재활용
HIGHLIGHT_ORANGE_VERY_LIGHT_BACKGROUND = "#FFF3E0" # 연한 주황색 (KEY_ORANGE_COLOR의 밝은 버전)
TABLE_HEADER_BACKGROUND = "#FAFAFA" # 테이블 헤더 배경색 (연한 회색)
TABLE_BORDER_COLOR = "#E0E0E0" # 테이블 테두리 색상

# === 섹션 0: 고정 헤더 및 FAB (헤더 메뉴 및 앵커 스크롤 수정) ===
def inject_custom_elements(google_form_url_param):
    logo_bogun_filename = "bogun.jpg"
    logo_mysc_filename = "[MYSC]로고_placeholder.png"
    logo_bogun_data_uri = image_to_data_uri(logo_bogun_filename)
    logo_mysc_data_uri = image_to_data_uri(logo_mysc_filename)
    logo_bogun_html = f'<img src="{logo_bogun_data_uri}" alt="보건복지부 로고" class="header-logo logo-bogun">' if logo_bogun_data_uri else '<span class="logo-placeholder">보건복지부</span>'
    logo_mysc_html = f'<img src="{logo_mysc_data_uri}" alt="MYSC 로고" class="header-logo logo-mysc">' if logo_mysc_data_uri else '<span class="logo-placeholder">MYSC</span>'
    
    nav_items_data = [
        {"label": "지원 대상", "id_target": "who-can-apply-section"},
        {"label": "지원 혜택", "id_target": "benefits-section"},
        {"label": "프로그램", "id_target": "section-program"},
        {"label": "접수 방법", "id_target": "application-method-section-final-hc"}, # 평가 기준이 이 섹션으로 통합됨
        {"label": "문의하기", "id_target": "contact-info-section"}
    ]
    nav_html_elements = "".join([f'<a href="#{item["id_target"]}" class="header-nav-item">{item["label"]}</a>' for item in nav_items_data])

    section_ids_for_scroll_margin = [item["id_target"] for item in nav_items_data] + ["post-hero-section", "hero-banner"]
    scroll_margin_selectors = ", ".join([f"#{id_name}" for id_name in section_ids_for_scroll_margin if id_name])




    custom_elements_html = f"""
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css');
        body, .stApp {{ font-family: 'Pretendard', sans-serif !important; }}
        {scroll_margin_selectors} {{ scroll-margin-top: {HEADER_HEIGHT_PX + 20}px !important; }}
        html {{ scroll-behavior: smooth; }}
        .fixed-header {{ position: fixed; top: 0; left: 0; width: 100%; height: {HEADER_HEIGHT_PX}px; background-color: rgba(255, 255, 255, 0.97); padding: 0 25px; border-bottom: 1px solid #EAEAEA; z-index: 1000; display: flex; justify-content: center; align-items: center; box-sizing: border-box; -webkit-backdrop-filter: blur(6px); backdrop-filter: blur(6px); }}
        .header-content {{ display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 1160px; height: 100%; }}
        .header-logo-group {{ display: flex; align-items: center; }}
        .header-logo {{ height: 36px; object-fit: contain; display: block; }}
        .logo-mysc {{ margin-left: 15px; }}
        .logo-placeholder {{ font-weight: bold; color: #333; }}
        .header-nav {{ display: flex; align-items: center; }}
        .header-nav-item {{ text-decoration: none; color: {HEADER_NAV_TEXT_COLOR}; font-size: 15px; font-weight: 500; padding: 8px 14px; margin-left: 10px; border-radius: 6px; transition: color 0.2s ease, background-color 0.2s ease; }}
        .header-nav-item:hover, .header-nav-item:focus {{ color: {KEY_ORANGE_COLOR}; background-color: rgba(255, 112, 67, 0.08); outline: none; }}
        @media (max-width: 992px) {{ .header-nav {{ display: none; }} .header-content {{ justify-content: center; }} }}
        @media (max-width: 480px) {{ .header-logo {{ height: 32px; }} }}
        .fab {{ position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); width: 90%; max-width: 480px; background-color: {KEY_LIME_GREEN_COLOR}; color: white !important; padding: 16px 20px; border-radius: 10px; text-decoration: none; font-size: 1.1em; font-weight: 600; text-align: center; box-shadow: 0 5px 12px rgba(0,0,0,0.18); z-index: 999; transition: background-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease; }}
        .fab:hover {{ background-color: #7CB342; transform: translateX(-50%) translateY(-2px); box-shadow: 0 7px 18px rgba(0,0,0,0.22); }}
        div[data-testid="stAppViewContainer"] > section.main {{ padding-top: {HEADER_HEIGHT_PX + 10}px !important; }}
    </style>
    <div class="fixed-header"> <div class="header-content"> <div class="header-logo-group">{logo_bogun_html}{logo_mysc_html}</div> <nav class="header-nav">{nav_html_elements}</nav> </div> </div>
    <a href="{google_form_url_param}" target="_blank" class="fab">📝 지원하기</a>"""
    st.markdown(custom_elements_html, unsafe_allow_html=True)

# === 섹션 1: 히어로 배너 ===
def display_hero_banner():
    background_image_filename = "bg.jpg"
    image_data_uri = image_to_data_uri(background_image_filename)
    background_style = f"background-image: url(\"{image_data_uri}\");" if image_data_uri else "background-color: #333333;"
    hero_text_top_padding = f"{HEADER_HEIGHT_PX + 80}px"
    hero_html = f"""
    <style>
        #hero-banner {{ min-height: 70vh; height: auto; {background_style} background-size: cover; background-position: center; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: {hero_text_top_padding} 20px 80px 20px; box-sizing: border-box; position: relative; font-family: 'Pretendard', sans-serif; }}
        #hero-banner .hero-text-container {{opacity: 0; animation: fadeInAppearHeroText 1.5s ease-out 0.5s forwards; }}
        #hero-banner .hero-main-text {{ color: white; font-size: 3.8em; font-weight: bold; line-height: 1.4; text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.75); margin: 0; }}
        @keyframes fadeInAppearHeroText {{ 0% {{ opacity: 0; transform: scale(0.95) translateY(20px); }} 100% {{ opacity: 1; transform: scale(1) translateY(0); }} }}
        @media (max-width: 992px) {{ #hero-banner .hero-main-text {{ font-size: 2.8em; }} }}
        @media (max-width: 768px) {{ #hero-banner .hero-main-text {{ font-size: 2.2em; }} }}
        @media (max-width: 576px) {{ #hero-banner .hero-main-text {{ font-size: 1.9em; }} }}
    </style>
    <div id="hero-banner"><div class="hero-text-container"><div class="hero-main-text">연결을 통해 확장을 꿈꾸는<br>국내 최초 사회서비스 전문 액셀러레이팅 <br> 소셜 링크 아카데미 3기</div></div></div>"""
    st.markdown(hero_html, unsafe_allow_html=True)

# === 섹션 2: "막막했던 투자유치..." (디자인 개선) ===
def display_post_hero_section():
    program_name = "소셜 링크 아카데미"
    original_base_text = "는 사회서비스 분야 전문 교육과정입니다. <br> 우수한 기술력과 잠재력을 보유한 사회서비스 기업*을 발굴하고,<br>투자 유치 역량을 강화해 국민의 삶을 HEAL하는 소셜 링커(Social Linker)로의 성장에 함께합니다."
    target_phrase = "국민의 삶을 HEAL하는 소셜 링커(Social Linker)로의 성장"
    highlighted_phrase = f"<span style='color: {KEY_ORANGE_COLOR}; font-weight: 600;'>{target_phrase}</span>"
    modified_base_text = original_base_text.replace(target_phrase, highlighted_phrase)
    legal_note_text = "*사회서비스 기업이란? : 사회서비스 이용 및 이용권 관리에 관한 법률 제2조1항 및 「사회보장기본법 제3조4항」에 근거하여 복지, 보건·의료, 교육, 고용, 주거, 문화, 환경 등의 분야에서 상담, 재활 돌봄, 정보제공, 시설 이용, 역량 개발, 사회참여 등을 통해 국민의 삶의 질 개선·향상을 지원하는 서비스 제공기업"
    TEXT_COLOR_BODY_FOR_P = "#34495e"

    section_html = f"""
    <style>
        #post-hero-section {{ background-color: {BACKGROUND_COLOR_SECTION_LIGHT_GRAY}; padding: 80px 25px; text-align: center; margin-top: 0; font-family: 'Pretendard', sans-serif; }}
        #post-hero-section .content-wrapper {{ max-width: 850px; margin: 0 auto; }} /* 이 섹션은 info 카드가 아니므로 너비 유지 */
        #post-hero-section .section-icon {{ font-size: 2.8em; color: {KEY_ORANGE_COLOR}; margin-bottom: 20px; line-height: 1; display: block; }}
        #post-hero-section h2 {{ font-size: 2.4em; font-weight: 700; color: {TEXT_COLOR_BODY_STRONG}; margin-bottom: 25px; line-height: 1.45; }}
        #post-hero-section p.subtitle-text {{ font-size: 1.25em; color: {TEXT_COLOR_BODY_FOR_P}; line-height: 1.8; margin: 0 auto; max-width: 780px; margin-bottom: 30px; }}
        #post-hero-section p.subtitle-text .highlight-program {{ color: {KEY_ORANGE_COLOR}; font-weight: 600; }}
        #post-hero-section .legal-note {{ font-size: 0.9em; color: {TEXT_COLOR_CAPTION}; line-height: 1.65; margin-top: 20px; max-width: 750px; margin-left: auto; margin-right: auto; text-align: justify; padding: 15px 20px; background-color: rgba(0,0,0,0.03); border-left: 4px solid #dddddd; border-radius: 4px; }}
        @media (max-width: 992px) {{ #post-hero-section h2 {{ font-size: 2.1em; }} #post-hero-section p.subtitle-text {{ font-size: 1.15em; }} #post-hero-section .section-icon {{ font-size: 2.6em; }} #post-hero-section .legal-note {{ font-size: 0.85em; }} }}
        @media (max-width: 768px) {{ #post-hero-section {{ padding: 70px 20px; }} #post-hero-section h2 {{ font-size: 1.9em; margin-bottom: 20px; }} #post-hero-section p.subtitle-text {{ font-size: 1.1em; margin-bottom:25px; }} #post-hero-section .section-icon {{ font-size: 2.4em; margin-bottom: 15px; }} #post-hero-section .legal-note {{ font-size: 0.8em; padding: 12px 15px;}} }}
        @media (max-width: 576px) {{ #post-hero-section h2 {{ font-size: 1.7em; }} #post-hero-section p.subtitle-text {{ font-size: 1.0em; }} #post-hero-section .section-icon {{ font-size: 2.2em; }} #post-hero-section .legal-note {{ font-size: 0.75em; }} }}
    </style>
    <div id="post-hero-section"> <div class="content-wrapper"> <span class="section-icon">💡</span> <h2>국민의 삶을 바꾸는 사회서비스, <br> 우리 함께 시작해볼까요?</h2> <p class="subtitle-text"> <span class="highlight-program">{program_name}</span>{modified_base_text} </p> <p class="legal-note"> {legal_note_text} </p> </div> </div>
    """
    st.markdown(section_html, unsafe_allow_html=True)

# === 섹션 3: 누가 지원할 수 있나요? ===
def display_who_can_apply_section():
    section_html = f"""
    <style>
        #who-can-apply-section {{ background-color: {BACKGROUND_COLOR_SECTION_MEDIUM_GRAY}; padding: 80px 20px; overflow-x: hidden; font-family: 'Pretendard', sans-serif; }}
        #who-can-apply-section .content-wrapper {{ max-width: 1200px; margin: 0 auto; }} /* 너비 수정: 800px -> 1200px */
        #who-can-apply-section .section-main-title-orange {{ font-size: 1.8em; font-weight: 700; color: {KEY_ORANGE_COLOR}; text-align: center; margin-bottom: 10px; }}
        #who-can-apply-section .section-subtitle-emoji {{ font-size: 2.2em; font-weight: 700; color: {TEXT_COLOR_HEADINGS}; text-align: center; margin-bottom: 35px; }}
        #who-can-apply-section .apply-info-card {{ background-color: {CARD_BACKGROUND_COLOR}; text-align: center; padding: 35px 40px; border-radius: 16px; box-shadow: 0 6px 25px rgba(0,0,0,0.07); text-align: left; }}
        #who-can-apply-section .apply-info-card p.apply-details {{ font-size: 1.2em; color: {TEXT_COLOR_BODY}; text-align: center; line-height: 1.8; margin-bottom: 0; }}
        @media (max-width: 1200px) {{ /* 반응형 max-width 조정 */
            #who-can-apply-section .content-wrapper {{ max-width: 95%; }}
        }}
        @media (max-width: 992px) {{ #who-can-apply-section .section-main-title-orange {{ font-size: 1.7em; }} #who-can-apply-section .section-subtitle-emoji {{ font-size: 2.0em; }} #who-can-apply-section .apply-info-card p.apply-details {{ font-size: 1.15em; }} }}
        @media (max-width: 768px) {{ #who-can-apply-section {{ padding: 60px 20px; }} #who-can-apply-section .section-main-title-orange {{ font-size: 1.6em; }} #who-can-apply-section .section-subtitle-emoji {{ font-size: 1.8em; margin-bottom: 30px; }} #who-can-apply-section .apply-info-card {{ padding: 30px 25px; }} #who-can-apply-section .apply-info-card p.apply-details {{ font-size: 1.05em; }} }}
        @media (max-width: 576px) {{ #who-can-apply-section .section-main-title-orange {{ font-size: 1.5em; }} #who-can-apply-section .section-subtitle-emoji {{ font-size: 1.6em; }} #who-can-apply-section .apply-info-card p.apply-details {{ font-size: 1.0em; }} }}
    </style>
    <div id="who-can-apply-section"><div class="content-wrapper"><h2 class="section-main-title-orange">지원대상</h2><h3 class="section-subtitle-emoji">🤔 누가 지원할 수 있나요?</h3><div class="apply-info-card"><p class="apply-details">사회서비스 관련 기술‧제품‧서비스 제공 기업으로 <strong>복지, 보건·의료, 교육, 고용, 주거, 문화, 환경</strong> 등의 분야가 포함되며, <strong> 총 13개 사 </strong>를 선발합니다.</p></div></div></div>"""
    st.markdown(section_html, unsafe_allow_html=True)

# === 섹션 4: 지원 혜택 ===
def display_benefits_section():
    checkmark_color = "#27ae60"
    section_html = f"""
    <style>
        #benefits-section {{ background-color: {BACKGROUND_COLOR_SECTION_WHITE}; padding: 80px 20px; overflow-x: hidden; font-family: 'Pretendard', sans-serif; }}
        #benefits-section .content-wrapper {{ max-width: 1200px; margin: 0 auto; }} /* 너비 수정: 800px -> 1200px */
        #benefits-section .benefits-main-title-orange {{ font-size: 1.8em; font-weight: 700; color: {KEY_ORANGE_COLOR}; text-align: center; margin-bottom: 10px; }}
        #benefits-section .benefits-subtitle {{ font-size: 2.2em; font-weight: 700; color: {TEXT_COLOR_HEADINGS}; text-align: center; margin-bottom: 35px; }}
        #benefits-section .benefits-card {{ background-color: {CARD_BACKGROUND_COLOR}; padding: 35px 40px; border-radius: 16px; box-shadow: 0 10px 35px rgba(0,0,0,0.12); text-align: left; }}
        #benefits-section .benefits-card ul {{ list-style-type: none; padding-left: 0; margin: 0; }}
        #benefits-section .benefits-card li {{ display: flex; align-items: flex-start; font-size: 1.2em; color: {TEXT_COLOR_BODY}; line-height: 1.6; margin-bottom: 15px; }}
        #benefits-section .benefits-card li:last-child {{ margin-bottom: 0; }}
        #benefits-section .benefits-card li::before {{ content: '✓'; color: {checkmark_color}; font-size: 1em; font-weight: bold; margin-right: 12px; line-height: inherit; flex-shrink: 0; }}
        @media (max-width: 1200px) {{ /* 반응형 max-width 조정 */
            #benefits-section .content-wrapper {{ max-width: 95%; }}
        }}
        @media (max-width: 992px) {{ #benefits-section .benefits-main-title-orange {{ font-size: 1.7em; }} #benefits-section .benefits-subtitle {{ font-size: 2.0em; }} #benefits-section .benefits-card li {{ font-size: 1.15em; }} }}
        @media (max-width: 768px) {{ #benefits-section {{ padding: 60px 20px; }} #benefits-section .benefits-main-title-orange {{ font-size: 1.6em; }} #benefits-section .benefits-subtitle {{ font-size: 1.8em; margin-bottom: 30px; }} #benefits-section .benefits-card {{ padding: 30px 25px; }} #benefits-section .benefits-card li {{ font-size: 1.05em; margin-bottom: 12px; }} }}
        @media (max-width: 576px) {{ #benefits-section .benefits-main-title-orange {{ font-size: 1.5em; }} #benefits-section .benefits-subtitle {{ font-size: 1.6em; }} #benefits-section .benefits-card li {{ font-size: 1.0em; }} }}
    </style>
    <div id="benefits-section"><div class="content-wrapper"><h2 class="benefits-main-title-orange">지원 혜택</h2><h3 class="benefits-subtitle">✨ 소링아 3기에 참여하면 어떤 혜택이 있나요?</h3><div class="benefits-card"><ul><li> 우수 기업 MYSC 2억 직접투자 검토</li><li> 팀 파트너의 1:1 심화 교육 진행을 통한 밀착 성장 지원</li><li>소셜 링크 아카데미 참여를 통한 사회서비스 기업과의 네트워크 형성</li></ul></div></div></div>"""
    st.markdown(section_html, unsafe_allow_html=True)

# === 섹션 5: 프로그램 진행 내용 ===
def display_program_flow_section():
    css_styles_html = f"""
    <style>
        @keyframes popInEffect {{ 0% {{ opacity: 0; transform: translateY(30px) scale(0.95); }} 70% {{ opacity: 1; transform: translateY(-5px) scale(1.02); }} 100% {{ opacity: 1; transform: translateY(0) scale(1); }} }}
        .program-flow-section-container {{ background-color: {BACKGROUND_COLOR_SECTION_WHITE}; padding: 75px 20px; font-family: 'Pretendard', sans-serif; }}
        .program-flow-content-wrapper {{ max-width: 1230px; margin: 0 auto; }} /* 너비 수정: 820px -> 1230px */
        .program-flow-main-title {{ font-size: 1.8em; font-weight: 700; color: {KEY_ORANGE_COLOR}; text-align: center; margin-bottom: 10px; }}
        .program-flow-main-subtitle {{ font-size: 2.2em; font-weight: 700; color: {TEXT_COLOR_HEADINGS}; text-align: center; margin-bottom: 45px; }}
        .program-group-title-container {{ text-align: center; margin-bottom: 15px; }}
        .program-group-title {{ font-size: 1.65em; font-weight: 600; color: {TEXT_COLOR_BODY_STRONG}; margin-top: 50px; margin-bottom: 28px; text-align: center; border-bottom: 2px solid {KEY_ORANGE_COLOR}; padding-bottom: 12px; display: inline-block; }}
        .program-group-title-container:first-child .program-group-title {{ margin-top: 0; }}
        .activity-card {{ background-color: {CARD_BACKGROUND_COLOR}; border-radius: 12px; box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.06); margin-bottom: 20px; padding: 22px 28px; border-left: 5px solid {KEY_ORANGE_COLOR}; opacity: 0; animation-name: popInEffect; animation-duration: 0.6s; animation-timing-function: ease-out; animation-fill-mode: forwards; outline: 0px solid transparent; outline-offset: 0px; transition: background-color 0.3s ease-in-out, border-left-color 0.3s ease-in-out, box-shadow 0.3s ease-in-out, outline-width 0.3s ease-in-out, outline-color 0.3s ease-in-out; cursor: default; }}
        .activity-card:hover {{ background-color: {KEY_ORANGE_COLOR}; border-left-color: {CARD_BACKGROUND_COLOR}; box-shadow: 0px 8px 20px rgba(255, 112, 67, 0.35); outline-width: 3px; outline-color: #ffffff; }}
        .activity-card h4 {{ font-size: 1.45em; font-weight: 600; color: {KEY_ORANGE_COLOR}; margin-top: 0; margin-bottom: 12px; transition: color 0.3s ease-in-out; }}
        .activity-card ul {{ list-style-type: none; padding-left: 0; margin: 0; }}
        .activity-card li {{ font-size: 1.05em; color: {TEXT_COLOR_CAPTION}; margin-bottom: 10px; line-height: 1.7; position: relative; padding-left: 22px; transition: color 0.3s ease-in-out; }}
        .activity-card li:last-child {{ margin-bottom: 0; }}
        .activity-card li strong {{ font-weight: 600; color: {TEXT_COLOR_BODY}; transition: color 0.3s ease-in-out; }}
        .activity-card li::before {{ content: "•"; color: {KEY_ORANGE_COLOR}; font-weight: 700; display: inline-block; position: absolute; left: 0; top: 1px; font-size: 1.1em; line-height: 1; transition: color 0.3s ease-in-out; }}
        .placeholder-text {{ color: {TEXT_COLOR_PLACEHOLDER}; font-style: normal; transition: color 0.3s ease-in-out; }}
        .activity-card:hover h4, .activity-card:hover li, .activity-card:hover li strong, .activity-card:hover li .placeholder-text, .activity-card:hover li::before {{ color: #ffffff; }}
        @media (max-width: 1230px) {{ /* 반응형 max-width 조정 */
            .program-flow-content-wrapper {{ max-width: 95%; }}
        }}
        @media (max-width: 768px) {{ .program-flow-main-title {{ font-size: 1.7em; }} .program-flow-main-subtitle {{ font-size: 2.0em; }} .program-group-title {{ font-size: 1.4em; margin-top: 40px; margin-bottom: 20px; }} .activity-card h4 {{ font-size: 1.3em; }} .activity-card li {{ font-size: 1.0em; }} }}
    </style>"""
    st.markdown(css_styles_html, unsafe_allow_html=True)
    
    program_elements = [
        {"group_title": "📚 기본 교육", "activities": [
            {"title": "스테이지 1: 기본 역량 강화", "items": [ "사회서비스의 이해: 사회서비스의 의미와 생태계 소개", "경영진단: MYSC 전문 컨설턴트의 경영진단 및 맞춤형 성장 로드랩 설정", "인사노무: 채용 및 취업 규칙/표준 근로계약서 기반의 근로계약서 작성 강의 진행", "법률 교육: 투자 핵심 용어, 유형 계약 시 주의사항 등" ]},
            {"title": "스테이지 2: 성장 및 가치 측정", "items": [ "AI를 통한 사회적가치 측정: 사회서비스 기업 대표님으로부터 직접 듣는 정성 지표 수집 및 데이터 자동화 이를 통한 알맞은 파트너십 구축 전략", "스타트업 AX전략: 글로벌 AI 트렌드와 사회서비스 기업의 향후 AX 전략", "홍보 마케팅: 사회서비스 기업 맞춤형 홍보 및 마케팅 전략" ]},
            {"title": "스테이지 3: 투자 유치 및 금융 설계", "items": [ "IR 스토리텔링: <span class='placeholder-text'>스토리 기반의 IR 피치덱 구성과 피칭 전략 강의</span>", "투자 생태계 이해: <span class='placeholder-text'> 국내 AC/VC/PE 등 벤처 투자와 관련된 생태계 전반 강의와 형태에 따른 투자 유치 가이드</span>", "혼합금융: <span class='placeholder-text'>MYSC의 실전적인 사례를 통해 알아보는 TIPS/LIPS/지원금을 통해 자본조달 전략 수립 강의</span>", "Closed IR: <span class='placeholder-text'>소링아 참여팀만을 위한 펀드/유관 펀드 심사역과 기업 간 Closed IR 진행</span>" ]}
        ]},
        {"group_title": "👊 심화 교육", "activities": [
            {"title": "팀파트너 매칭", "items": ["<strong>팀 파트너:</strong>공공/민간에서 풍부한 경험을 보유한 MYSC 컨설턴트가 진단 미팅과 격월 기업의 전반적인 현황을 파악하고 성장을 지원하는 멘토링을 진행합니다."]},
            {"title": "사업 스케일업", "items": ["<strong>내부 컨설팅:</strong>오픈이노베이션/브랜딩/임팩트 진단/조직문화 및 HR/투자/TIPS/LIPS 등 기업의 스케일업에 꼭 필요한 아젠다에 기업 진단에 맞춰 심층 교육을 진행합니다."]},
            {"title": "파트너 전문 교육", "items": ["<strong>외부 파트너 컨설팅:</strong>특허/법률/노무 등 외부 전문가의 도움이 필요한 경우 스타트업을 다년간 MYSC와 함께 육성해온 파트너와의 심층적인 자문을 제공합니다.(파트너 기관: 특허법인 도담, 법무법인 디엘지, 동화 노무법인)"]}
        ]},
        {"group_title": "🤝 네트워킹 및 성과공유", "activities": [
            {"title": "발대식", "items": [ " 사회서비스 전문가 강의, 기업 자가진단 작성 및 활용방법, 사회서비스 분야 선배 기업가 강연, 참여 기업 간 네트워킹 진행(6월 중)" ]},
            {"title": "동반성장 워크숍", "items": ["비주얼 띵킹 기반의 1박 2일 워크숍 진행, 사회서비스 기업가 초청 강연, 네트워킹으로 구성(10월 중)"]},
            {"title": "성과공유회 (데모데이)", "items": [ "수료식, 최종 성과 발표, 사회서비스 유관 펀드 보유 투자자와의 밋업, 유관기관 네트워킹(11월 중)" ]}
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

def display_application_method_text():
    참가신청서개인정보동의서 = "https://drive.google.com/uc?export=download&id=1Rf2YMEwUTzgiVTqTzlHJzhzcIduK9Xix"
    사업계획서 ="https://drive.google.com/uc?export=download&id=1JWATxbrHLgDre5EOPtH-vGOuBPGbpwG9"

    # 여기에 모든 색상 및 스타일 관련 변수가 정의되어 있다고 가정합니다.
    BACKGROUND_COLOR_SECTION_WHITE = "#FFFFFF"
    KEY_ORANGE_COLOR = "#FFA500"
    TEXT_COLOR_HEADINGS = "#333333"
    TEXT_COLOR_BODY = "#555555"
    TEXT_COLOR_BODY_STRONG = "#000000"
    CARD_BACKGROUND_COLOR = "#F9F9F9"
    TABLE_BORDER_COLOR = "#DDDDDD"
    TABLE_HEADER_BACKGROUND = "#EEEEEE"
    HIGHLIGHT_ORANGE_VERY_LIGHT_BACKGROUND = "#FFF3E0" # '구분' 셀 배경색
    HIGHLIGHT_ORANGE_EXTREMELY_LIGHT_BACKGROUND = "#FFF9F0" # '주요 항목' 셀 배경색

    html_content = f"""
    <style>
        #application-method-section-final-hc {{ padding: 80px 20px; background-color: {BACKGROUND_COLOR_SECTION_WHITE}; font-family: 'Pretendard', sans-serif; }}
        #application-method-section-final-hc .content-wrapper {{ max-width: 1200px; margin: 0 auto; }}
        #application-method-section-final-hc .main-title-orange {{ font-size: 1.8em; font-weight: 700; color: {KEY_ORANGE_COLOR}; text-align: center; margin-bottom: 10px; }}
        #application-method-section-final-hc .subtitle-emoji {{ font-size: 2.2em; font-weight: 700; color: {TEXT_COLOR_HEADINGS}; text-align: center; margin-bottom: 35px; }}
        #application-method-section-final-hc .info-card {{ background-color: {CARD_BACKGROUND_COLOR}; padding: 30px 35px; border-radius: 16px; box-shadow: 0 8px 25px rgba(0,0,0,0.08); text-align: left; }}
        #application-method-section-final-hc .info-card p.application-guide {{ font-size: 1.1em; color: {TEXT_COLOR_BODY}; line-height: 1.75; margin-bottom: 30px; }}
        #application-method-section-final-hc .info-card strong {{ color: {TEXT_COLOR_BODY_STRONG}; }}

        #application-method-section-final-hc .criteria-table-title {{
            font-size: 1.3em; font-weight: 600; color: {TEXT_COLOR_BODY_STRONG}; text-align: center; margin-top: 10px; margin-bottom: 20px;
        }}
        #application-method-section-final-hc .criteria-table-container {{
            overflow-x: auto; margin-bottom: 30px; border: 1px solid {TABLE_BORDER_COLOR}; border-radius: 8px;
        }}
        #application-method-section-final-hc .criteria-table {{
            width: 100%; border-collapse: collapse; font-size: 0.9em; color: {TEXT_COLOR_BODY};
        }}
        /* 기본 td 정렬은 왼쪽 */
        #application-method-section-final-hc .criteria-table th,
        #application-method-section-final-hc .criteria-table td {{
            border: 1px solid {TABLE_BORDER_COLOR}; padding: 10px; text-align: left; vertical-align: middle; line-height: 1.4;
        }}
        /* th (헤더)는 가운데 정렬 */
        #application-method-section-final-hc .criteria-table th {{
            background-color: {TABLE_HEADER_BACKGROUND}; color: {TEXT_COLOR_BODY_STRONG}; font-weight: 600; text-align: center;
        }}
        /* '구분' (L1) 셀 가운데 정렬 */
        #application-method-section-final-hc .category-header-cell {{
            font-weight: 500; background-color: {HIGHLIGHT_ORANGE_VERY_LIGHT_BACKGROUND}; color: {TEXT_COLOR_BODY_STRONG}; text-align: center;
        }}
        /* '주요 항목' (L2) 셀 가운데 정렬 */
        #application-method-section-final-hc .sub-category-item-cell {{ 
            font-weight: normal; background-color: {HIGHLIGHT_ORANGE_EXTREMELY_LIGHT_BACKGROUND}; color: {TEXT_COLOR_BODY_STRONG}; text-align: center; vertical-align: middle;
        }}
        /* '세부 내용(질문)' (L3) 셀은 왼쪽 정렬 (기본 td 설정과 동일하나 명시적으로 유지) */
        #application-method-section-final-hc .evaluation-question-cell {{ 
            text-align: left; vertical-align: middle;
        }}
        #application-method-section-final-hc .criteria-table .total-row td {{
            background-color: #f0f0f0; font-weight: bold; color: {TEXT_COLOR_BODY_STRONG};
        }}
        #application-method-section-final-hc .criteria-table .total-row td:first-child {{ /* 합계 텍스트 */
             text-align: center;
        }}
        #application-method-section-final-hc .criteria-table .total-row td:last-child {{ /* 합계 점수 */
            text-align: center;
        }}

        #application-method-section-final-hc .download-button-container {{ text-align: center; margin-top: 0px; margin-bottom: 10px; }}
        #application-method-section-final-hc .download-button {{ display: inline-block; background-color: {KEY_ORANGE_COLOR}; color: white !important; padding: 12px 28px; border-radius: 8px; text-decoration: none !important; font-size: 1.1em; font-weight: 600; text-align: center; border: none; box-shadow: 0 4px 12px rgba(0,0,0,0.15); transition: background-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease; cursor: pointer; margin: 5px; }}
        #application-method-section-final-hc .download-button:hover, #application-method-section-final-hc .download-button:focus {{ background-color: #E65100; transform: translateY(-2px); box-shadow: 0 6px 18px rgba(0,0,0,0.2); color: white !important; text-decoration: none !important; }}
        #application-method-section-final-hc .download-button:active {{ transform: translateY(0px); box-shadow: 0 3px 10px rgba(0,0,0,0.12); }}
        
        @media (max-width: 1200px) {{ #application-method-section-final-hc .content-wrapper {{ max-width: 95%; }} }}
        @media (max-width: 768px) {{
            #application-method-section-final-hc .main-title-orange {{ font-size: 1.7em; }}
            #application-method-section-final-hc .subtitle-emoji {{ font-size: 2.0em; }}
            #application-method-section-final-hc .info-card p.application-guide {{ font-size: 1.05em; }}
            #application-method-section-final-hc .criteria-table-title {{ font-size: 1.2em; }}
            #application-method-section-final-hc .criteria-table th,
            #application-method-section-final-hc .criteria-table td {{ padding: 8px; font-size: 0.85em; }}
            #application-method-section-final-hc .download-button {{ font-size: 1.05em; padding: 10px 22px; }}
        }}
        @media (max-width: 576px) {{
            #application-method-section-final-hc .criteria-table th,
            #application-method-section-final-hc .criteria-table td {{ font-size: 0.8em; }}
        }}
    </style>
    <div id="application-method-section-final-hc">
        <div class="content-wrapper">
            <h2 class="main-title-orange">접수 방법 및 평가 기준</h2> <h3 class="subtitle-emoji">🤔 지원과 평가는 어떻게 진행되나요?</h3>
            <div class="info-card">
                <p class="application-guide">
                    - 화면 하단의 <strong>'📝 지원하기'</strong> 버튼을 클릭하여 온라인 설문 링크에 접속합니다.<br>
                    - 해당 링크에서 <strong>(1)참가신청서 및 개인정보 동의서</strong>와 <strong>(2)사업계획서</strong>를 모두 다운로드 받아 작성 후, 그 외 제출 서류와 함께 구글폼에 업로드해 주십시오..<br>
                    - <Strong>서면 심사 합격자는 대면 심사 진행을 위한 발표 자료(IR 발표자료 등)를 제출</Strong>해주셔야 하며, 서면 심사 합격 여부와 함께 별도 안내 될 예정입니다. <br> <Strong>(※ 제출기한: 7월 8일 16:00)</Strong>
                </p>
                <div>
                    <h4 class="criteria-table-title">평가 기준표</h4>
                    <div class="criteria-table-container">
                        <table class="criteria-table">
                            <thead>
                                <tr>
                                    <th style="width:25%;">평가 기준</th>
                                    <th style="width:30%;">평가 항목</th>
                                    <th style="width:45%;">평가 질문(점수)</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td rowspan="4" class="category-header-cell">창업 동기 및 역량<br>(20점)</td>
                                    <td rowspan="2" class="sub-category-item-cell">창업 동기 및 필요성<br>(10점)</td>
                                    <td class="evaluation-question-cell">기업이 해결하고자 하는 사회문제가 구체적으로 제시되고 있는가? (5점)</td>
                                </tr>
                                <tr>
                                    <td class="evaluation-question-cell">기업의 사업모델을 통해 사회문제를 해결할 수 있는가? (5점)</td>
                                </tr>
                                <tr>
                                    <td rowspan="2" class="sub-category-item-cell">보유 역량<br>(10점)</td>
                                    <td class="evaluation-question-cell">대표와 의사결정그룹이 뚜렷한 임팩트 기업가 정신을 가지고 사업을 추진하고 있는가? (5점)</td>
                                </tr>
                                <tr>
                                    <td class="evaluation-question-cell">사업실행을 위한 핵심 기술을 책임지고 이끌 수 있는 인력(팀)이 구성되어 있는가? (5점)</td>
                                </tr>
                                <tr>
                                    <td rowspan="2" class="category-header-cell">창업 아이템 개요 및 차별성<br>(20점)</td>
                                    <td class="sub-category-item-cell">창업 아이템 개요<br>(10점)</td>
                                    <td class="evaluation-question-cell">핵심 고객에 대한 정의와 고객/거래처 확보가 되어 있는가? (10점)</td>
                                </tr>
                                <tr>
                                    <td class="sub-category-item-cell">창업 아이템 차별성<br>(10점)</td>
                                    <td class="evaluation-question-cell">기업의 사업모델(아이템)이 경쟁사 대비 차별적이고 독창적인가? (10점)</td>
                                </tr>
                                <tr>
                                    <td rowspan="3" class="category-header-cell">창업 아이템 시장성<br>(30점)</td>
                                    <td class="sub-category-item-cell">창업 아이템의 국내·외 시장성<br>(5점)</td>
                                    <td class="evaluation-question-cell">시장의 니즈를 파악하고 그에 대한 전략이 세워져 있는가? (5점)</td>
                                </tr>
                                <tr>
                                    <td rowspan="2" class="sub-category-item-cell">국내·외 시장진입 전략<br>(25점)</td>
                                    <td class="evaluation-question-cell">비즈니스의 양적 확장과 질적 성장에 대한 타당한 계획이 있는가? (15점)</td>
                                </tr>
                                <tr>
                                    <td class="evaluation-question-cell">기업이 제품, 서비스 홍보를 위한 영업 및 마케팅 전략이 있는가? (10점)</td>
                                </tr>
                                <tr>
                                    <td rowspan="2" class="category-header-cell">고용 및 자금조달 계획<br>(20점)</td>
                                    <td class="sub-category-item-cell">고용 계획<br>(5점)</td>
                                    <td class="evaluation-question-cell">신규인력 고용을 통해 팀의 역량을 강화하는데 계획을 가지고 있는가? (5점)</td>
                                </tr>
                                <tr>
                                    <td class="sub-category-item-cell">투자 및 자금조달 계획<br>(15점)</td>
                                    <td class="evaluation-question-cell">향후 투자유치 가능성 등 지속가능한 수익창출을 위한 기반이 존재하는가? (15점)</td>
                                </tr>
                                <tr>
                                    <td rowspan="2" class="category-header-cell">사회서비스 적합성<br>(10점)</td>
                                    <td rowspan="2" class="sub-category-item-cell">임팩트<br>(10점)</td>
                                    <td class="evaluation-question-cell">사회문제를 해결했을 때 발생되는 사회환경적 임팩트를 설명할 수 있는가? (5점)</td>
                                </tr>
                                <tr>
                                    <td class="evaluation-question-cell">사회서비스 분야의 문제를 해결할 수 있는 산업이며, 그것이 사회에 꼭 필요한가? (5점)</td>
                                </tr>
                            </tbody>
                            <tfoot class="total-row">
                                <tr>
                                    <td colspan="2"><strong>합계</strong></td>
                                    <td><strong>100점</strong></td>
                                </tr>
                            </tfoot>
                        </table>
                    </div>
                    <div class="download-button-container">
                        <a href="{참가신청서개인정보동의서}" class="download-button" download>📄 신청서 및 개인정보 동의서 다운로드</a>
                        <a href="{사업계획서}" class="download-button" download>📄 사업계획서 다운로드</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

# === 섹션 8: 문의하기 ===
def display_contact_info():
    contact_email = "social.link.academy@gmail.com"
    section_style = f"""
    <style>
        #contact-info-section {{ padding: 80px 20px; background-color: {BACKGROUND_COLOR_SECTION_LIGHT_GRAY}; font-family: 'Pretendard', sans-serif; }} /* 배경색 변경 */
        #contact-info-section .content-wrapper {{ max-width: 1050px; margin: 0 auto; }} /* 너비 수정: 700px -> 1050px */
        #contact-info-section .main-title-orange {{ font-size: 1.8em; font-weight: 700; color: {KEY_ORANGE_COLOR}; text-align: center; margin-bottom: 35px; }}
        .contact-card {{ background-color: {CARD_BACKGROUND_COLOR}; border-radius: 16px; box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.08); padding: 30px 35px; text-align: left; }}
        .contact-card h3 {{ font-size: 1.6em; font-weight: 600; color: {TEXT_COLOR_BODY_STRONG}; margin-top: 0; margin-bottom: 22px; text-align: center; }}
        .contact-card p {{ font-size: 1.15em; color: {TEXT_COLOR_BODY}; line-height: 1.8; margin-bottom: 12px; display: flex; align-items: center; }}
        .contact-card p:last-child {{ margin-bottom: 0; }}
        .contact-card .icon {{ margin-right: 12px; font-size: 1.2em; color: {KEY_ORANGE_COLOR}; width: 22px; text-align:center; }}
        .contact-card strong {{ color: {TEXT_COLOR_BODY_STRONG};}}
        .contact-card a {{ color: {KEY_ORANGE_COLOR}; text-decoration: none; font-weight: 500;}}
        .contact-card a:hover {{ text-decoration: underline; }}
        @media (max-width: 1050px) {{ /* 반응형 max-width 조정 */
            #contact-info-section .content-wrapper {{ max-width: 95%; }}
        }}
        @media (max-width: 768px) {{ #contact-info-section .main-title-orange {{ font-size: 1.7em; margin-bottom:30px; }} .contact-card h3 {{ font-size: 1.5em; }} .contact-card p {{ font-size: 1.1em; }} }}
    </style>"""
    st.markdown(section_style, unsafe_allow_html=True)
    content_html = f"""
    <div id="contact-info-section"><div class="content-wrapper">
            <h2 class="main-title-orange">문의하기</h2>
            <div class="contact-card">
                <h3>프로그램 운영 사무국 (MYSC)</h3>
                <p><span class="icon">✉️</span><strong>이메일:</strong> <a href="mailto:{contact_email}">{contact_email}</a></p>
                <p><span class="icon">📞</span><strong>연락처:</strong> 02-499-5111 </p>
            </div></div></div>"""
    st.markdown(content_html, unsafe_allow_html=True)
    

def display_key_achievements_section(): # 현재 호출되지 않음
    main_title_text = "소셜 링크 아카데미 및 사회서비스 투자 교류회"
    subtitle_text = "주요 성과 (2023-2024)"
    section_html_content = f"""
    <style>
        #key-achievements-section-mvp {{ background-color: {BACKGROUND_COLOR_SECTION_WHITE}; padding: 60px 20px; text-align: center; font-family: 'Pretendard', sans-serif; }}
        #key-achievements-section-mvp .content-wrapper-mvp {{ max-width: 1380px; margin: 0 auto; }} /* 너비 수정: 920px -> 1380px */
        #key-achievements-section-mvp .key-achievements-main-title {{ font-size: 1.2em; font-weight: 700; color: {KEY_ORANGE_COLOR}; text-align: center; margin-bottom: 0px; }}
        #key-achievements-section-mvp .key-achievements-subtitle {{ font-size: 1.8em; font-weight: 600; color: {TEXT_COLOR_HEADINGS}; text-align: center; margin-bottom: 35px; }}
        .achievements-grid-mvp {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 25px; }}
        .achievement-item-mvp {{ background-color: {CARD_BACKGROUND_COLOR}; border: 1px solid #f0f0f0; border-radius: 12px; padding: 20px 15px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.05); cursor: pointer; transition: transform 0.3s ease-in-out, background-color 0.3s ease-in-out, border-color 0.3s ease-in-out, box-shadow 0.3s ease-in-out; }}
        .achievement-item-mvp:hover {{ background-color: {KEY_ORANGE_COLOR}; transform: scale(1.05); border-color: {KEY_ORANGE_COLOR}; box-shadow: 0 8px 20px rgba(0,0,0,0.1); }}
        .achievement-item-mvp .icon-mvp {{ font-size: 2.6em; display: block; margin-bottom: 15px; line-height: 1; color: {KEY_ORANGE_COLOR}; transition: color 0.3s ease-in-out; }}
        .achievement-item-mvp:hover .icon-mvp {{ color: #ffffff; }}
        .achievement-item-mvp h4 {{ font-size: 1.15em; font-weight: 600; color: {TEXT_COLOR_BODY_STRONG}; margin-top: 0; margin-bottom: 6px; line-height: 1.4; transition: color 0.3s ease-in-out; }}
        .achievement-item-mvp:hover h4 {{ color: #ffffff; }}
        .achievement-item-mvp .stat-mvp {{ font-size: 1.0em; font-weight: 500; color: {TEXT_COLOR_BODY}; margin-bottom: 4px; line-height: 1.5; transition: color 0.3s ease-in-out; }}
        .achievement-item-mvp:hover .stat-mvp {{ color: #ffffff; }}
        .achievement-item-mvp .stat-mvp .stat-highlight {{ color: {KEY_ORANGE_COLOR}; font-weight: 700; transition: color 0.3s ease-in-out; }}
        .achievement-item-mvp:hover .stat-mvp .stat-highlight {{ color: #ffffff; }}
        .achievement-item-mvp .sub-detail-mvp {{ font-size: 0.8em; color: {TEXT_COLOR_CAPTION}; line-height: 1.4; transition: color 0.3s ease-in-out; }}
        .achievement-item-mvp:hover .sub-detail-mvp {{ color: #f0f0f0; }}
        @media (max-width: 1380px) {{ /* 반응형 max-width 조정 */
            #key-achievements-section-mvp .content-wrapper-mvp {{ max-width: 95%; }}
        }}
        @media (max-width: 992px) {{ .achievements-grid-mvp {{ grid-template-columns: repeat(2, 1fr); gap: 20px; }} #key-achievements-section-mvp .key-achievements-main-title {{ font-size: 1.7em; }} #key-achievements-section-mvp .key-achievements-subtitle {{ font-size: 1.3em; margin-bottom: 30px;}} .achievement-item-mvp .icon-mvp {{ font-size: 2.4em; }} .achievement-item-mvp h4 {{ font-size: 1.1em; }} .achievement-item-mvp .stat-mvp {{ font-size: 0.95em; }} }}
        @media (max-width: 576px) {{ .achievements-grid-mvp {{ grid-template-columns: 1fr; gap: 18px; }} #key-achievements-section-mvp {{ padding: 50px 15px; }} #key-achievements-section-mvp .key-achievements-main-title {{ font-size: 1.6em; }} #key-achievements-section-mvp .key-achievements-subtitle {{ font-size: 1.2em; margin-bottom: 25px;}} .achievement-item-mvp .icon-mvp {{ font-size: 2.2em; }} .achievement-item-mvp h4 {{ font-size: 1.05em; }} .achievement-item-mvp .stat-mvp {{ font-size: 0.9em; }} .achievement-item-mvp .sub-detail-mvp {{ font-size: 0.75em; }} }}
    </style>
    <div id="key-achievements-section-mvp"> <div class="content-wrapper-mvp"> <h2 class="key-achievements-main-title">{main_title_text}</h2> <h3 class="key-achievements-subtitle">{subtitle_text}</h3> <div class="achievements-grid-mvp"> <div class="achievement-item-mvp"> <span class="icon-mvp">🎓</span> <h4>소셜 링크 아카데미</h4> <p class="stat-mvp"> <strong class='stat-highlight'>1, 2기</strong> 운영</p> </div> <div class="achievement-item-mvp"> <span class="icon-mvp">🏢</span> <h4>함께한 기업</h4> <p class="stat-mvp">총 <strong class='stat-highlight'>124</strong>개社</p> <p class="sub-detail-mvp">(중복 제외)</p> </div> <div class="achievement-item-mvp"> <span class="icon-mvp">👥</span> <h4>함께한 사람들</h4> <p class="stat-mvp"><strong class='stat-highlight'>500</strong>여 명</p> </div> <div class="achievement-item-mvp"> <span class="icon-mvp">🤝</span> <h4>투자 교류회</h4> <p class="stat-mvp">총 <strong class='stat-highlight'>9</strong>회 운영</p> </div> <div class="achievement-item-mvp"> <span class="icon-mvp">₩</span> <h4>투자 금액</h4> <p class="stat-mvp">총 <strong class='stat-highlight'>145.25</strong>억 원</p> </div> <div class="achievement-item-mvp"> <span class="icon-mvp">📈</span> <h4>참여 투자사</h4> <p class="stat-mvp"><strong class='stat-highlight'>66</strong>개사,</p> <p class="sub-detail-mvp">소속 VC 약 120명 참여</p> </div> </div> </div> </div>
    """
    st.markdown(section_html_content, unsafe_allow_html=True)

# ===============================================
# === Streamlit 앱 메인 실행 로직 (호출 순서) ===
# ===============================================
def main():

    GA_TAG_HTML = """
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-3M5RSCCZQN"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-3M5RSCCZQN');
    </script>
    """
    st_html(GA_TAG_HTML, height=0)
    inject_custom_elements(GOOGLE_FORM_URL)
    display_hero_banner()
    display_post_hero_section()
    display_who_can_apply_section()
    display_benefits_section()
    display_program_flow_section()
    
    hr_style = "border:none; border-top:1px solid #eee; margin: 60px auto; width: 80%; max-width: 900px;"
    
    st.markdown(f"<hr style='{hr_style}'>", unsafe_allow_html=True)
    display_application_method_text() # 평가 기준표가 이 함수 내부로 통합됨
    
    st.markdown(f"<hr style='{hr_style}'>", unsafe_allow_html=True) # "접수 방법 및 평가 기준" 섹션 후 구분선
    display_contact_info()

    footer_html = f"""
    <style>
        .footer-caption {{ text-align: center; font-size: 0.9em; color: #888888; padding: 25px 0; border-top: 1px solid #eaeaea; margin-top: 40px; font-family: 'Pretendard', sans-serif; }}
        .footer-caption strong {{ color: #666666; }}
    </style>
    <div class="footer-caption"> © 2025 중앙사회서비스원 & MYSC . All rights reserved. &nbsp;&nbsp;&nbsp;&nbsp; </div>"""
    st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()