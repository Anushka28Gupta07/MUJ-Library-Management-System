import streamlit as st
from backend import db


def render_login():
    st.markdown("<div class='hero'><div class='hero-kicker'>THE LIBRARIAN'S PRIVATE STUDY</div><h1>Every great adventure<br>begins with a story.</h1><p>A thoughtfully organised collection, a welcoming place for readers, and a little magic in the everyday work of a library.</p><span class='hero-seal'>✦ THE ENCHANTED LIBRARY · EST. WITH IMAGINATION ✦</span></div>", unsafe_allow_html=True)
    st.write("")
    left, right = st.columns([1.1, .9], gap="large", vertical_alignment="center")
    with left:
        st.markdown("<div class='eyebrow'>WELCOME, KEEPER OF STORIES</div><h2 style='margin-top:0'>Your library awaits.</h2><div class='page-intro'>Sign in to tend the catalogue, welcome new members, manage lending, and keep every volume in its rightful place.</div>", unsafe_allow_html=True)
        st.markdown("<div class='paper-card'><div style='font-family:Cinzel,serif;color:#681f2d;font-size:1rem;font-weight:700'>A place for curious minds</div><p style='color:#786c60;margin:.45rem 0 0;line-height:1.7'>A warm, storybook-inspired workspace designed for real library operations — not just a pretty cover.</p></div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='section-heading'>Librarian sign in</div>", unsafe_allow_html=True)
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submitted = st.form_submit_button("Unlock the library  →", use_container_width=True)
        st.markdown("<div class='tiny-note'>Demo access: <b>admin</b> / <b>admin123</b></div>", unsafe_allow_html=True)
        if submitted:
            try:
                if db.check_login(username.strip(), password):
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username.strip()
                    st.session_state["current_page"] = "Dashboard"
                    st.rerun()
                else:
                    st.error("Those credentials don't match. Please try again.")
            except Exception as exc:
                st.error(f"Could not validate sign-in: {exc}")
