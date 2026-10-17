import streamlit as st
import base64
from pathlib import Path
from backend import db

def get_base64_image(image_path):
    if Path(image_path).exists():
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def render_login():
    img_path = Path(__file__).parent / "background.jpg"
    b64_bg = get_base64_image(img_path)

    bg_style = ""
    if b64_bg:
        bg_style = f"""
        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(rgba(10, 15, 26, 0.65), rgba(10, 15, 26, 0.75)), 
                        url("data:image/jpeg;base64,{b64_bg}") no-repeat center center fixed !important;
            background-size: cover !important;
        }}
        """

    st.markdown(
        f"""
        <style>
        {bg_style}
        /* Style the tabs clean and flat */
        div[data-baseweb="tab-list"] {{
            margin-bottom: 0.5rem !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    col_left, col_right = st.columns([1.25, 1], gap="large")

    with col_left:
        st.markdown(
"""<div style='padding-top: 1rem;'>
<div style='font-size: 0.75rem; letter-spacing: 0.14em; text-transform: uppercase; color: #94a3b8; font-weight: 600;'>THE LIBRARIAN'S PRIVATE STUDY</div>
<h1 style='font-size: 2.85rem; font-weight: 800; line-height: 1.15; margin: 0.8rem 0; color: #f8fafc;'>Every great adventure begins with a story.</h1>
<p style='font-size: 1.05rem; color: #cbd5e1; line-height: 1.6;'>A thoughtfully organised collection, a welcoming place for readers, and a little magic in the everyday work of a library.</p>
<div style='font-size: 0.8rem; letter-spacing: 0.1em; color: #94a3b8; margin-top: 0.8rem;'>✦ THE ENCHANTED LIBRARY · EST. WITH IMAGINATION ✦</div>
<div style='margin-top: 2rem;'>
<div style='font-size: 0.75rem; letter-spacing: 0.12em; text-transform: uppercase; color: #94a3b8; font-weight: 600;'>WELCOME, KEEPER OF STORIES</div>
<h2 style='font-size: 1.9rem; font-weight: 700; margin: 0.35rem 0; color: #f8fafc;'>Your library awaits.</h2>
<p style='font-size: 0.95rem; color: #94a3b8;'>Sign in to tend the catalogue, welcome new members, manage lending, and keep every volume in its rightful place.</p>
</div>
<div style='margin-top: 1.5rem; padding: 1rem 1.2rem; background: rgba(30, 41, 59, 0.6); border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);'>
<div style='color: #f87171; font-weight: 600; font-size: 0.9rem;'>A place for curious minds</div>
<div style='font-size: 0.85rem; color: #94a3b8; margin-top: 0.2rem;'>A warm, storybook-inspired workspace designed for real library operations — not just a pretty cover.</div>
</div>
</div>""",
            unsafe_allow_html=True
        )

    with col_right:
        login_tab, signup_tab = st.tabs(["Librarian sign in", "Register member"])

        with login_tab:
            with st.form("signin_form"):
                uname = st.text_input("Username", placeholder="e.g., admin")
                pwd = st.text_input("Password", type="password", placeholder="••••••••")
                submit = st.form_submit_button("Unlock the library →", use_container_width=True)

            if submit:
                if db.check_login(uname, pwd):
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = uname
                    st.session_state["current_page"] = "Dashboard"
                    st.rerun()
                else:
                    st.error("Invalid credentials. (Default: admin / admin123)")

        with signup_tab:
            st.caption("Enroll a new member into the MySQL database.")
            with st.form("member_signup_form", clear_on_submit=True):
                m_name = st.text_input("Full Name *", placeholder="e.g., Ayushi Verma")
                m_email = st.text_input("Email Address *", placeholder="e.g., ayushi@example.com")
                m_phone = st.text_input("Phone Number (optional)", placeholder="e.g., 9876543210")
                m_submit = st.form_submit_button("Create Member Account", use_container_width=True)

            if m_submit:
                if not m_name.strip() or not m_email.strip():
                    st.error("Name and email are required.")
                else:
                    try:
                        mem_id = db.add_member(m_name.strip(), m_email.strip(), m_phone.strip())
                        st.success(f"Member created successfully! Member ID: #{mem_id}")
                    except Exception as err:
                        st.error(f"Error creating member: {err}")
