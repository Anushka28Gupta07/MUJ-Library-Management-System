import streamlit as st
import pandas as pd

def render_search():
    st.title("🔍 Search Catalog")
    st.write("Lookup books across titles, authors, publishers, or categories.")

    search_query = st.text_input("Enter search keywords...", placeholder="e.g., Algorithms, Kernighan, Database, Pearson")

    all_books = [
        {"BookID": 101, "Title": "The C Programming Language", "Author": "Brian Kernighan", "Category": "Programming", "Publisher": "Pearson", "Year": 1988, "Status": "Available"},
        {"BookID": 102, "Title": "Introduction to Algorithms", "Author": "Thomas Cormen", "Category": "Programming", "Publisher": "McGraw Hill", "Year": 2022, "Status": "Issued"},
        {"BookID": 103, "Title": "Database System Concepts", "Author": "Abraham Silberschatz", "Category": "Database Systems", "Publisher": "McGraw Hill", "Year": 2019, "Status": "Available"},
        {"BookID": 104, "Title": "Clean Code", "Author": "Robert Martin", "Category": "Programming", "Publisher": "Pearson", "Year": 2008, "Status": "Available"},
        {"BookID": 105, "Title": "Mathematics for Engineers", "Author": "R. D. Sharma", "Category": "Mathematics", "Publisher": "Pearson", "Year": 2023, "Status": "Available"},
        {"BookID": 106, "Title": "The Pragmatic Programmer", "Author": "Robert Martin", "Category": "Programming", "Publisher": "OReilly Media", "Year": 2019, "Status": "Maintenance"}
    ]

    df = pd.DataFrame(all_books)

    if search_query.strip():
        filtered_df = df[
            df["Title"].str.contains(search_query, case=False, na=False) |
            df["Author"].str.contains(search_query, case=False, na=False) |
            df["Category"].str.contains(search_query, case=False, na=False) |
            df["Publisher"].str.contains(search_query, case=False, na=False)
        ]
        if not filtered_df.empty:
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
            st.caption(f"Showing {len(filtered_df)} matching record(s).")
        else:
            st.warning(f"No results found for '{search_query}'.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption("Showing complete collection (6 titles registered).")