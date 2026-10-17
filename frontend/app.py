import streamlit as st
from styles import apply_custom_styles
from login import render_login
import dashboard
import books
import members
import issue_return
import search
import reports
import master_data

# Page configuration
st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)

# Initialize Session States
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Dashboard"

if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "Dark"

# Render Login if not logged in, otherwise render Portal with custom styles
if not st.session_state["authenticated"]:
    render_login()
else:
    # Apply dashboard theme only when logged in
    apply_custom_styles(theme=st.session_state["theme_mode"])

    # Sidebar Header
    st.sidebar.markdown("### 📚 **LMS Portal**")
    st.sidebar.markdown(
        f"""
        <div style='background: rgba(255,255,255,0.06); padding: 8px 12px; border-radius: 6px; margin-bottom: 14px;'>
            <span style='font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;'>Logged in as</span><br>
            <strong style='font-size: 14px;'>{st.session_state.get('username', 'Admin')}</strong> 
            <span style='font-size: 11px;'>• Chief Librarian</span>
        </div>
        """, 
        unsafe_allow_html=True
    )

    nav_options = [
        "Dashboard",
        "Books",
        "Members",
        "Issue Book",
        "Return Book",
        "Search",
        "Reports",
        "Authors / Publishers / Categories"
    ]

    selected_nav = st.sidebar.radio(
        "Navigation",
        options=nav_options,
        index=nav_options.index(st.session_state["current_page"]) if st.session_state["current_page"] in nav_options else 0,
        label_visibility="collapsed"
    )

    st.session_state["current_page"] = selected_nav

    st.sidebar.divider()

    # Theme Switcher Control
    col_t1, col_t2 = st.sidebar.columns([1, 1])
    with col_t1:
        if st.button("🌙 Dark", use_container_width=True):
            st.session_state["theme_mode"] = "Dark"
            st.rerun()
    with col_t2:
        if st.button("☀️ Light", use_container_width=True):
            st.session_state["theme_mode"] = "Light"
            st.rerun()

    # Logout
    st.sidebar.write("")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.session_state["current_page"] = "Dashboard"
        st.rerun()

    # Route to screen module
    if selected_nav == "Dashboard":
        dashboard.render_dashboard()
    elif selected_nav == "Books":
        books.render_books()
    elif selected_nav == "Members":
        members.render_members()
    elif selected_nav == "Issue Book":
        issue_return.render_issue()
    elif selected_nav == "Return Book":
        issue_return.render_return()
    elif selected_nav == "Search":
        search.render_search()
    elif selected_nav == "Reports":
        reports.render_reports()
    elif selected_nav == "Authors / Publishers / Categories":
        master_data.render_master_data()
