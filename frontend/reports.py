import streamlit as st
import pandas as pd

def render_reports():
    st.title("📑 System Reports & Audits")

    tab1, tab2, tab3, tab4 = st.tabs(["📤 Currently Issued", "⚠️ Overdue Loans", "🏆 Most Borrowed", "💰 Fine Summary"])

    with tab1:
        st.subheader("Books Currently Checked Out")
        issued = pd.DataFrame([
            {"CopyID": 1001, "Book": "The C Programming Language", "Borrower": "Ayushi Verma", "Due Date": "2026-09-15"},
            {"CopyID": 1003, "Book": "Introduction to Algorithms", "Borrower": "Rahul Sharma", "Due Date": "2026-09-19"}
        ])
        st.dataframe(issued, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("Loans Past Due Date")
        overdue = pd.DataFrame([
            {"LoanID": 5001, "Borrower": "Ayushi Verma", "Book": "The C Programming Language", "Due Date": "2026-09-15", "Days Overdue": "32 Days"}
        ])
        st.dataframe(overdue, use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("Most Frequently Borrowed Titles")
        popular = pd.DataFrame([
            {"Rank": 1, "Book Title": "Database System Concepts", "Times Borrowed": 14},
            {"Rank": 2, "Book Title": "The C Programming Language", "Times Borrowed": 11},
            {"Rank": 3, "Book Title": "Introduction to Algorithms", "Times Borrowed": 9}
        ])
        st.dataframe(popular, use_container_width=True, hide_index=True)

    with tab4:
        st.subheader("Outstanding Fines by Member")
        fines = pd.DataFrame([
            {"MemberID": 201, "Member": "Ayushi Verma", "Unpaid Fines": "₹56.00"},
            {"MemberID": 203, "Member": "Priya Singh", "Unpaid Fines": "₹50.00 (Paid)"},
            {"MemberID": 205, "Member": "Neha Gupta", "Unpaid Fines": "₹30.00 (Paid)"}
        ])
        st.dataframe(fines, use_container_width=True, hide_index=True)