import streamlit as st

def apply_custom_styles():
    """
    Standard dark theme styles without oversized min-height rules.
    """
    st.markdown(
        """
        <style>
        /* Base page background */
        .stApp, [data-testid="stAppViewContainer"] {
            background-color: #0b0f19 !important;
            color: #f8fafc !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #070a10 !important;
            border-right: 1px solid #26354a !important;
        }

        [data-testid="stSidebar"] * {
            color: #f8fafc !important;
        }

        /* High contrast text inputs and dropdowns */
        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div,
        input, textarea, select {
            background-color: #1e293b !important;
            color: #f8fafc !important;
            border: 1px solid #334155 !important;
            border-radius: 6px !important;
        }

        input::placeholder, textarea::placeholder {
            color: #94a3b8 !important;
            opacity: 0.8 !important;
        }

        /* Standard buttons */
        .stButton > button {
            background-color: #1e293b !important;
            color: #f8fafc !important;
            border: 1px solid #334155 !important;
            border-radius: 6px !important;
            font-weight: 500 !important;
        }

        /* Forms */
        div[data-testid="stForm"] {
            background-color: #151e2e !important;
            border: 1px solid #26354a !important;
            border-radius: 8px !important;
            padding: 1.25rem !important;
        }

        /* Compact cards (no forced min-height) */
        .paper-card {
            background-color: #151e2e !important;
            border: 1px solid #26354a !important;
            border-radius: 8px !important;
            padding: 1rem 1.25rem !important;
            margin-bottom: 0.75rem !important;
            color: #f8fafc !important;
        }

        .book-card-title {
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            line-height: 1.3 !important;
            margin: 0 !important;
            word-break: break-word !important;
            color: #f8fafc !important;
        }

        .section-heading {
            font-size: 1.15rem;
            font-weight: 600;
            margin: 1rem 0 0.5rem 0;
            color: #f8fafc;
        }

        .empty-state {
            padding: 2rem;
            text-align: center;
            color: #94a3b8;
            border: 1px dashed #26354a;
            border-radius: 8px;
            margin: 1rem 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def page_header(tag, title, subtitle):
    st.markdown(
        f"""
        <div style='margin-bottom: 1.5rem;'>
            <div style='font-size: 0.72rem; letter-spacing: 0.12em; text-transform: uppercase; color: #3b82f6; font-weight: 700;'>{tag}</div>
            <h2 style='margin-top: 0.2rem; margin-bottom: 0.3rem; color: #f8fafc;'>{title}</h2>
            <div style='font-size: 0.9rem; color: #94a3b8;'>{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def stat_card(label, value, caption=""):
    st.markdown(
        f"""
        <div class='paper-card' style='text-align: center;'>
            <div style='font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; color: #94a3b8;'>{label}</div>
            <div style='font-size: 1.85rem; font-weight: 700; margin: 0.2rem 0; color: #f8fafc;'>{value}</div>
            <div style='font-size: 0.72rem; color: #64748b;'>{caption}</div>
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
            <div style='display: flex; justify-content: space-between; align-items: flex-start; gap: 0.5rem;'>
                <div>
                    <div class='book-card-title'>{title}</div>
                    <div style='font-size: 0.85rem; color: #94a3b8; margin-top: 0.25rem;'>By {authors} · {year}</div>
                </div>
                <span style='background: rgba(59, 130, 246, 0.15); color: #60a5fa; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 600; white-space: nowrap;'>
                    {category}
                </span>
            </div>
            <div style='display: flex; justify-content: space-between; margin-top: 0.85rem; padding-top: 0.65rem; border-top: 1px solid #26354a; font-size: 0.8rem; color: #94a3b8;'>
                <span>ISBN: <strong style='color: #cbd5e1;'>{isbn}</strong></span>
                <span>Publisher: <strong style='color: #cbd5e1;'>{publisher}</strong></span>
                <span>Copies: <strong style='color: #60a5fa;'>{available} / {total} available</strong></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
