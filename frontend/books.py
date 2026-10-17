import streamlit as st
from backend import db
from frontend.styles import page_header, book_card


def render_books():
    page_header("THE CATALOGUE", "The book collection", "Browse the shelves, add new titles, and maintain your catalogue. All changes are saved to MySQL.")
    
    browse, add_book_tab, master_add_tab, manage = st.tabs([
        "✦ Browse the shelves", 
        "＋ Add a volume", 
        "✍ Add Author / Publisher", 
        "⚙ Manage titles"
    ])

    # 1. BROWSE CATALOG
    with browse:
        term = st.text_input("Search the catalogue", placeholder="Title, ISBN, author, or category", key="catalogue_search")
        try:
            rows = db.book_list(term or None)
            st.caption(f"{len(rows)} title(s) found")
            if rows:
                for row in rows:
                    book_card(row)
            else:
                st.markdown("<div class='empty-state'>No matching volumes. Try another search or add a title.</div>", unsafe_allow_html=True)
        except Exception as exc:
            st.error(f"Could not load the catalogue: {exc}")

    # 2. ADD A VOLUME
    with add_book_tab:
        # Show persisted success banner if a volume was just added
        if st.session_state.get("book_added_success"):
            st.success(st.session_state.pop("book_added_success"))

        st.markdown("<div class='section-heading'>Add a volume to the shelves</div>", unsafe_allow_html=True)
        try:
            pubs = db.list_publishers()
            cats = db.list_categories()
            authors = db.list_authors()

            if not pubs or not cats:
                st.warning("Before adding a book, register at least one publisher and category in 'Add Author / Publisher'.")
            else:
                with st.form("add_book_form", clear_on_submit=True):
                    title = st.text_input("Book title *")
                    isbn = st.text_input("ISBN *")
                    c1, c2 = st.columns(2)
                    with c1:
                        year = st.number_input("Publication year", min_value=1450, max_value=2100, value=2024, step=1)
                    with c2:
                        copies = st.number_input("Physical copies", min_value=0, max_value=500, value=1, step=1)
                    
                    publisher = st.selectbox("Publisher *", pubs, format_func=lambda x: x['PublisherName'])
                    category = st.selectbox("Category *", cats, format_func=lambda x: x['CategoryName'])
                    chosen = st.multiselect("Author(s) *", authors, format_func=lambda x: x['AuthorName'])
                    
                    submit = st.form_submit_button("Add to the catalogue", use_container_width=True)

                if submit:
                    if not title.strip() or not isbn.strip():
                        st.error("Title and ISBN are required.")
                    else:
                        new_id = db.add_book(
                            isbn, 
                            title, 
                            int(year), 
                            publisher['PublisherID'], 
                            category['CategoryID'], 
                            [a['AuthorID'] for a in chosen], 
                            int(copies)
                        )
                        st.session_state["book_added_success"] = f"Book '{title.strip()}' has been added successfully! (Assigned ID #{new_id})"
                        st.toast(f"Added '{title.strip()}' successfully!", icon="✅")
                        st.rerun()
        except Exception as exc:
            st.error(f"Could not prepare the form: {exc}")

    # 3. ADD AUTHOR / PUBLISHER / CATEGORY
    with master_add_tab:
        # Show persisted success banner if master record was just added
        if st.session_state.get("master_data_success"):
            st.success(st.session_state.pop("master_data_success"))

        st.markdown("<div class='section-heading'>Register Master Catalog Data</div>", unsafe_allow_html=True)
        tab_author, tab_pub, tab_cat = st.tabs(["＋ New Author", "＋ New Publisher", "＋ New Category"])

        with tab_author:
            with st.form("quick_add_author_main", clear_on_submit=True):
                qa_name = st.text_input("Author Name *", placeholder="e.g., Robert Martin")
                qa_nationality = st.text_input("Nationality (optional)", placeholder="e.g., American")
                qa_submit = st.form_submit_button("Save Author to Database", use_container_width=True)

            if qa_submit:
                if not qa_name.strip():
                    st.error("Please provide an author name.")
                else:
                    new_auth_id = db.add_author(qa_name.strip(), qa_nationality.strip())
                    st.session_state["master_data_success"] = f"Author '{qa_name.strip()}' has been added successfully! (Author ID #{new_auth_id})"
                    st.toast(f"Author '{qa_name.strip()}' registered!", icon="✅")
                    st.rerun()

        with tab_pub:
            with st.form("quick_add_publisher_main", clear_on_submit=True):
                qp_name = st.text_input("Publisher Name *", placeholder="e.g., Pearson Education")
                qp_city = st.text_input("City / Location (optional)", placeholder="e.g., London")
                qp_submit = st.form_submit_button("Save Publisher to Database", use_container_width=True)

            if qp_submit:
                if not qp_name.strip():
                    st.error("Please provide a publisher name.")
                else:
                    new_pub_id = db.add_publisher(qp_name.strip(), qp_city.strip())
                    st.session_state["master_data_success"] = f"Publisher '{qp_name.strip()}' has been added successfully! (Publisher ID #{new_pub_id})"
                    st.toast(f"Publisher '{qp_name.strip()}' registered!", icon="✅")
                    st.rerun()

        with tab_cat:
            with st.form("quick_add_category_main", clear_on_submit=True):
                qc_name = st.text_input("Category / Subject *", placeholder="e.g., Algorithms")
                qc_submit = st.form_submit_button("Save Category to Database", use_container_width=True)

            if qc_submit:
                if not qc_name.strip():
                    st.error("Please provide a category name.")
                else:
                    new_cat_id = db.add_category(qc_name.strip())
                    st.session_state["master_data_success"] = f"Category '{qc_name.strip()}' has been created successfully! (Category ID #{new_cat_id})"
                    st.toast(f"Category '{qc_name.strip()}' created!", icon="✅")
                    st.rerun()

    # 4. MANAGE TITLES
    with manage:
        if st.session_state.get("manage_book_success"):
            st.success(st.session_state.pop("manage_book_success"))

        try:
            rows = db.book_list()
            if not rows:
                st.info("There are no titles to manage yet.")
            else:
                selected = st.selectbox("Choose a title to edit or remove", rows, format_func=lambda x: f"{x['BookID']} · {x['Title']}")
                st.markdown("<div class='paper-card'>Only title and publication year can be edited here. Titles with active loans or physical copy histories are protected by MySQL constraints.</div>", unsafe_allow_html=True)
                
                with st.form("edit_book_form"):
                    title = st.text_input("Title", value=selected['Title'])
                    year_val = selected.get('PublicationYear') or 2024
                    year = st.number_input("Publication year", min_value=1450, max_value=2100, value=int(year_val), step=1)
                    update = st.form_submit_button("Save Changes")

                if update:
                    if not title.strip():
                        st.error("Title cannot be empty.")
                    else:
                        db.update_book(selected['BookID'], title.strip(), int(year))
                        st.session_state["manage_book_success"] = f"Title #{selected['BookID']} updated successfully."
                        st.rerun()

                confirm = st.checkbox("I confirm I want to permanently delete this title", key="confirm_delete_book")
                if st.button("Delete Selected Title", disabled=not confirm):
                    try:
                        db.delete_book(selected['BookID'])
                        st.session_state["manage_book_success"] = f"Book title deleted successfully."
                        st.rerun()
                    except Exception as exc:
                        st.error(str(exc))
        except Exception as exc:
            st.error(f"Could not load titles: {exc}")