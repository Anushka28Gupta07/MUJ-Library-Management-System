import streamlit as st
import pandas as pd
from datetime import date, timedelta, datetime

def render_issue():
    st.title("📤 Issue a Book")
    st.write("Assign an available physical copy to an authorized library member.")

    with st.form("issue_book_form"):
        col1, col2 = st.columns(2)
        with col1:
            member = st.selectbox("Select Member", [
                "201 - Ayushi Verma",
                "202 - Rahul Sharma",
                "203 - Priya Singh",
                "204 - Arjun Mehta",
                "205 - Neha Gupta"
            ])
        with col2:
            book_copy = st.selectbox("Select Available Copy", [
                "Copy #1002 - The C Programming Language",
                "Copy #1004 - Database System Concepts",
                "Copy #1006 - Clean Code",
                "Copy #1007 - Mathematics for Engineers"
            ])

        issue_date = date.today()
        due_date = issue_date + timedelta(days=14)

        st.info(f"📅 **Issue Date:** {issue_date} | **Due Date (14 Days Standard):** {due_date}")

        submitted = st.form_submit_button("Confirm & Issue Copy", use_container_width=True)
        if submitted:
            st.success(f"Success! {book_copy} has been issued to {member}. Scheduled Due Date: {due_date}")


def render_return():
    st.title("📥 Return a Book & Clear Fines")
    st.write("Process returns, update inventory availability, and settle overdue penalties.")

    active_loans = [
        {"LoanID": 5001, "Member": "Ayushi Verma", "Book": "The C Programming Language", "CopyID": 1001, "IssueDate": "2026-09-01", "DueDate": "2026-09-15"},
        {"LoanID": 5002, "Member": "Rahul Sharma", "Book": "Introduction to Algorithms", "CopyID": 1003, "IssueDate": "2026-09-05", "DueDate": "2026-09-19"}
    ]

    st.subheader("Active Loans in Circulation")
    st.dataframe(pd.DataFrame(active_loans), use_container_width=True, hide_index=True)

    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        loan_options = {
            f"Loan #{l['LoanID']} - {l['Book']} ({l['Member']})": l for l in active_loans
        }
        selected_label = st.selectbox("Select Loan to Process", list(loan_options.keys()))
        selected_record = loan_options[selected_label]

    with col_b:
        return_date = st.date_input("Actual Return Date", value=date.today())

    # Live Fine Calculation
    due_date = datetime.strptime(selected_record["DueDate"], "%Y-%m-%d").date()
    fine_per_day = 2.00  # Rs. 2 per day rule

    if return_date > due_date:
        overdue_days = (return_date - due_date).days
        total_fine = overdue_days * fine_per_day
        st.error(f"⚠️ **Overdue Notice:** Book is **{overdue_days} days** overdue. Fine to collect: **₹{total_fine:.2f}** (@ ₹2.00/day).")
    else:
        st.success("✅ Book returned on or before due date. Zero fine accrued.")

    if st.button("Confirm Return & Update Database", use_container_width=True, type="primary"):
        st.balloons()
        st.success(f"Book '{selected_record['Book']}' (Copy #{selected_record['CopyID']}) status successfully reset to 'Available'!")