import streamlit as st
import pandas as pd

def render_members():
    st.title("👥 Member Management")

    tab1, tab2, tab3 = st.tabs(["📋 View All Members", "➕ Register Member", "✏️ Edit / Delete"])

    members_data = [
        {"MemberID": 201, "MemberName": "Ayushi Verma", "Email": "ayushi@example.com", "Phone": "9876543210", "JoinDate": "2026-01-10"},
        {"MemberID": 202, "MemberName": "Rahul Sharma", "Email": "rahul@example.com", "Phone": "9876543211", "JoinDate": "2026-01-15"},
        {"MemberID": 203, "MemberName": "Priya Singh", "Email": "priya@example.com", "Phone": "9876543212", "JoinDate": "2026-02-01"},
        {"MemberID": 204, "MemberName": "Arjun Mehta", "Email": "arjun@example.com", "Phone": "9876543213", "JoinDate": "2026-02-12"},
        {"MemberID": 205, "MemberName": "Neha Gupta", "Email": "neha@example.com", "Phone": "9876543214", "JoinDate": "2026-03-05"}
    ]

    with tab1:
        st.subheader("Registered Library Members")
        st.dataframe(pd.DataFrame(members_data), use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("Register a New Member")
        with st.form("add_member_form"):
            name = st.text_input("Full Name *")
            email = st.text_input("Email Address (Unique) *")
            phone = st.text_input("Phone Number")
            submit = st.form_submit_button("Register Member", use_container_width=True)

            if submit:
                if not name or not email:
                    st.error("Name and Email are mandatory fields.")
                else:
                    st.success(f"Member '{name}' successfully registered with ID #206!")

    with tab3:
        st.subheader("Edit or Remove Member")
        names = [m["MemberName"] for m in members_data]
        selected_name = st.selectbox("Select Member", names)
        member = next(m for m in members_data if m["MemberName"] == selected_name)

        edit_email = st.text_input("Email", value=member["Email"])
        edit_phone = st.text_input("Phone", value=member["Phone"])

        col_s, col_d = st.columns(2)
        with col_s:
            if st.button("Update Member", use_container_width=True):
                st.success("Member record updated successfully.")
        with col_d:
            if st.button("Delete Member", use_container_width=True, type="primary"):
                st.warning("⚠️ Rejection: Foreign Key constraint failed. Member has active or historical loans.")