import streamlit as st

def apply_custom_styles(theme="Dark"):
    """
    Applies unified theme styling to Streamlit input boxes, buttons, 
    sidebars, cards, and text to ensure high contrast in both themes.
    """
    if theme == "Dark":
        bg_main = "linear-gradient(135deg, #0b0f19 0%, #111827 50%, #0f172a 100%)"
        sidebar_bg = "linear-gradient(180deg, #090d16 0%, #0f172a 100%)"
        card_bg = "rgba(255, 255, 255, 0.03)"
        card_border = "rgba(255, 255, 255, 0.10)"
        text_primary = "#f8fafc"
        text_secondary = "#94a3b8"
        input_bg = "#1e293b"
        input_border = "#334155"
        btn_bg = "#1e293b"
        btn_text = "#f8fafc"
        btn_hover = "#334155"
    else:  # Light Mode
        bg_main = "linear-gradient(135deg, #f8fafc 0%, #edf2f7 50%, #f1f5f9 100%)"
        sidebar_bg = "#ffffff"
        card_bg = "#ffffff"
        card_border = "#e2e8f0"
        text_primary = "#0f172a"
        text_secondary = "#475569"
        input_bg = "#ffffff"
        input_border = "#cbd5e1"
        btn_bg = "#f1f5f9"
        btn_text = "#0f172a"
        btn_hover = "#e2e8f0"

    st.markdown(
        f"""
        <style>
        /* Viewport Background */
        [data-testid="stAppViewContainer"] {{
            background: {bg_main} !important;
            color: {text_primary} !important;
        }}

        [data-testid="stHeader"] {{
            background: rgba(0,0,0,0) !important;
        }}

        /* Sidebar */
        [data-testid="stSidebar"] {{
            background: {sidebar_bg} !important;
            border-right: 1px solid {card_border} !important;
        }}

        /* Headings & Text */
        h1, h2, h3, h4, h5, h6, p, span, label, div {{
            color: {text_primary} !important;
        }}

        /* Text Inputs & Select Boxes */
        input, select, textarea, div[data-baseweb="select"] > div {{
            background-color: {input_bg} !important;
            color: {text_primary} !important;
            border: 1px solid {input_border} !important;
            border-radius: 6px !important;
        }}

        /* Buttons: Ensure visible text and borders */
        .stButton > button {{
            background-color: {btn_bg} !important;
            color: {btn_text} !important;
            border: 1px solid {input_border} !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            transition: all 0.15s ease-in-out !important;
        }}

        .stButton > button:hover {{
            background-color: {btn_hover} !important;
            border-color: #94a3b8 !important;
        }}

        /* Primary action buttons (Delete, Confirm, etc.) */
        button[kind="primary"] {{
            background-color: #ef4444 !important;
            color: #ffffff !important;
            border: none !important;
        }}

        /* Metric Tiles & Form Containers */
        div[data-testid="stMetric"], div[data-testid="stForm"] {{
            background: {card_bg} !important;
            border: 1px solid {card_border} !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
        }}

        /* DataTables */
        div[data-testid="stDataFrame"] {{
            border: 1px solid {card_border} !important;
            border-radius: 8px !important;
            overflow: hidden !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )