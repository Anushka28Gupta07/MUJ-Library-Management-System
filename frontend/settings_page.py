import streamlit as st
from frontend.styles import page_header


def render_settings():
    page_header("THE LIBRARIAN'S DESK", "Settings & notes", "A few details about this workspace and the rules currently enforced by the Python backend.")
    st.markdown("<div class='hero'><div class='hero-kicker'>DESIGN LANGUAGE</div><h1>Warm parchment.<br>Scarlet and antique gold.</h1><p>A storybook-inspired library aesthetic with readable contrast, restrained motion, and a professional workspace.</p><span class='hero-seal'>✦ MOTION RESPECTS REDUCED-MOTION SETTINGS ✦</span></div>",unsafe_allow_html=True)
    st.markdown("<div class='section-heading'>Lending rules</div>",unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1: st.markdown("<div class='stat-card'><div class='stat-icon'>◷</div><div class='stat-number'>14 days</div><div class='stat-label'>Standard loan period</div></div>",unsafe_allow_html=True)
    with c2: st.markdown("<div class='stat-card'><div class='stat-icon'>₹</div><div class='stat-number'>₹2 / day</div><div class='stat-label'>Overdue fine, calculated by backend</div></div>",unsafe_allow_html=True)
    st.write("")
    st.markdown("<div class='paper-card'><div class='book-title'>Database connection</div><div class='book-meta'>The frontend calls the existing backend functions in <code>backend/db.py</code>. MySQL credentials remain in your root <code>.env</code> file and are not included in this frontend package.</div></div>",unsafe_allow_html=True)
    st.caption("Demo sign-in is handled by the existing backend: admin / admin123. Change authentication before deploying this demo for real users.")

