
import sys
from pathlib import Path

# Add the project root so Python can find the backend folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


import streamlit as st
from styles import apply_custom_styles
from login import render_login
import dashboard, books, members, issue_return, search, reports, master_data, settings_page

st.set_page_config(page_title="The Reading Room | Library Management", page_icon="📚", layout="wide", initial_sidebar_state="expanded")

for key, value in {"authenticated": False, "current_page": "Dashboard", "username": None}.items():
    if key not in st.session_state:
        st.session_state[key] = value

apply_custom_styles()

if not st.session_state["authenticated"]:
    render_login()
else:
    with st.sidebar:
        st.markdown("<div style='text-align:center;padding:.65rem 0 1rem'><div style='font-size:2.2rem'>♧</div><div style='font-family:Playfair Display,Georgia,serif;font-size:1.28rem;font-weight:700;line-height:1.2'>The Reading Room</div><div style='font-size:.72rem;letter-spacing:.12em;margin-top:.35rem;opacity:.75'>LIBRARY MANAGEMENT</div></div>", unsafe_allow_html=True)
        st.markdown("<div style='background:rgba(255,255,255,.08);padding:.8rem;border-radius:10px;margin-bottom:1rem'><div style='font-size:.68rem;letter-spacing:.12em;opacity:.7'>SIGNED IN AS</div><strong>" + str(st.session_state.get('username') or 'Librarian') + "</strong><div style='font-size:.78rem;opacity:.78'>Chief Librarian</div></div>", unsafe_allow_html=True)
        nav = ["Dashboard", "Books", "Members", "Issue / Return", "Search", "Reports", "Authors / Publishers / Categories", "Settings"]
        icons = {"Dashboard":"⌂", "Books":"▤", "Members":"♙", "Issue / Return":"⇄", "Search":"⌕", "Reports":"▥", "Authors / Publishers / Categories":"✧", "Settings":"⚙"}
        current = st.session_state.get("current_page", "Dashboard")
        selected = st.radio("Navigate", nav, index=nav.index(current) if current in nav else 0, format_func=lambda x: f"{icons[x]}   {x}", label_visibility="collapsed")
        st.session_state["current_page"] = selected
        st.markdown("<div style='height:1px;background:rgba(255,255,255,.2);margin:1rem 0'></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:.76rem;opacity:.72;line-height:1.6'>A quieter place for good books.<br/>Manage your collection with care.</div>", unsafe_allow_html=True)
        if st.button("↪  Sign out", use_container_width=True):
            st.session_state["authenticated"] = False
            st.session_state["username"] = None
            st.session_state["current_page"] = "Dashboard"
            st.rerun()

    routes = {
        "Dashboard": dashboard.render_dashboard,
        "Books": books.render_books,
        "Members": members.render_members,
        "Issue / Return": issue_return.render_issue_return,
        "Search": search.render_search,
        "Reports": reports.render_reports,
        "Authors / Publishers / Categories": master_data.render_master_data,
        "Settings": settings_page.render_settings,
    }
    routes[selected]()
