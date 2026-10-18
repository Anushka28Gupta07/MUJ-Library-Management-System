import streamlit as st


def apply_custom_styles():
    """
    Editorial Dark Academia theme:
    Refined charcoal base, glowing gold/bronze accents, card elevation,
    and crisp high-contrast data rows inspired by institutional dashboards.
    """
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Inter:wght@400;500;600;700&display=swap');

        /* Base Application Canvas */
        .stApp, [data-testid="stAppViewContainer"] {
            background: radial-gradient(circle at 50% 0%, #151c28 0%, #0c1017 100%) !important;
            color: #e2e8f0 !important;
            font-family: 'Inter', -apple-system, sans-serif !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        /* Sidebar: Deep Midnight Onyx */
        [data-testid="stSidebar"] {
            background-color: #080b10 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        }

        [data-testid="stSidebar"] * {
            color: #e2e8f0 !important;
        }

        /* Input Controls */
        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div,
        input, textarea, select {
            background-color: #131924 !important;
            color: #f8fafc !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 8px !important;
        }

        /* Action Buttons */
        .stButton > button {
            background: linear-gradient(180deg, #1f2937 0%, #111827 100%) !important;
            color: #f1f5f9 !important;
            border: 1px solid rgba(212, 175, 55, 0.35) !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 0.5rem 1.25rem !important;
            transition: all 0.2s ease !important;
        }

        .stButton > button:hover {
            border-color: #e2b357 !important;
            box-shadow: 0 0 12px rgba(226, 179, 87, 0.25) !important;
            color: #ffffff !important;
        }

        /* Form Container */
        div[data-testid="stForm"] {
            background-color: #121722 !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4) !important;
        }

        /* Editorial Paper / Glass Cards */
        .paper-card {
            background: linear-gradient(180deg, #161e2c 0%, #101621 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 10px !important;
            padding: 1rem 1.25rem !important;
            margin-bottom: 0.85rem !important;
            color: #f1f5f9 !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
        }

        .stat-card-box {
            background: linear-gradient(180deg, #161e2c 0%, #101621 100%) !important;
            border: 1px solid rgba(212, 175, 55, 0.2) !important;
            border-radius: 10px !important;
            padding: 1.25rem 1rem !important;
            text-align: center !important;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
        }

        .book-card-title {
            font-family: 'Cinzel', serif !important;
            font-size: 1.15rem !important;
            font-weight: 700 !important;
            color: #f8fafc !important;
        }

        .section-heading {
            font-family: 'Cinzel', serif;
            font-size: 1.2rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            color: #e2b357;
            margin: 1.5rem 0 0.85rem 0;
            text-transform: uppercase;
        }

        .pill {
            background: rgba(226, 179, 87, 0.12);
            color: #e2b357;
            border: 1px solid rgba(226, 179, 87, 0.3);
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 0.78rem;
            font-weight: 600;
        }

        .activity-row {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 0.75rem 0.5rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }

        .activity-avatar {
            font-size: 1.25rem;
            background: rgba(255, 255, 255, 0.05);
            padding: 0.4rem;
            border-radius: 8px;
        }

        .activity-title {
            color: #f1f5f9;
            font-size: 0.92rem;
        }

        .activity-sub {
            color: #94a3b8;
            font-size: 0.82rem;
        }

        .activity-time {
            color: #64748b;
            font-size: 0.8rem;
            white-space: nowrap;
        }

        .empty-state {
            padding: 2.5rem;
            text-align: center;
            color: #94a3b8;
            border: 1px dashed rgba(255, 255, 255, 0.12);
            border-radius: 10px;
            margin: 1rem 0;
        }

        .tiny-note {
            font-size: 0.75rem;
            color: #64748b;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def page_header(*args, **kwargs):
    tag = ""
    title = ""
    subtitle = ""

    if len(args) == 1:
        title = args[0]
    elif len(args) == 2:
        title, subtitle = args[0], args[1]
    elif len(args) >= 3:
        tag, title, subtitle = args[0], args[1], args[2]

    tag = kwargs.get("tag", tag)
    title = kwargs.get("title", title)
    subtitle = kwargs.get("subtitle", subtitle)

    tag_html = f"<div style='font-size: 0.72rem; letter-spacing: 0.16em; text-transform: uppercase; color: #e2b357; font-weight: 700; margin-bottom: 0.3rem;'>{tag}</div>" if tag else ""
    subtitle_html = f"<div style='font-size: 0.92rem; color: #94a3b8;'>{subtitle}</div>" if subtitle else ""

    st.markdown(
        f"""
        <div style='margin-bottom: 1.75rem;'>
            {tag_html}
            <h2 style='font-family: \"Cinzel\", serif; margin-top: 0.1rem; margin-bottom: 0.35rem; color: #f8fafc; font-size: 1.9rem;'>{title}</h2>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True
    )


def stat_card(*args, **kwargs):
    if len(args) == 3:
        a, b, c = args
        if len(str(a)) <= 3:
            icon, value, label = a, b, c
        else:
            label, value, icon = a, b, c
    elif len(args) == 2:
        icon = "✦"
        value, label = args[0], args[1]
    else:
        icon = kwargs.get("icon", "✦")
        value = kwargs.get("value", "0")
        label = kwargs.get("label", "")

    st.markdown(
        f"""
        <div class='stat-card-box'>
            <div style='font-size: 1.35rem; color: #e2b357; margin-bottom: 0.35rem;'>{icon}</div>
            <div style='font-size: 2rem; font-weight: 700; margin: 0.2rem 0; color: #ffffff;'>{value}</div>
            <div style='font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em; color: #94a3b8; font-weight: 600;'>{label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def book_card(book):
    title = book.get("Title", "Untitled")
    authors = book.get("Authors") or "Unknown Author"
    isbn = book.get("ISBN", "—")
    category = book.get("CategoryName", "General")
    publisher = book.get("PublisherName", "—")
    year = book.get("PublicationYear", "—")
    available = book.get("AvailableCopies", 0)
    total = book.get("TotalCopies", 0)

    st.markdown(
        f"""
        <div class='paper-card'>
            <div style='display: flex; justify-content: space-between; align-items: flex-start; gap: 0.75rem;'>
                <div>
                    <div class='book-card-title'>{title}</div>
                    <div style='font-size: 0.85rem; color: #94a3b8; margin-top: 0.3rem;'>By {authors} · {year}</div>
                </div>
                <span class='pill'>{category}</span>
            </div>
            <div style='display: flex; justify-content: space-between; margin-top: 1rem; padding-top: 0.75rem; border-top: 1px solid rgba(255, 255, 255, 0.08); font-size: 0.82rem; color: #94a3b8;'>
                <span>ISBN: <strong style='color: #cbd5e1;'>{isbn}</strong></span>
                <span>Publisher: <strong style='color: #cbd5e1;'>{publisher}</strong></span>
                <span>Copies: <strong style='color: #e2b357;'>{available} / {total} available</strong></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )