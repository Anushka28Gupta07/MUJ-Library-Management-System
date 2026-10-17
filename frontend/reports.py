import streamlit as st
import pandas as pd
from backend import db
from frontend.styles import page_header


def _report(label, function, key, description):
    st.markdown(f"<div class='section-heading'>{label}</div><div class='page-intro'>{description}</div>",unsafe_allow_html=True)
    try:
        rows=function()
        if rows:
            frame=pd.DataFrame(rows)
            st.caption(f"{len(frame)} record(s)")
            # Use expandable record cards instead of a default dark database table.
            for index,row in enumerate(rows):
                primary=next((row[k] for k in ('Title','MemberName','LoanID','BookID','CategoryName') if row.get(k) not in (None,'')),f"Record {index+1}")
                details=' · '.join(f"{k.replace('_',' ')}: {v.strftime('%d %b %Y') if hasattr(v,'strftime') else v}" for k,v in row.items() if v not in (None,'') and k not in ('Title','MemberName'))
                import html
                st.markdown(f"<div class='paper-card'><div class='book-title'>{html.escape(str(primary))}</div><div class='book-meta'>{html.escape(details)}</div></div>",unsafe_allow_html=True)
            st.download_button(f"Download {label.lower()} as CSV",frame.to_csv(index=False).encode('utf-8-sig'),file_name=f"{key}.csv",mime='text/csv',key=f"download_{key}")
        else: st.markdown("<div class='empty-state'>No records for this report right now.</div>",unsafe_allow_html=True)
    except Exception as exc: st.error(f"Could not generate report: {exc}")


def render_reports():
    page_header("THE LIBRARIAN'S LEDGER", "Reports & insights", "Useful operational reports generated from live MySQL data. Download any report as a CSV when you need to share or analyse it.")
    issued,overdue,popular,fines=st.tabs(["Current loans","Overdue","Popular titles","Fines"])
    with issued: _report("Currently issued volumes",db.report_issued,"currently_issued_books","See which volumes are out and who has borrowed them.")
    with overdue: _report("Overdue volumes",db.report_overdue,"overdue_books","Review late returns and the current estimated fine for each open loan.")
    with popular: _report("Most borrowed titles",db.report_most_issued,"most_issued_titles","Understand which titles are being borrowed most often.")
    with fines: _report("Fines recorded",db.report_fines,"library_fines","Review completed loan records with fines greater than zero.")
