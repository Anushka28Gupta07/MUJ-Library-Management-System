import streamlit as st

def render_master_data():
    st.title("⚙️ Master Data Management")
    st.write("Maintain foundational library entities (Authors, Publishers, Categories).")

    tab1, tab2, tab3 = st.tabs(["✍️ Authors", "🏢 Publishers", "🏷️ Categories"])

    with tab1:
        st.subheader("Add Author")
        with st.form("author_form"):
            aname = st.text_input("Author Name *")
            nat = st.text_input("Nationality")
            if st.form_submit_button("Save Author"):
                if aname:
                    st.success(f"Author '{aname}' added successfully!")
                else:
                    st.error("Author Name is required.")

    with tab2:
        st.subheader("Add Publisher")
        with st.form("publisher_form"):
            pname = st.text_input("Publisher Name *")
            city = st.text_input("City")
            if st.form_submit_button("Save Publisher"):
                if pname:
                    st.success(f"Publisher '{pname}' added successfully!")
                else:
                    st.error("Publisher Name is required.")

    with tab3:
        st.subheader("Add Category")
        with st.form("cat_form"):
            cname = st.text_input("Category Name (Unique) *")
            if st.form_submit_button("Save Category"):
                if cname:
                    st.success(f"Category '{cname}' added successfully!")
                else:
                    st.error("Category Name is required.")