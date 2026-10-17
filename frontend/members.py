import streamlit as st
from backend import db
from frontend.styles import page_header


def render_members():
    page_header("THE READING COMMUNITY", "Library members", "Welcome readers, keep their contact details up to date, and manage memberships from one place.")
    directory, register, manage=st.tabs(["♙ Reader directory","＋ Register a reader","⚙ Manage membership"])
    with directory:
        term=st.text_input("Find a reader",placeholder="Name, email, or phone",key="member_search")
        try:
            rows=db.list_members()
            if term.strip(): rows=[r for r in rows if term.lower() in ' '.join(str(v or '') for v in r.values()).lower()]
            st.caption(f"{len(rows)} reader(s)")
            if rows:
                for r in rows:
                    import html
                    name=html.escape(str(r.get('MemberName') or 'Unnamed reader')); email=html.escape(str(r.get('Email') or 'No email')); phone=html.escape(str(r.get('Phone') or 'No phone'))
                    joined=r.get('JoinDate'); joined=joined.strftime('%d %b %Y') if hasattr(joined,'strftime') else str(joined or '—')
                    st.markdown(f"<div class='paper-card' style='display:flex;gap:.9rem;align-items:center'><div class='book-spine' style='height:48px;width:48px;min-width:48px;border-radius:50%'>♙</div><div style='flex:1'><div class='book-title'>{name}</div><div class='book-meta'>{email}<br>{phone}</div></div><div style='text-align:right'><span class='pill'>Reader #{r['MemberID']}</span><div class='tiny-note' style='margin-top:.4rem'>Joined {html.escape(joined)}</div></div></div>",unsafe_allow_html=True)
            else: st.markdown("<div class='empty-state'>No matching readers. Try another search or register a new member.</div>",unsafe_allow_html=True)
        except Exception as exc: st.error(f"Could not load members: {exc}")
    with register:
        with st.form("register_member",clear_on_submit=True):
            name=st.text_input("Full name *",placeholder="Reader full name"); email=st.text_input("Email address *",placeholder="reader@example.com"); phone=st.text_input("Phone number (optional)")
            submit=st.form_submit_button("Register reader",use_container_width=True)
        if submit:
            try:
                if not name.strip() or not email.strip():
                    st.error("Full name and email address are required.")
                else:
                    member_id=db.add_member(name.strip(),email.strip(),phone.strip())
                    st.success(f"Reader registered in MySQL · Member ID {member_id}")
                    st.rerun()
            except Exception as exc: st.error(f"Could not register reader: {exc}")
    with manage:
        try:
            rows=db.list_members()
            if rows:
                selected=st.selectbox("Choose a reader",rows,format_func=lambda x:f"{x['MemberID']} · {x['MemberName']}")
                with st.form("edit_member"):
                    name=st.text_input("Full name",value=selected['MemberName']); email=st.text_input("Email",value=selected['Email']); phone=st.text_input("Phone",value=selected.get('Phone') or '')
                    update=st.form_submit_button("Save reader details")
                if update:
                    try: db.update_member(selected['MemberID'],name.strip(),email.strip(),phone.strip()); st.success("Member details updated."); st.rerun()
                    except Exception as exc: st.error(str(exc))
                confirm=st.checkbox("Confirm membership deletion",key="confirm_member_delete")
                if st.button("Delete member",disabled=not confirm):
                    try: db.delete_member(selected['MemberID']); st.success("Member deleted."); st.rerun()
                    except Exception as exc: st.error(str(exc))
            else: st.info("Register a reader before managing memberships.")
        except Exception as exc: st.error(f"Could not load membership records: {exc}")
