import streamlit as st
import httpx
from typing import Optional
import json

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Feature Voting System", layout="centered")

# Session state for auth
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None

# Helper for API calls

def api_post(endpoint, data=None, token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    headers["Content-Type"] = "application/json"
    try:
        resp = httpx.post(f"{API_URL}{endpoint}/", json=data, headers=headers, timeout=10)
        return resp
    except Exception as e:
        return None

def api_post_form(endpoint, data=None, token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    try:
        resp = httpx.post(f"{API_URL}{endpoint}", data=data, headers=headers, timeout=10)
        return resp
    except Exception as e:
        return None

def api_get(endpoint, token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        resp = httpx.get(f"{API_URL}{endpoint}/", headers=headers, timeout=10)
        return resp
    except Exception as e:
        return None

def get_error_detail(resp):
    if not resp:
        return "API error"
    try:
        return resp.json().get("detail", str(resp.text))
    except Exception:
        return resp.text or "Unknown error"

# Caching for features list
@st.cache_data(show_spinner=False)
def get_features(token: Optional[str]):
    resp = api_get("/features", token)
    print(resp)
    if resp and resp.status_code == 200:
        return resp.json()
    return []

def clear_features_cache():
    get_features.clear()
    get_features(st.session_state.token)

# Helper to get user's votes
@st.cache_data(show_spinner=False)
def get_user_votes(token: Optional[str]):
    resp = api_get("/votes/user", token)
    if resp and resp.status_code == 200:
        return set(v["feature_id"] for v in resp.json())
    return set()

def clear_votes_cache():
    get_user_votes.clear()

# UI
st.title("🚀 Feature Voting System")

# Login form
if not st.session_state.token:
    st.subheader("Login")
    show_register = st.session_state.get("show_register", False)
    if not show_register:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                resp = api_post_form("/token", data={"username": username, "password": password}, token=None)
                if resp and resp.status_code == 200:
                    st.session_state.token = resp.json()["access_token"]
                    st.session_state.username = username
                    st.success("Logged in!")
                    st.experimental_rerun()
                else:
                    st.error("Login failed: " + get_error_detail(resp))
        if st.button("Create new user"):
            st.session_state.show_register = True
            st.experimental_rerun()
        st.stop()
    else:
        st.subheader("Register New User")
        with st.form("register_form"):
            reg_username = st.text_input("Username", key="reg_username")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            submitted = st.form_submit_button("Register")
            if submitted:
                if not reg_username or not reg_email or not reg_password:
                    st.warning("Please fill in all fields.")
                else:
                    resp = api_post("/users/register/", {"username": reg_username, "email": reg_email, "password": reg_password})
                    if resp and resp.status_code == 200:
                        st.success("User created! Please log in.")
                        st.session_state.show_register = False
                        st.experimental_rerun()
                    else:
                        st.error("Registration failed: " + get_error_detail(resp))
        if st.button("Back to login"):
            st.session_state.show_register = False
            st.experimental_rerun()
        st.stop()

# Main app
st.write(f"Welcome, **{st.session_state.username}**!")

# Create feature
with st.expander("➕ Propose a new feature"):
    with st.form("create_feature_form"):
        title = st.text_input("Feature Title")
        description = st.text_area("Description")
        submitted = st.form_submit_button("Submit Feature")
        if submitted:
            if not title or not description:
                st.warning("Please fill in all fields.")
            else:
                resp = api_post("/features", {"title": title, "description": description}, st.session_state.token)
                if resp and resp.status_code == 200:
                    st.success("Feature created!")
                    clear_features_cache()
                    st.experimental_rerun()
                else:
                    st.error("Error: " + get_error_detail(resp))

# List features in a table with upvote button only if not voted
st.subheader("All Features")
features = get_features(st.session_state.token)
voted_features = get_user_votes(st.session_state.token) if st.session_state.token else set()

import pandas as pd

def render_features_table(features, voted_features):
    if not features:
        st.info("No features found.")
        return
    # Table header
    cols = st.columns([3, 5, 1, 2])
    cols[0].markdown("**Title**")
    cols[1].markdown("**Description**")
    cols[2].markdown("**Votes**")
    cols[3].markdown("**Actions**")
    # Table rows
    for feat in features:
        voted = feat["id"] in voted_features
        cols = st.columns([3, 5, 1, 2])
        cols[0].markdown(f"**{feat['title']}**")
        cols[1].markdown(feat['description'])
        cols[2].write(feat['votes'])
        if not voted:
            if cols[3].button("Upvote", key=f"upvote_{feat['id']}"):
                resp = api_post(f"/votes/upvote/{feat['id']}", token=st.session_state.token)
                if resp and resp.status_code == 200:
                    st.success("Upvoted!")
                    clear_features_cache()
                    clear_votes_cache()
                    st.experimental_rerun()
                else:
                    st.error("Error: " + get_error_detail(resp))
        else:
            cols[3].button("Upvote", key=f"upvote_{feat['id']}_disabled", disabled=True)
            cols[3].write(":white_check_mark: Voted")

render_features_table(features, voted_features) 