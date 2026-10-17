import streamlit as st
from backend import db
from frontend.styles import page_header, book_card


def render_search():
    page_header("THE READING NOOK", "Discover a volume", "Search by title, author, ISBN, or category. The results come directly from your catalogue in MySQL.")
    query=st.text_input("What would you like to find?",placeholder="Try a title, author, ISBN, or category…",key="discover_query")
    try:
        rows=db.book_list(query.strip() or None)
        if query.strip(): st.caption(f"{len(rows)} result(s) for “{query.strip()}”")
        elif rows: st.caption(f"Showing all {len(rows)} titles")
        if rows:
            for row in rows: book_card(row)
        else: st.markdown("<div class='empty-state'>No matching titles found. Try fewer words or check the spelling.</div>",unsafe_allow_html=True)
    except Exception as exc: st.error(f"Search could not reach the database: {exc}")
