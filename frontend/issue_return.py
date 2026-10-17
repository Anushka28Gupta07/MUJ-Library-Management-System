import streamlit as st
from backend import db
from frontend.styles import page_header


def render_issue_return():
    page_header("THE CIRCULATION DESK", "Issue & return", "Keep lending simple: issue an available copy, record returns, and let the backend calculate overdue fines.")
    issue_tab,return_tab=st.tabs(["↗ Issue a volume","↙ Record a return"])
    with issue_tab:
        try:
            members=db.list_member_names(); available=db.available_books()
            if not members: st.warning("Register a member before issuing a book.")
            elif not available: st.info("There are no available copies at the moment.")
            else:
                st.markdown("<div class='paper-card'><b style='color:#681f2d'>Lending terms</b><div class='book-meta'>Standard loan period: 14 days · Overdue fine: ₹2 per day</div></div>",unsafe_allow_html=True)
                with st.form("issue_book_form"):
                    member=st.selectbox("Reader",members,format_func=lambda x:f"{x['MemberName']} · Member #{x['MemberID']}")
                    book=st.selectbox("Volume",available,format_func=lambda x:f"{x['Title']} · {x['AvailableCopies']} available")
                    submit=st.form_submit_button("Confirm issue",use_container_width=True)
                if submit:
                    try: loan_id=db.issue_book(member['MemberID'],book['BookID']); st.success(f"Volume issued successfully · Loan ID {loan_id}"); st.rerun()
                    except Exception as exc: st.error(str(exc))
        except Exception as exc: st.error(f"Could not load the issue form: {exc}")
    with return_tab:
        try:
            loans=db.open_loans()
            if not loans: st.markdown("<div class='empty-state'>Every volume is accounted for — there are no open loans.</div>",unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='section-heading'>{len(loans)} open loan(s)</div>",unsafe_allow_html=True)
                for loan in loans:
                    fine=float(loan.get('CurrentFine') or 0); due=loan.get('DueDate'); due=due.strftime('%d %b %Y') if hasattr(due,'strftime') else str(due or '—')
                    import html
                    st.markdown(f"<div class='paper-card'><div style='display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap'><div><div class='book-title'>{html.escape(str(loan['Title']))}</div><div class='book-meta'>{html.escape(str(loan['MemberName']))} · Loan #{loan['LoanID']}<br>Due {html.escape(due)}</div></div><div><span class='pill {'pill-red' if fine else 'pill-green'}'>{'Fine ₹%.2f'%fine if fine else 'No fine due'}</span></div></div></div>",unsafe_allow_html=True)
                loan=st.selectbox("Select loan to return",loans,format_func=lambda x:f"Loan #{x['LoanID']} · {x['Title']} — {x['MemberName']}")
                st.info(f"Current estimated fine: ₹{float(loan.get('CurrentFine') or 0):.2f}. The final amount is calculated when the return is recorded.")
                if st.button("Record return",use_container_width=True):
                    try:
                        result=db.return_book(loan['LoanID']); st.success(f"Returned successfully · Overdue days: {result['OverdueDays']} · Fine: ₹{float(result['FineAmount']):.2f}"); st.rerun()
                    except Exception as exc: st.error(str(exc))
        except Exception as exc: st.error(f"Could not load open loans: {exc}")
