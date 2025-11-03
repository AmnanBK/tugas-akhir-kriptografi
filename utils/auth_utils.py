import streamlit as st


def check_login():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Silakan login terlebih dahulu!")
        st.switch_page("app.py")
        st.stop()


def logout():
    st.session_state.clear()
    st.session_state["page"] = "login"
    st.rerun()
