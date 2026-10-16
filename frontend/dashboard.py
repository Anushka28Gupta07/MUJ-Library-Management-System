import streamlit as st
import pandas as pd

def render_dashboard():
    st.title("📊 Library Dashboard")
    st.write("Overview of current library inventory, active loans, and collections.")

    # 1. Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Book Titles", value="6")
    with col2:
        st.metric(label="Total Physical Copies", value="8")
    with col3:
        st.metric(label="Currently Issued", value="3", delta="-1 returned today")
    with col4:
        st.metric(label="Registered Members", value="5")

    st.divider()

    # 2. Charts Section
    col_chart1, col_chart2 = st.columns([2, 1])

    with col_chart1:
        st.subheader("📚 Books by Category")
        category_data = pd.DataFrame({
            "Category": ["Programming", "Mathematics", "Database Systems", "Fiction"],
            "Count": [3, 1, 1, 0]
        })
        st.bar_chart(category_data.set_index("Category"))

    with col_chart2:
        st.subheader("📌 Quick Status")
        st.info("💡 **Tip:** Use the sidebar menu to issue or return physical copies.")
        st.write("**Total Overdue Fines Pending:** ₹80.00")
        st.write("**Copies in Maintenance:** 1 (Pragmatic Programmer)")