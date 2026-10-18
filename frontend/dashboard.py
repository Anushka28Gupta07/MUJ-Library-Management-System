import streamlit as st
import base64
from pathlib import Path
import html
from backend import db
from frontend.styles import stat_card, book_card


def get_base64_image(image_path):
    """Encodes a local image to base64 so Streamlit can embed it directly."""
    if Path(image_path).exists():
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None


def render_dashboard():
    # ---------------------------------------------------------
    # 1. TOP HERO BANNER (Banner.jpeg)
    # ---------------------------------------------------------
    banner_path = Path(__file__).parent / "Banner.jpeg"
    b64_banner = get_base64_image(banner_path)

    if b64_banner:
        st.markdown(
            f"""
            <div style="
                border-radius: 12px;
                overflow: hidden;
                margin-bottom: 1.5rem;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.45);
                border: 1px solid rgba(255, 255, 255, 0.1);
            ">
                <img src="data:image/jpeg;base64,{b64_banner}" style="width: 100%; height: auto; display: block; object-fit: cover; max-height: 220px;" alt="Library Banner" />
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div class='hero'><div class='hero-kicker'>THE LIBRARY AT A GLANCE</div><h1>A little order.<br>A lot of wonder.</h1><p>Your collection, your readers, and today's lending activity — gathered in one calm place.</p><span class='hero-seal'>✦ LIVE COLLECTION OVERVIEW ✦</span></div>", 
            unsafe_allow_html=True
        )

    st.write("")

    # ---------------------------------------------------------
    # 2. STATS OVERVIEW
    # ---------------------------------------------------------
    try:
        stats = db.dashboard_stats() or {}
        titles = int(stats.get('titles') or 0)
        copies = int(stats.get('copies') or 0)
        issued = int(stats.get('issued') or 0)
        members = int(stats.get('members') or 0)
        cols = st.columns(4, gap="medium")
        cards = [
            ("✧", f"{titles:,}", "Unique book titles"),
            ("♙", f"{members:,}", "Registered readers"),
            ("↗", f"{issued:,}", "Copies currently out"),
            ("▤", f"{max(copies - issued, 0):,}", "Copies on the shelves")
        ]
        for col, (icon, value, label) in zip(cols, cards):
            with col:
                stat_card(icon, value, label)
    except Exception as exc:
        st.error("The dashboard could not read live statistics from MySQL.")
        st.caption(str(exc))
        return

    st.markdown("<div class='section-heading'>✦ Around the collection</div>", unsafe_allow_html=True)
    left, right = st.columns([1, 1], gap="large")

    # ---------------------------------------------------------
    # 3. BOOKS BY CATEGORY
    # ---------------------------------------------------------
    with left:
        st.markdown("#### Books by category")
        try:
            rows = db.books_per_category()
            if rows:
                for row in rows:
                    count = int(row.get('book_count') or 0)
                    name = str(row.get('CategoryName') or 'Uncategorised')
                    st.markdown(
                        f"<div class='paper-card' style='padding:.75rem 1rem;display:flex;align-items:center;gap:.8rem'>"
                        f"<span style='color:#a93c42;font-size:1.1rem'>✦</span>"
                        f"<div style='flex:1;color:#cbd5e1;font-weight:600'>{name}</div>"
                        f"<span class='pill'>{count} title(s)</span></div>",
                        unsafe_allow_html=True
                    )
            else:
                st.markdown("<div class='empty-state'>No categories have been added yet.</div>", unsafe_allow_html=True)
        except Exception as exc:
            st.info(f"Category overview unavailable: {exc}")

    # ---------------------------------------------------------
    # 4. RECENT LENDING ACTIVITY
    # ---------------------------------------------------------
    with right:
        st.markdown("#### Recent lending activity")
        try:
            rows = db._fetch_all(
                """SELECT l.LoanID, b.Title, m.MemberName, l.IssueDate, l.ReturnDate, l.DueDate 
                   FROM Loan l 
                   JOIN Book_Copy bc ON l.CopyID=bc.CopyID 
                   JOIN Book b ON bc.BookID=b.BookID 
                   JOIN Member m ON l.MemberID=m.MemberID 
                   ORDER BY COALESCE(l.ReturnDate, l.IssueDate) DESC, l.LoanID DESC 
                   LIMIT 5"""
            )
            if rows:
                for row in rows:
                    action = "Returned" if row.get('ReturnDate') else "Issued"
                    dt = row.get('ReturnDate') or row.get('IssueDate')
                    date_text = dt.strftime('%d %b %Y') if hasattr(dt, 'strftime') else str(dt or 'Date unavailable')
                    title = str(row.get('Title') or 'Untitled')
                    member = str(row.get('MemberName') or 'Unknown member')
                    st.markdown(
                        f"<div class='activity-row'>"
                        f"<div class='activity-avatar'>📖</div>"
                        f"<div style='min-width:0;flex:1'>"
                        f"<div class='activity-title'><b>{html.escape(action)}:</b> {html.escape(title)}</div>"
                        f"<div class='activity-sub'>{html.escape(member)}</div>"
                        f"</div>"
                        f"<div class='activity-time'>{html.escape(date_text)}</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
            else:
                st.markdown("<div class='empty-state'>Your first lending record will appear here.</div>", unsafe_allow_html=True)
        except Exception as exc:
            st.info(f"Recent activity unavailable: {exc}")

    st.markdown("<div class='tiny-note' style='margin-top:1rem'>All figures above are calculated from your connected MySQL database.</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-heading'>A few volumes to begin with</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 5. FEATURED BOOKS
    # ---------------------------------------------------------
    try:
        books = db.book_list()[:3]
        if books:
            cols = st.columns(min(3, len(books)), gap="medium")
            for col, row in zip(cols, books):
                with col:
                    book_card(row)
        else:
            st.info("The catalogue is empty. Add your first title in Catalogue.")
    except Exception as exc:
        st.info(f"Could not load featured books: {exc}")
