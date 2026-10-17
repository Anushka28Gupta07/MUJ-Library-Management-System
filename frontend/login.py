import streamlit as st
import base64
import os

def get_image_base64():
    frontend_dir = os.path.dirname(__file__)
    possible_names = [
        "background.jpg",
        "background.jpeg",
        "background.png",
        "background.JPG",
        "background.PNG"
    ]
    for name in possible_names:
        full_path = os.path.join(frontend_dir, name)
        if os.path.exists(full_path):
            with open(full_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
                ext = name.split(".")[-1].lower()
                mime = "jpeg" if ext in ["jpg", "jpeg"] else "png"
                return f"data:image/{mime};base64,{encoded}"
    return None

def render_login():
    bg_data = get_image_base64()

    if bg_data:
        bg_style = f"""
        [data-testid="stAppViewContainer"] {{
            background-image: radial-gradient(circle at center, rgba(15, 23, 42, 0.65) 0%, rgba(10, 15, 29, 0.85) 100%), url("{bg_data}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }}
        [data-testid="stHeader"] {{
            background: rgba(0,0,0,0) !important;
        }}
        """
    else:
        bg_style = """
        [data-testid="stAppViewContainer"] {
            background-color: #0b1120 !important;
        }
        """

    st.markdown(
        f"""
        <style>
        {bg_style}

        div[data-testid="stForm"] {{
            background: rgba(15, 23, 42, 0.78) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(255, 255, 255, 0.18) !important;
            border-radius: 14px !important;
            padding: 2.2rem 1.8rem !important;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.6) !important;
        }}

        h1 {{
            color: #ffffff !important;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.9);
            font-weight: 800 !important;
        }}

        h2, h3, p, label {{
            color: #f8fafc !important;
        }}

        input {{
            border-radius: 6px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h1 style='text-align: center; margin-top: 1.5rem; margin-bottom: 1.5rem;'>📚 Library Management System</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.8, 1])

    with col2:
        tab_signin, tab_signup = st.tabs(["🔑 Sign In", "📝 Create Account"])

        with tab_signin:
            with st.form("login_form"):
                username = st.text_input("Username or Email", placeholder="e.g., admin or user@example.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                submit = st.form_submit_button("Sign In to Portal", use_container_width=True)

                if submit:
                    if username == "admin" and password == "admin123":
                        st.session_state["authenticated"] = True
                        st.session_state["username"] = username
                        st.session_state["current_page"] = "Dashboard"
                        st.success("Authentication successful.")
                        st.rerun()
                    elif "@" in username and password:
                        st.session_state["authenticated"] = True
                        st.session_state["username"] = username.split("@")[0].capitalize()
                        st.session_state["current_page"] = "Dashboard"
                        st.success("Welcome back! Redirecting...")
                        st.rerun()
                    elif username.strip() == "" or password.strip() == "":
                        st.error("Please fill in all fields.")
                    else:
                        st.error("Invalid credentials. Try 'admin' and 'admin123'")

        with tab_signup:
            with st.form("signup_form"):
                new_name = st.text_input("Full Name *", placeholder="e.g., Ayushi Verma")
                new_email = st.text_input("College Email *", placeholder="e.g., student@example.com")
                new_phone = st.text_input("Phone Number", placeholder="e.g., 9876543210")
                new_pass = st.text_input("Create Password *", type="password", placeholder="••••••••")
                confirm_pass = st.text_input("Confirm Password *", type="password", placeholder="••••••••")

                register = st.form_submit_button("Register Account", use_container_width=True)

                if register:
                    if not new_name or not new_email or not new_pass:
                        st.error("Please fill in all required fields marked with *.")
                    elif new_pass != confirm_pass:
                        st.error("Passwords do not match.")
                    else:
                        st.success(f"Account created successfully for {new_name}! You can now sign in.")