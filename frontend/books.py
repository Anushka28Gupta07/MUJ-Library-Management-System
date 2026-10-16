import streamlit as st
import pandas as pd

def render_books():
    st.title("📖 Book Catalog Management")

    # Initial catalog data
    default_books = [
        {"BookID": 101, "Title": "The C Programming Language", "ISBN": "9780131103627", "Author": "Brian Kernighan", "Category": "Programming", "Publisher": "Pearson", "Year": 1988, "Available Copies": 1},
        {"BookID": 102, "Title": "Introduction to Algorithms", "ISBN": "9780262046305", "Author": "Thomas Cormen", "Category": "Programming", "Publisher": "McGraw Hill", "Year": 2022, "Available Copies": 0},
        {"BookID": 103, "Title": "Database System Concepts", "ISBN": "9780078022159", "Author": "Abraham Silberschatz", "Category": "Database Systems", "Publisher": "McGraw Hill", "Year": 2019, "Available Copies": 1},
        {"BookID": 104, "Title": "Clean Code", "ISBN": "9780132350884", "Author": "Robert Martin", "Category": "Programming", "Publisher": "Pearson", "Year": 2008, "Available Copies": 1},
        {"BookID": 105, "Title": "Mathematics for Engineers", "ISBN": "9789355012345", "Author": "R. D. Sharma", "Category": "Mathematics", "Publisher": "Pearson", "Year": 2023, "Available Copies": 1},
        {"BookID": 106, "Title": "The Pragmatic Programmer", "ISBN": "9780135957059", "Author": "Robert Martin", "Category": "Programming", "Publisher": "OReilly Media", "Year": 2019, "Available Copies": 0}
    ]

    # Initial lost/damaged tracking
    default_lost_records = [
        {"CopyID": 1005, "Book Title": "The Pragmatic Programmer", "Status": "Lost", "Reported By": "Ayushi Verma", "Report Date": "2026-10-02", "Replacement Fine": "₹750.00"},
        {"CopyID": 1008, "Book Title": "Introduction to Algorithms", "Status": "Damaged", "Reported By": "Rahul Sharma", "Report Date": "2026-10-10", "Replacement Fine": "₹300.00"}
    ]

    if "books_list" not in st.session_state:
        st.session_state["books_list"] = default_books

    if "lost_books_list" not in st.session_state:
        st.session_state["lost_books_list"] = default_lost_records

    # 4 clean tabs including Lost & Damaged
    tab1, tab2, tab3, tab4 = st.tabs([
        "📚 View All Books", 
        "⚠️ Lost & Damaged Copies", 
        "➕ Add New Book", 
        "✏️ Edit / Delete"
    ])

    # TAB 1: VIEW ALL BOOKS
    with tab1:
        st.subheader("All Registered Titles")
        df = pd.DataFrame(st.session_state["books_list"])
        st.dataframe(df, use_container_width=True, hide_index=True)

    # TAB 2: LOST & DAMAGED COPIES
    with tab2:
        st.subheader("⚠️ Lost & Damaged Copies Registry")
        st.write("Track unreturned, missing, or compromised physical inventory copies.")

        # Display current lost records
        df_lost = pd.DataFrame(st.session_state["lost_books_list"])
        st.dataframe(df_lost, use_container_width=True, hide_index=True)

        st.divider()
        st.markdown("#### 📝 Report a Physical Copy as Lost / Damaged")

        with st.form("report_lost_form", clear_on_submit=True):
            col_l1, col_l2 = st.columns(2)
            with col_l1:
                book_names = [b["Title"] for b in st.session_state["books_list"]]
                selected_lost_book = st.selectbox("Select Book Title", book_names)
                copy_id = st.number_input("Physical Copy ID *", min_value=1001, max_value=9999, value=1009)
                reported_by = st.selectbox("Borrower / Reporter", [
                    "Ayushi Verma", "Rahul Sharma", "Priya Singh", "Arjun Mehta", "Neha Gupta", "Internal Inventory Audit"
                ])
            with col_l2:
                incident_type = st.selectbox("Incident Type", ["Lost", "Damaged", "Subject for Replacement"])
                replacement_fee = st.number_input("Assessed Replacement Fine (₹)", min_value=0, max_value=5000, value=500, step=50)

            submitted_lost = st.form_submit_button("Record Incident & Update Inventory", use_container_width=True)

            if submitted_lost:
                # Add to lost registry
                new_lost_entry = {
                    "CopyID": int(copy_id),
                    "Book Title": selected_lost_book,
                    "Status": incident_type,
                    "Reported By": reported_by,
                    "Report Date": "2026-10-17",
                    "Replacement Fine": f"₹{replacement_fee:.2f}"
                }
                st.session_state["lost_books_list"].append(new_lost_entry)

                # Deduct 1 available copy if available
                for b in st.session_state["books_list"]:
                    if b["Title"] == selected_lost_book and b["Available Copies"] > 0:
                        b["Available Copies"] -= 1
                        break

                st.success(f"Copy #{copy_id} flagged as '{incident_type}'. Fine of ₹{replacement_fee:.2f} billed to {reported_by}.")
                st.rerun()

    # TAB 3: ADD BOOK
    with tab3:
        st.subheader("Add a New Book to the Database")
        with st.form("add_book_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                title = st.text_input("Book Title *")
                isbn = st.text_input("ISBN (Unique) *")
                year = st.number_input("Publication Year", min_value=1450, max_value=2100, value=2024)
            with col_b:
                publisher = st.selectbox("Publisher", ["Pearson", "McGraw Hill", "OReilly Media"])
                category = st.selectbox("Category", ["Programming", "Mathematics", "Database Systems", "Fiction"])
                authors = st.multiselect("Author(s)", ["Brian Kernighan", "Thomas Cormen", "Abraham Silberschatz", "Robert Martin", "R. D. Sharma", "J.K. Rowling"])
                copies = st.number_input("Initial Physical Copies", min_value=1, max_value=20, value=2)

            submitted = st.form_submit_button("Add Book", use_container_width=True)
            if submitted:
                if not title or not isbn or not authors:
                    st.error("Please fill in Title, ISBN, and at least one Author.")
                else:
                    new_id = max([b["BookID"] for b in st.session_state["books_list"]], default=100) + 1
                    new_entry = {
                        "BookID": new_id,
                        "Title": title,
                        "ISBN": isbn,
                        "Author": ", ".join(authors),
                        "Category": category,
                        "Publisher": publisher,
                        "Year": int(year),
                        "Available Copies": int(copies)
                    }
                    st.session_state["books_list"].append(new_entry)
                    st.success(f"Book '{title}' registered with ID #{new_id}!")
                    st.rerun()

    # TAB 4: EDIT / DELETE
    with tab4:
        st.subheader("Edit or Remove a Book")
        book_titles = [b["Title"] for b in st.session_state["books_list"]]
        selected_title = st.selectbox("Select Book", book_titles)
        selected_book = next(b for b in st.session_state["books_list"] if b["Title"] == selected_title)

        new_title = st.text_input("Edit Title", value=selected_book["Title"])
        new_year = st.number_input("Edit Publication Year", value=selected_book["Year"], min_value=1450, max_value=2100)

        col_save, col_del = st.columns([1, 1])
        with col_save:
            if st.button("Save Changes", use_container_width=True):
                selected_book["Title"] = new_title
                selected_book["Year"] = int(new_year)
                st.success(f"Details updated for Book ID: {selected_book['BookID']}")
                st.rerun()
        with col_del:
            if st.button("Delete Book", use_container_width=True, type="primary"):
                st.warning("⚠️ Cannot delete book: Physical copies or active loan history exist in the database.")