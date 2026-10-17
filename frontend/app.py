
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from styles import apply_custom_styles
from login import render_login
import dashboard, books, members, issue_return, search, reports, master_data, settings_page

st.set_page_config(
    page_title="Central Library Management | MUJ", 
    page_icon="📚", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Initialize Session State
defaults = {
    "authenticated": False,
    "current_page": "Dashboard",
    "username": None
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

apply_custom_styles()

if not st.session_state["authenticated"]:
    render_login()
else:
    with st.sidebar:
        st.markdown(
            """
            <div style='margin-bottom: 0.8rem;'>
                <span style='background: rgba(59, 130, 246, 0.2); color: #60a5fa; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: 600;'>
                    MANIPAL UNIVERSITY JAIPUR
                </span>
                <h3 style='margin-top: 0.5rem; margin-bottom: 0.2rem;'>Central Library</h3>
                <p style='font-size: 0.75rem; opacity: 0.7;'>Relational DBMS Portal</p>
            </div>
            """, 
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div style='background: rgba(125,125,125,0.12); padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem; border: 1px solid rgba(125,125,125,0.2);'>
                <div style='font-size: 0.68rem; letter-spacing: 0.1em; opacity: 0.7;'>CURRENT OPERATOR</div>
                <strong>{st.session_state.get('username') or 'Librarian'}</strong>
                <div style='font-size: 0.75rem; opacity: 0.75;'>Administrator / Staff</div>
            </div>
            """, 
            unsafe_allow_html=True
        )

        nav = ["Dashboard", "Books", "Members", "Issue / Return", "Search", "Reports", "Authors / Publishers / Categories", "Settings"]
        icons = {
            "Dashboard": "⌂", 
            "Books": "▤", 
            "Members": "♙", 
            "Issue / Return": "⇄", 
            "Search": "⌕", 
            "Reports": "▥", 
            "Authors / Publishers / Categories": "✧", 
            "Settings": "⚙"
        }

        current = st.session_state.get("current_page", "Dashboard")
        selected = st.radio(
            "Navigation", 
            nav, 
            index=nav.index(current) if current in nav else 0, 
            format_func=lambda x: f"{icons[x]}   {x}", 
            label_visibility="collapsed"
        )
        st.session_state["current_page"] = selected

        st.markdown("<div style='height:1px; background: rgba(125,125,125,0.25); margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

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