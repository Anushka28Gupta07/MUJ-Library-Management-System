import streamlit as st
from backend import db
from frontend.styles import page_header, book_card


def render_books():
    page_header("THE CATALOGUE", "The book collection", "Browse the shelves, add new titles, and maintain your catalogue. All changes are saved to MySQL.")
    browse, add, manage = st.tabs(["✦ Browse the shelves", "＋ Add a volume", "⚙ Manage titles"])
    with browse:
        term=st.text_input("Search the catalogue",placeholder="Title, ISBN, author, or category",key="catalogue_search")
        try:
            rows=db.book_list(term or None)
            st.caption(f"{len(rows)} title(s) found")
            if rows:
                for row in rows: book_card(row)
            else: st.markdown("<div class='empty-state'>No matching volumes. Try another search or add a title.</div>",unsafe_allow_html=True)
        except Exception as exc: st.error(f"Could not load the catalogue: {exc}")
    with add:
        st.markdown("<div class='section-heading'>Add a volume to the shelves</div>",unsafe_allow_html=True)
        try:
            # Quick-create reference records here so users are not forced to leave the book workflow.
            with st.expander("＋ Add an author, publisher, or category first"):
                quick_author, quick_publisher, quick_category = st.tabs(["New author", "New publisher", "New category"])
                with quick_author:
                    with st.form("quick_add_author", clear_on_submit=True):
                        qa_name = st.text_input("Author name *", key="quick_author_name")
                        qa_nationality = st.text_input("Nationality (optional)", key="quick_author_nationality")
                        qa_submit = st.form_submit_button("Save author")
                    if qa_submit:
                        if not qa_name.strip(): st.error("Enter an author name.")
                        else:
                            db.add_author(qa_name.strip(), qa_nationality.strip())
                            st.success("Author saved. The author list will refresh.")
                            st.rerun()
                with quick_publisher:
                    with st.form("quick_add_publisher", clear_on_submit=True):
                        qp_name = st.text_input("Publisher name *", key="quick_publisher_name")
                        qp_city = st.text_input("City (optional)", key="quick_publisher_city")
                        qp_submit = st.form_submit_button("Save publisher")
                    if qp_submit:
                        if not qp_name.strip(): st.error("Enter a publisher name.")
                        else:
                            db.add_publisher(qp_name.strip(), qp_city.strip())
                            st.success("Publisher saved. The publisher list will refresh.")
                            st.rerun()
                with quick_category:
                    with st.form("quick_add_category", clear_on_submit=True):
                        qc_name = st.text_input("Category name *", key="quick_category_name")
                        qc_submit = st.form_submit_button("Save category")
                    if qc_submit:
                        if not qc_name.strip(): st.error("Enter a category name.")
                        else:
                            db.add_category(qc_name.strip())
                            st.success("Category saved. The category list will refresh.")
                            st.rerun()
            pubs,cats,authors=db.list_publishers(),db.list_categories(),db.list_authors()
            if not pubs or not cats:
                st.warning("Before adding a book, add at least one publisher and one category in Collection Setup.")
            else:
                with st.form("add_book_form",clear_on_submit=True):
                    title=st.text_input("Book title *"); isbn=st.text_input("ISBN *")
                    c1,c2=st.columns(2)
                    with c1: year=st.number_input("Publication year",min_value=1450,max_value=2100,value=2024,step=1)
                    with c2: copies=st.number_input("Physical copies",min_value=0,max_value=500,value=1,step=1)
                    publisher=st.selectbox("Publisher *",pubs,format_func=lambda x:x['PublisherName'])
                    category=st.selectbox("Category *",cats,format_func=lambda x:x['CategoryName'])
                    chosen=st.multiselect("Author(s)",authors,format_func=lambda x:x['AuthorName'])
                    submit=st.form_submit_button("Add to the catalogue",use_container_width=True)
                if submit:
                    if not title.strip() or not isbn.strip(): st.error("Title and ISBN are required.")
                    else:
                        new_id=db.add_book(isbn,title,int(year),publisher['PublisherID'],category['CategoryID'],[a['AuthorID'] for a in chosen],int(copies))
                        st.success(f"Volume added successfully · Book ID {new_id}"); st.rerun()
        except Exception as exc: st.error(f"Could not prepare the form: {exc}")
    with manage:
        try:
            rows=db.book_list()
            if not rows: st.info("There are no titles to manage yet.")
            else:
                selected=st.selectbox("Choose a title",rows,format_func=lambda x:f"{x['BookID']} · {x['Title']}")
                st.markdown("<div class='paper-card'>Only title and publication year can be edited here. Titles with loan history are protected from deletion by the backend.</div>",unsafe_allow_html=True)
                with st.form("edit_book_form"):
                    title=st.text_input("Title",value=selected['Title'])
                    year_val=selected.get('PublicationYear') or 2024
                    year=st.number_input("Publication year",min_value=1450,max_value=2100,value=int(year_val),step=1)
                    update=st.form_submit_button("Save changes")
                if update:
                    if not title.strip(): st.error("Title cannot be empty.")
                    else: db.update_book(selected['BookID'],title.strip(),int(year)); st.success("Title updated."); st.rerun()
                confirm=st.checkbox("I understand deletion cannot be undone",key="confirm_delete_book")
                if st.button("Delete selected title",disabled=not confirm):
                    try: db.delete_book(selected['BookID']); st.success("Title deleted."); st.rerun()
                    except Exception as exc: st.error(str(exc))
        except Exception as exc: st.error(f"Could not load titles: {exc}")
