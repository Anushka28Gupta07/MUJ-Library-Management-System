import streamlit as st
from backend import db
from frontend.styles import page_header


def _cards(rows, id_key, title_key, detail_key=None):
    if not rows:
        st.markdown("<div class='empty-state'>Nothing here yet. Add the first record using the form.</div>",unsafe_allow_html=True); return
    import html
    for row in rows:
        title=html.escape(str(row.get(title_key) or 'Untitled')); detail=html.escape(str(row.get(detail_key) or '')) if detail_key else ''
        st.markdown(f"<div class='paper-card' style='display:flex;align-items:center;gap:.8rem'><div class='book-spine' style='width:38px;min-width:38px;height:45px'>✧</div><div style='flex:1'><div class='book-title'>{title}</div><div class='book-meta'>{detail}</div></div><span class='pill'>ID {row[id_key]}</span></div>",unsafe_allow_html=True)


def render_master_data():
    page_header("THE REFERENCE SHELVES", "Collection setup", "Maintain the authors, publishers, and categories that help keep the catalogue consistent.")
    authors_tab,publishers_tab,categories_tab=st.tabs(["✍ Authors","▤ Publishers","✧ Categories"])
    with authors_tab:
        try: _cards(db.list_authors(),'AuthorID','AuthorName','Nationality')
        except Exception as exc: st.error(str(exc))
        with st.form("add_author",clear_on_submit=True):
            st.markdown("#### Add an author"); name=st.text_input("Author name *"); nationality=st.text_input("Nationality (optional)"); submit=st.form_submit_button("Add author")
        if submit:
            try:
                if not name.strip(): st.error("Author name is required.")
                else: db.add_author(name,nationality); st.success("Author added."); st.rerun()
            except Exception as exc: st.error(f"Could not add author: {exc}")
    with publishers_tab:
        try: _cards(db.list_publishers(),'PublisherID','PublisherName','City')
        except Exception as exc: st.error(str(exc))
        with st.form("add_publisher",clear_on_submit=True):
            st.markdown("#### Add a publisher"); name=st.text_input("Publisher name *"); city=st.text_input("City (optional)"); submit=st.form_submit_button("Add publisher")
        if submit:
            try:
                if not name.strip(): st.error("Publisher name is required.")
                else: db.add_publisher(name,city); st.success("Publisher added."); st.rerun()
            except Exception as exc: st.error(f"Could not add publisher: {exc}")
    with categories_tab:
        try: _cards(db.list_categories(),'CategoryID','CategoryName')
        except Exception as exc: st.error(str(exc))
        with st.form("add_category",clear_on_submit=True):
            st.markdown("#### Add a category"); name=st.text_input("Category name *"); submit=st.form_submit_button("Add category")
        if submit:
            try:
                if not name.strip(): st.error("Category name is required.")
                else: db.add_category(name); st.success("Category added."); st.rerun()
            except Exception as exc: st.error(f"Could not add category: {exc}")
