import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os
from datetime import datetime
import hashlib

# Get base directory of the app
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="SegmentPro — Customer Intelligence Platform",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Persistent storage file for authentication
AUTH_FILE = ".streamlit/auth_session.json"

# Create .streamlit directory if it doesn't exist
os.makedirs(".streamlit", exist_ok=True)

# Function to save authentication session
def save_auth_session():
    """Save authentication state to file"""
    auth_data = {
        "authenticated": st.session_state.authenticated,
        "username": st.session_state.username
    }
    with open(AUTH_FILE, "w") as f:
        json.dump(auth_data, f)

# Function to load authentication session
def load_auth_session():
    """Load authentication state from file"""
    if os.path.exists(AUTH_FILE):
        try:
            with open(AUTH_FILE, "r") as f:
                auth_data = json.load(f)
                return auth_data.get("authenticated", False), auth_data.get("username", None)
        except:
            return False, None
    return False, None

# Function to clear authentication session
def clear_auth_session():
    """Clear authentication session file"""
    if os.path.exists(AUTH_FILE):
        os.remove(AUTH_FILE)

# Initialize session state
if 'authenticated' not in st.session_state:
    auth_state, username = load_auth_session()
    st.session_state.authenticated = auth_state
    st.session_state.username = username
if 'username' not in st.session_state:
    st.session_state.username = None
if 'users' not in st.session_state:
    st.session_state.users = {}
if 'show_signin' not in st.session_state:
    st.session_state.show_signin = False
if 'show_signup' not in st.session_state:
    st.session_state.show_signup = False

# Simple password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Authentication functions
def register_user(username, email, password):
    if username in st.session_state.users:
        return False, "Username already exists"
    st.session_state.users[username] = {
        "email": email,
        "password": hash_password(password)
    }
    return True, "Account created successfully!"

def login_user(username, password):
    if username not in st.session_state.users:
        return False, "Username not found"
    if st.session_state.users[username]["password"] != hash_password(password):
        return False, "Incorrect password"
    return True, "Login successful!"

# ──────────────────────────────────────────────
# PREMIUM DARK GLASSMORPHISM CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ── Root Variables ── */
    :root {
        --bg-primary: #0a0a1a;
        --bg-secondary: #111128;
        --bg-card: rgba(255, 255, 255, 0.04);
        --bg-card-hover: rgba(255, 255, 255, 0.07);
        --glass: rgba(255, 255, 255, 0.06);
        --glass-border: rgba(255, 255, 255, 0.1);
        --accent-1: #6366f1;
        --accent-2: #8b5cf6;
        --accent-3: #a78bfa;
        --accent-cyan: #22d3ee;
        --accent-pink: #f472b6;
        --accent-emerald: #34d399;
        --accent-amber: #fbbf24;
        --text-primary: #f1f5f9;
        --text-secondary: rgba(255, 255, 255, 0.6);
        --text-muted: rgba(255, 255, 255, 0.35);
        --gradient-main: linear-gradient(135deg, #6366f1 0%, #8b5cf6 40%, #a78bfa 100%);
        --gradient-hero: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        --gradient-cyan: linear-gradient(135deg, #06b6d4 0%, #8b5cf6 100%);
        --gradient-pink: linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%);
        --gradient-emerald: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
        --shadow-glow: 0 0 40px rgba(99, 102, 241, 0.15);
        --radius: 16px;
        --radius-sm: 10px;
        --radius-lg: 24px;
    }

    /* ── Global Reset ── */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .stApp {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }

    /* Hide Streamlit defaults */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    div[data-testid="stDecoration"] {display: none;}

    /* ── Scrollbar ── */
    ::-webkit-scrollbar {width: 6px;}
    ::-webkit-scrollbar-track {background: var(--bg-primary);}
    ::-webkit-scrollbar-thumb {background: var(--accent-1); border-radius: 3px;}
    ::-webkit-scrollbar-thumb:hover {background: var(--accent-2);}

    /* ── Keyframe Animations ── */
    @keyframes fadeInUp {
        from {opacity: 0; transform: translateY(40px);}
        to {opacity: 1; transform: translateY(0);}
    }
    @keyframes fadeInDown {
        from {opacity: 0; transform: translateY(-30px);}
        to {opacity: 1; transform: translateY(0);}
    }
    @keyframes slideInLeft {
        from {opacity: 0; transform: translateX(-40px);}
        to {opacity: 1; transform: translateX(0);}
    }
    @keyframes pulse-glow {
        0%, 100% {box-shadow: 0 0 20px rgba(99, 102, 241, 0.2);}
        50% {box-shadow: 0 0 40px rgba(99, 102, 241, 0.4);}
    }
    @keyframes gradient-shift {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    @keyframes float-slow {
        0%, 100% {transform: translateY(0px) rotate(0deg);}
        33% {transform: translateY(-15px) rotate(1deg);}
        66% {transform: translateY(8px) rotate(-1deg);}
    }
    @keyframes shimmer {
        0% {background-position: -200% 0;}
        100% {background-position: 200% 0;}
    }
    @keyframes orbit {
        from {transform: rotate(0deg) translateX(160px) rotate(0deg);}
        to {transform: rotate(360deg) translateX(160px) rotate(-360deg);}
    }
    @keyframes orbit-reverse {
        from {transform: rotate(0deg) translateX(120px) rotate(0deg);}
        to {transform: rotate(-360deg) translateX(120px) rotate(360deg);}
    }
    @keyframes text-glow {
        0%, 100% {text-shadow: 0 0 30px rgba(99,102,241,0.3);}
        50% {text-shadow: 0 0 60px rgba(139,92,246,0.5);}
    }

    /* ── Glass Card Base ── */
    .glass-card {
        background: var(--glass);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius);
        padding: 28px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    }
    .glass-card:hover {
        background: var(--bg-card-hover);
        border-color: rgba(99, 102, 241, 0.3);
        box-shadow: var(--shadow-glow);
        transform: translateY(-2px);
    }

    /* ── Landing Page ── */
    .landing-hero {
        min-height: 85vh;
        background: var(--gradient-hero);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 60px 20px;
        position: relative;
        overflow: hidden;
        border-radius: 0 0 var(--radius-lg) var(--radius-lg);
        margin: -100px -100px 30px -100px;
    }
    /* Animated orbs */
    .landing-hero::before {
        content: '';
        position: absolute;
        width: 500px; height: 500px;
        background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
        border-radius: 50%;
        top: -100px; right: -100px;
        animation: float-slow 8s ease-in-out infinite;
    }
    .landing-hero::after {
        content: '';
        position: absolute;
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(236,72,153,0.1) 0%, transparent 70%);
        border-radius: 50%;
        bottom: -80px; left: -80px;
        animation: float-slow 10s ease-in-out infinite reverse;
    }
    .hero-badge {
        display: inline-block;
        padding: 8px 20px;
        background: rgba(99,102,241,0.15);
        border: 1px solid rgba(99,102,241,0.3);
        border-radius: 50px;
        color: var(--accent-3);
        font-size: 0.85em;
        font-weight: 500;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 24px;
        animation: fadeInDown 0.6s ease-out;
    }
    .hero-icon-ring {
        width: 100px; height: 100px;
        border-radius: 50%;
        background: rgba(99,102,241,0.1);
        border: 2px solid rgba(99,102,241,0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.8em;
        margin: 0 auto 28px;
        animation: pulse-glow 3s ease-in-out infinite, fadeInUp 0.7s ease-out;
    }
    .hero-title {
        font-size: 4em;
        font-weight: 800;
        color: white;
        letter-spacing: -2px;
        margin-bottom: 12px;
        line-height: 1.1;
        animation: fadeInUp 0.8s ease-out, text-glow 4s ease-in-out infinite;
    }
    .hero-subtitle {
        font-size: 1.3em;
        color: var(--text-secondary);
        font-weight: 300;
        margin-bottom: 16px;
        animation: fadeInUp 0.9s ease-out;
    }
    .hero-desc {
        font-size: 1em;
        color: var(--text-muted);
        max-width: 520px;
        margin: 0 auto 40px;
        line-height: 1.7;
        animation: fadeInUp 1s ease-out;
    }
    /* Floating orbital dots */
    .orb-container {
        position: absolute;
        width: 100%; height: 100%;
        top: 0; left: 0;
        pointer-events: none;
        z-index: 0;
    }
    .orb {
        position: absolute;
        width: 8px; height: 8px;
        border-radius: 50%;
        top: 50%; left: 50%;
    }
    .orb-1 {
        background: var(--accent-cyan);
        animation: orbit 12s linear infinite;
        box-shadow: 0 0 12px var(--accent-cyan);
    }
    .orb-2 {
        background: var(--accent-pink);
        animation: orbit-reverse 15s linear infinite;
        box-shadow: 0 0 12px var(--accent-pink);
    }
    .orb-3 {
        background: var(--accent-emerald);
        animation: orbit 20s linear infinite reverse;
        box-shadow: 0 0 12px var(--accent-emerald);
        width: 6px; height: 6px;
    }
    /* Feature pills on landing */
    .feature-pills {
        display: flex;
        gap: 12px;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 30px;
        z-index: 2;
        position: relative;
        animation: fadeInUp 1.1s ease-out;
    }
    .feature-pill {
        padding: 10px 20px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 50px;
        color: var(--text-secondary);
        font-size: 0.85em;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .feature-pill:hover {
        background: rgba(99,102,241,0.15);
        border-color: rgba(99,102,241,0.3);
        color: var(--accent-3);
    }

    /* ── Auth Forms ── */
    .auth-wrapper {
        max-width: 440px;
        margin: 40px auto;
        animation: fadeInUp 0.6s ease-out;
    }
    .auth-card {
        background: rgba(17, 17, 40, 0.9);
        backdrop-filter: blur(24px);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-lg);
        padding: 48px 40px;
        position: relative;
        overflow: hidden;
    }
    .auth-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: var(--gradient-main);
    }
    .auth-header {
        text-align: center;
        margin-bottom: 32px;
    }
    .auth-header h2 {
        font-size: 1.8em;
        font-weight: 700;
        background: var(--gradient-main);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    .auth-header p {
        color: var(--text-muted);
        font-size: 0.9em;
    }

    /* ── Dashboard Header ── */
    .dash-header {
        background: linear-gradient(135deg, rgba(99,102,241,0.12) 0%, rgba(139,92,246,0.08) 100%);
        border: 1px solid rgba(99,102,241,0.15);
        border-radius: var(--radius-lg);
        padding: 32px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 28px;
        animation: fadeInDown 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    .dash-header::after {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: var(--gradient-main);
    }
    .dash-brand {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .dash-brand-icon {
        width: 48px; height: 48px;
        border-radius: 14px;
        background: var(--gradient-main);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4em;
        box-shadow: 0 4px 20px rgba(99,102,241,0.3);
    }
    .dash-brand-text {
        font-size: 1.6em;
        font-weight: 700;
        background: var(--gradient-main);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    .dash-user {
        display: flex;
        align-items: center;
        gap: 12px;
        color: var(--text-secondary);
        font-weight: 500;
    }
    .user-avatar {
        width: 38px; height: 38px;
        border-radius: 12px;
        background: linear-gradient(135deg, var(--accent-cyan), var(--accent-2));
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.9em;
        font-weight: 700;
        color: white;
    }

    /* ── Section Header ── */
    .section-header {
        text-align: center;
        margin-bottom: 36px;
        animation: fadeInUp 0.5s ease-out;
    }
    .section-header h1 {
        font-size: 2.2em;
        font-weight: 800;
        background: var(--gradient-main);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
        margin-bottom: 8px;
    }
    .section-header p {
        color: var(--text-muted);
        font-size: 1em;
    }

    /* ── Stat Cards ── */
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin: 20px 0;
    }
    .stat-card {
        background: var(--glass);
        backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius);
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
    }
    .stat-card.cyan::before { background: var(--gradient-cyan); }
    .stat-card.pink::before { background: var(--gradient-pink); }
    .stat-card.emerald::before { background: var(--gradient-emerald); }
    .stat-card.purple::before { background: var(--gradient-main); }
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-glow);
        border-color: rgba(99,102,241,0.3);
    }
    .stat-card .stat-icon {
        font-size: 1.6em;
        margin-bottom: 10px;
    }
    .stat-card .stat-value {
        font-size: 1.8em;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 4px;
    }
    .stat-card .stat-label {
        font-size: 0.8em;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 500;
    }

    /* ── Segment Result Card ── */
    .segment-result {
        background: linear-gradient(135deg, rgba(99,102,241,0.1) 0%, rgba(139,92,246,0.05) 100%);
        border: 1px solid rgba(99,102,241,0.2);
        border-radius: var(--radius-lg);
        padding: 36px;
        text-align: center;
        animation: fadeInUp 0.5s ease-out;
        position: relative;
        overflow: hidden;
    }
    .segment-result::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: var(--gradient-main);
    }
    .segment-result .segment-emoji {
        font-size: 3em;
        margin-bottom: 12px;
        animation: float-slow 4s ease-in-out infinite;
    }
    .segment-result .segment-name {
        font-size: 1.8em;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 6px;
    }
    .segment-result .segment-type {
        color: var(--accent-3);
        font-size: 1em;
        font-weight: 500;
        margin-bottom: 16px;
    }

    /* ── Info / Feature Boxes ── */
    .info-glass {
        background: var(--glass);
        backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius);
        padding: 22px 26px;
        transition: all 0.3s ease;
        position: relative;
    }
    .info-glass:hover {
        border-color: rgba(99,102,241,0.3);
        background: var(--bg-card-hover);
    }
    .info-glass .info-label {
        font-size: 0.75em;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: var(--text-muted);
        margin-bottom: 8px;
        font-weight: 600;
    }
    .info-glass .info-value {
        font-size: 1.6em;
        font-weight: 700;
        color: var(--text-primary);
    }

    /* ── Strategy Card ── */
    .strategy-card {
        background: linear-gradient(135deg, rgba(34,211,238,0.08) 0%, rgba(99,102,241,0.08) 100%);
        border: 1px solid rgba(34,211,238,0.2);
        border-radius: var(--radius);
        padding: 24px 28px;
        margin: 16px 0;
    }
    .strategy-card h4 {
        color: var(--accent-cyan);
        font-size: 0.85em;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 10px;
        font-weight: 600;
    }
    .strategy-card p {
        color: var(--text-primary);
        font-size: 1.05em;
        font-weight: 500;
    }

    /* ── Recommendation Items ── */
    .rec-item {
        background: var(--glass);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-sm);
        padding: 16px 20px;
        margin: 8px 0;
        display: flex;
        align-items: center;
        gap: 14px;
        transition: all 0.3s ease;
    }
    .rec-item:hover {
        background: var(--bg-card-hover);
        border-color: rgba(99,102,241,0.2);
        transform: translateX(4px);
    }
    .rec-item .rec-icon {
        width: 40px; height: 40px;
        border-radius: 10px;
        background: rgba(99,102,241,0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1em;
        flex-shrink: 0;
    }
    .rec-item .rec-text {
        color: var(--text-primary);
        font-size: 0.95em;
        font-weight: 400;
    }

    /* ── Prompt Card (empty state) ── */
    .prompt-card {
        background: var(--glass);
        border: 1px dashed rgba(99,102,241,0.3);
        border-radius: var(--radius);
        padding: 48px 36px;
        text-align: center;
    }
    .prompt-card .prompt-icon {
        font-size: 2.5em;
        margin-bottom: 16px;
        opacity: 0.6;
    }
    .prompt-card .prompt-text {
        color: var(--text-secondary);
        font-size: 1.05em;
    }

    /* ── About Section ── */
    .about-card {
        background: var(--glass);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius);
        padding: 32px;
    }
    .about-card h3 {
        color: var(--accent-3);
        font-size: 1.2em;
        margin-bottom: 16px;
    }
    .about-card li {
        color: var(--text-secondary);
        margin-bottom: 8px;
        line-height: 1.6;
    }

    /* ── Streamlit Widget Overrides ── */
    .stSlider > div > div {
        color: var(--text-primary) !important;
    }
    .stSlider label {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 1em !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: var(--glass);
        border-radius: var(--radius);
        padding: 6px;
        gap: 4px;
        border: 1px solid var(--glass-border);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-sm);
        color: var(--text-secondary);
        font-weight: 500;
        padding: 10px 18px;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(99,102,241,0.15) !important;
        color: var(--accent-3) !important;
        border-color: transparent !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 24px;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: var(--accent-1) !important;
    }

    .stButton > button {
        border-radius: var(--radius-sm) !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        border: 1px solid var(--glass-border) !important;
        background: var(--glass) !important;
        color: var(--text-primary) !important;
    }
    .stButton > button:hover {
        border-color: rgba(99,102,241,0.4) !important;
        background: rgba(99,102,241,0.12) !important;
        box-shadow: 0 0 20px rgba(99,102,241,0.15) !important;
        transform: translateY(-1px);
    }
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {
        background: var(--gradient-main) !important;
        border: none !important;
        color: white !important;
        box-shadow: 0 4px 20px rgba(99,102,241,0.3) !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="stBaseButton-primary"]:hover {
        box-shadow: 0 6px 30px rgba(99,102,241,0.4) !important;
        transform: translateY(-2px);
    }

    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-1) !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
    }
    .stTextInput label {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }

    div[data-testid="stExpander"] {
        background: var(--glass) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius) !important;
    }

    .stDataFrame {
        border-radius: var(--radius) !important;
    }

    /* ── Dividers ── */
    hr {
        border: 0 !important;
        height: 1px !important;
        background: linear-gradient(to right, transparent, var(--glass-border), transparent) !important;
        margin: 28px 0 !important;
    }

    /* ── Footer ── */
    .footer-bar {
        text-align: center;
        padding: 32px 20px;
        color: var(--text-muted);
        font-size: 0.85em;
        border-top: 1px solid var(--glass-border);
        margin-top: 40px;
    }
    .footer-bar span {
        background: var(--gradient-main);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
    }

    /* ── Misc ── */
    .stMarkdown a { color: var(--accent-3) !important; }
    .stAlert { border-radius: var(--radius-sm) !important; }
    div[data-testid="stMetric"] {
        background: var(--glass);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-sm);
        padding: 14px 18px;
    }
    div[data-testid="stMetric"] label {color: var(--text-muted) !important;}
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {color: var(--text-primary) !important;}

    /* Example segment cards */
    .example-segment {
        background: var(--glass);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius);
        padding: 24px;
        transition: all 0.3s ease;
    }
    .example-segment:hover {
        border-color: rgba(99,102,241,0.3);
        transform: translateY(-3px);
        box-shadow: var(--shadow-glow);
    }
    .example-segment h4 {
        color: var(--accent-3);
        margin-bottom: 12px;
    }
    .example-segment p {
        color: var(--text-secondary);
        font-size: 0.9em;
        line-height: 1.6;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# LANDING / AUTH PAGES
# ──────────────────────────────────────────────

def show_landing_page():
    """Display premium dark landing page"""
    st.markdown("""
    <div class="landing-hero">
        <div class="orb-container">
            <div class="orb orb-1"></div>
            <div class="orb orb-2"></div>
            <div class="orb orb-3"></div>
        </div>
        <div style="position:relative; z-index:2;">
            <div class="hero-badge">✦ Customer Intelligence</div>
            <div class="hero-icon-ring">🛍️</div>
            <h1 class="hero-title">SegmentPro</h1>
            <p class="hero-subtitle">Customer Intelligence Platform</p>
            <p class="hero-desc">
                Unlock powerful customer insights with AI-driven K-Means segmentation.
                Discover hidden patterns, optimize marketing strategies, and drive revenue growth.
            </p>
            <div class="feature-pills">
                <span class="feature-pill">🔮 Predictive Segments</span>
                <span class="feature-pill">📊 Visual Analytics</span>
                <span class="feature-pill">💡 Smart Recommendations</span>
                <span class="feature-pill">⚡ Real-time Analysis</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button("🔓 Sign In", key="nav_signin_landing", use_container_width=True):
            st.session_state.show_signin = True
            st.rerun()
    with col3:
        if st.button("📝 Sign Up", key="nav_signup_landing", use_container_width=True):
            st.session_state.show_signup = True
            st.rerun()


def show_signin_modal():
    """Display Sign In form with glassmorphism styling"""
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
        <div class="auth-card">
            <div class="auth-header">
                <h2>🔓 Welcome Back</h2>
                <p>Sign in to access your dashboard</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("👤 Username", placeholder="Enter your username", key="signin_user")
        password = st.text_input("🔐 Password", type="password", placeholder="Enter your password", key="signin_pass")

        if st.button("Sign In", use_container_width=True, key="signin_btn", type="primary"):
            if username and password:
                success, message = login_user(username, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.show_signin = False
                    save_auth_session()
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please enter both username and password")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📝 Don't have an account? Create one", use_container_width=True, key="switch_to_signup_from_signin"):
            st.session_state.show_signin = False
            st.session_state.show_signup = True
            st.rerun()


def show_signup_modal():
    """Display Sign Up form with glassmorphism styling"""
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
        <div class="auth-card">
            <div class="auth-header">
                <h2>📝 Create Account</h2>
                <p>Join SegmentPro today</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        new_username = st.text_input("👤 Username", placeholder="Choose a username", key="signup_user")
        new_email = st.text_input("📧 Email", placeholder="Enter your email", key="signup_email")
        new_password = st.text_input("🔐 Password", type="password", placeholder="Create a password", key="signup_pass")
        confirm_password = st.text_input("🔐 Confirm Password", type="password", placeholder="Confirm password", key="signup_pass_confirm")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Create Account", use_container_width=True, key="signup_btn", type="primary"):
                if not new_username or not new_email or not new_password:
                    st.error("Please fill in all fields")
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    success, message = register_user(new_username, new_email, new_password)
                    if success:
                        st.success(message)
                        st.session_state.show_signup = False
                        st.session_state.show_signin = True
                        st.rerun()
                    else:
                        st.error(message)
        with c2:
            if st.button("← Back to Sign In", use_container_width=True, key="switch_to_signin"):
                st.session_state.show_signup = False
                st.session_state.show_signin = True
                st.rerun()


# ──────────────────────────────────────────────
# MODEL & DATA LOADING
# ──────────────────────────────────────────────

@st.cache_resource
def load_model():
    try:
        model_path = os.path.join(BASE_DIR, 'models', 'kmeans_model.pkl')
        info_path = os.path.join(BASE_DIR, 'models', 'model_info.json')
        model = joblib.load(model_path)
        with open(info_path) as f:
            info = json.load(f)
        return model, info
    except Exception as e:
        st.error(f"Failed to load model: {str(e)}")
        return None, None

@st.cache_data
def load_dataset():
    try:
        dataset_path = os.path.join(BASE_DIR, 'dataset', 'Mall_Customers.csv')
        df = pd.read_csv(dataset_path)
        return df
    except Exception as e:
        st.error(f"Failed to load dataset: {str(e)}")
        return None


# ──────────────────────────────────────────────
# ROUTING: LANDING vs DASHBOARD
# ──────────────────────────────────────────────

if not st.session_state.authenticated:
    if not st.session_state.show_signin and not st.session_state.show_signup:
        show_landing_page()
    elif st.session_state.show_signin:
        show_signin_modal()
    elif st.session_state.show_signup:
        show_signup_modal()
    st.stop()


# ──────────────────────────────────────────────
# AUTHENTICATED DASHBOARD
# ──────────────────────────────────────────────

# Top header bar
user_initial = st.session_state.username[0].upper() if st.session_state.username else "U"
st.markdown(f"""
<div class="dash-header">
    <div class="dash-brand">
        <div class="dash-brand-icon">🛍️</div>
        <div class="dash-brand-text">SegmentPro</div>
    </div>
    <div class="dash-user">
        <span>Welcome, {st.session_state.username}</span>
        <div class="user-avatar">{user_initial}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Logout column
logout_col1, logout_col2 = st.columns([5, 1])
with logout_col2:
    if st.button("🚪 Logout", key="navbar_logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username = None
        clear_auth_session()
        st.rerun()

# Load model
try:
    kmeans, model_info = load_model()
    model_loaded = kmeans is not None
    if not model_loaded:
        st.error("Error: Failed to load KMeans model. Check 'models/kmeans_model.pkl'.")
except Exception as e:
    kmeans = None
    model_loaded = False
    st.error(f"Error: {e}")

# Load dataset
dataset = load_dataset()

# Section header
st.markdown("""
<div class="section-header">
    <h1>🛍️ Customer Segmentation Dashboard</h1>
    <p>AI-powered K-Means clustering analysis for intelligent customer insights</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Input Controls ──
slider_col1, slider_col2 = st.columns(2)
with slider_col1:
    income = st.slider(
        "💰 Annual Income (k₹)",
        min_value=10, max_value=150, value=60, step=5,
        help="Select annual income in thousands"
    )
with slider_col2:
    spending = st.slider(
        "🛍️ Spending Score (1-100)",
        min_value=1, max_value=100, value=50,
        help="Shopping activity and frequency score"
    )

st.markdown("---")

# ── Profile Metrics ──
income_level = "High" if income >= 100 else "Medium" if income >= 50 else "Low"
spending_level = "High" if spending >= 60 else "Medium" if spending >= 40 else "Low"

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="info-glass">
        <div class="info-label">Annual Income</div>
        <div class="info-value" style="color: var(--accent-cyan);">₹{income}k</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="info-glass">
        <div class="info-label">Spending Score</div>
        <div class="info-value" style="color: var(--accent-pink);">{spending}/100</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="info-glass">
        <div class="info-label">Profile Type</div>
        <div class="info-value" style="color: var(--accent-emerald);">{income_level} / {spending_level}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Predict Button ──
btn_c1, btn_c2, btn_c3 = st.columns([1, 2, 1])
with btn_c2:
    predict_btn = st.button(
        "🔮  Analyze & Find My Segment",
        use_container_width=True,
        key="find_segment_main",
        type="primary"
    )

st.markdown("---")

# ── Segment Definitions (shared) ──
segments = {
    0: {
        "name": "Premium Customer", "emoji": "💎",
        "desc": "High income, high spender",
        "strategy": "Send VIP offers, luxury brand promotions, and exclusive early-access invites.",
        "color": "#fbbf24",
        "details": "Your most valuable customers — high purchasing power and strong engagement.",
        "gradient": "linear-gradient(135deg, rgba(251,191,36,0.1), rgba(245,158,11,0.05))",
        "border": "rgba(251,191,36,0.3)"
    },
    1: {
        "name": "Careful Spender", "emoji": "💰",
        "desc": "High income, low spender",
        "strategy": "Send value-for-money deals, quality comparisons, and smart savings alerts.",
        "color": "#34d399",
        "details": "Price-conscious high earners who value quality and meaningful discounts.",
        "gradient": "linear-gradient(135deg, rgba(52,211,153,0.1), rgba(16,185,129,0.05))",
        "border": "rgba(52,211,153,0.3)"
    },
    2: {
        "name": "Impulsive Buyer", "emoji": "🛍️",
        "desc": "Low income, high spender",
        "strategy": "Send flash sale alerts, limited-time offers, and trending product notifications.",
        "color": "#f472b6",
        "details": "Enthusiastic shoppers with limited income — highly responsive to promotions.",
        "gradient": "linear-gradient(135deg, rgba(244,114,182,0.1), rgba(236,72,153,0.05))",
        "border": "rgba(244,114,182,0.3)"
    },
    3: {
        "name": "Budget Customer", "emoji": "💚",
        "desc": "Low income, low spender",
        "strategy": "Send heavy discount coupons, clearance sale alerts, and budget bundle offers.",
        "color": "#22d3ee",
        "details": "Cost-conscious customers seeking the best value for every rupee.",
        "gradient": "linear-gradient(135deg, rgba(34,211,238,0.1), rgba(6,182,212,0.05))",
        "border": "rgba(34,211,238,0.3)"
    },
    4: {
        "name": "Average Customer", "emoji": "📊",
        "desc": "Medium income, medium spender",
        "strategy": "Send loyalty points, regular newsletters, and seasonal promotion offers.",
        "color": "#a78bfa",
        "details": "Balanced customers with moderate income and steady spending habits.",
        "gradient": "linear-gradient(135deg, rgba(167,139,250,0.1), rgba(139,92,246,0.05))",
        "border": "rgba(167,139,250,0.3)"
    }
}

# ── Tabs ──
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔮 Find Segment",
    "📈 Visualizations",
    "📊 Data Analysis",
    "💡 Recommendations",
    "ℹ️ About"
])

# ── TAB 1: Segment Finder ──
with tab1:
    st.markdown("### 🔮 Customer Segment Results")
    st.markdown("---")

    if predict_btn and model_loaded:
        input_data = np.array([[income, spending]])
        cluster = kmeans.predict(input_data)[0]
        seg = segments.get(cluster, {})

        st.markdown(f"""
        <div class="segment-result" style="background: {seg['gradient']}; border-color: {seg['border']};">
            <div class="segment-emoji">{seg['emoji']}</div>
            <div class="segment-name">{seg['name']}</div>
            <div class="segment-type">{seg['desc']}</div>
            <p style="color: var(--text-secondary); max-width: 500px; margin: 0 auto; font-size: 0.95em;">
                {seg['details']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Detail cards
        d1, d2, d3 = st.columns(3)
        with d1:
            st.markdown(f"""
            <div class="info-glass">
                <div class="info-label">Segment</div>
                <div class="info-value" style="font-size:1.2em; color:{seg['color']};">{seg['emoji']} {seg['name']}</div>
            </div>""", unsafe_allow_html=True)
        with d2:
            st.markdown(f"""
            <div class="info-glass">
                <div class="info-label">Behavior Type</div>
                <div class="info-value" style="font-size:1.2em;">{seg['desc']}</div>
            </div>""", unsafe_allow_html=True)
        with d3:
            st.markdown(f"""
            <div class="info-glass">
                <div class="info-label">Cluster ID</div>
                <div class="info-value" style="font-size:1.2em;">Group {cluster}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")

        # Strategy
        st.markdown(f"""
        <div class="strategy-card">
            <h4>📢 Recommended Marketing Strategy</h4>
            <p>{seg['strategy']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Expandable analytics
        with st.expander("🔍 Detailed Segment Analytics"):
            ac1, ac2 = st.columns(2)
            with ac1:
                st.metric("Cluster Number", cluster)
            with ac2:
                st.metric("Estimated Segment Size", "~40 customers")
            st.markdown(f"""
            **Customer Characteristics:**
            - Income Level: {'High' if income >= 100 else 'Medium' if income >= 50 else 'Low'}
            - Spending Behavior: {'Frequent' if spending >= 60 else 'Moderate' if spending >= 40 else 'Minimal'}
            - Purchase Power Index: {income * (spending / 100):.0f}k
            """)

    elif not predict_btn:
        st.markdown("""
        <div class="prompt-card">
            <div class="prompt-icon">🔮</div>
            <div class="prompt-text">Adjust the sliders above and click <strong>"Analyze & Find My Segment"</strong> to discover your customer profile.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📌 Example Segments")
        ex1, ex2 = st.columns(2)
        with ex1:
            st.markdown("""
            <div class="example-segment">
                <h4>💎 Premium Customer</h4>
                <p>Income: ₹120k+ &nbsp;·&nbsp; Score: 80+<br>Best for luxury product promotions</p>
            </div>""", unsafe_allow_html=True)
        with ex2:
            st.markdown("""
            <div class="example-segment">
                <h4>💰 Careful Spender</h4>
                <p>Income: ₹100k+ &nbsp;·&nbsp; Score: &lt;40<br>Best for value-focused deals</p>
            </div>""", unsafe_allow_html=True)


# ── TAB 2: Visualizations ──
with tab2:
    st.markdown("### 📈 Visualizations & Insights")

    images_path = os.path.join(BASE_DIR, 'images')
    clusters_img = os.path.join(images_path, 'clusters.png')

    if os.path.exists(clusters_img):
        st.markdown("#### 🎯 Customer Clusters")
        st.image(clusters_img, caption='2D Plot — Customer Segments (Income vs Spending Score)', use_container_width=True)

        st.markdown("---")

        # Metrics row
        st.markdown("""
        <div class="stat-grid">
            <div class="stat-card cyan">
                <div class="stat-icon">👥</div>
                <div class="stat-value">200</div>
                <div class="stat-label">Total Customers</div>
            </div>
            <div class="stat-card pink">
                <div class="stat-icon">🎯</div>
                <div class="stat-value">5</div>
                <div class="stat-label">Clusters</div>
            </div>
            <div class="stat-card emerald">
                <div class="stat-icon">📐</div>
                <div class="stat-value">2</div>
                <div class="stat-label">Features</div>
            </div>
            <div class="stat-card purple">
                <div class="stat-icon">⚙️</div>
                <div class="stat-value">K=5</div>
                <div class="stat-label">Optimal K</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 📈 Detailed Analysis")

        viz1, viz2 = st.columns(2)
        with viz1:
            st.markdown("##### 📉 Elbow Method")
            elbow_img = os.path.join(images_path, 'elbow_curve.png')
            if os.path.exists(elbow_img):
                st.image(elbow_img, caption='Elbow Curve — Optimal K=5', use_container_width=True)
        with viz2:
            st.markdown("##### 📊 Feature Distributions")
            dist_img = os.path.join(images_path, 'distributions.png')
            if os.path.exists(dist_img):
                st.image(dist_img, caption='Income & Spending Score Distributions', use_container_width=True)
    else:
        st.warning("⚠️ Visualization images not found in the images/ folder.")


# ── TAB 3: Data Analysis ──
with tab3:
    st.markdown("### 📊 Data Analysis")

    if dataset is not None:
        # Overview metrics
        st.markdown(f"""
        <div class="stat-grid">
            <div class="stat-card cyan">
                <div class="stat-icon">📋</div>
                <div class="stat-value">{len(dataset)}</div>
                <div class="stat-label">Total Records</div>
            </div>
            <div class="stat-card pink">
                <div class="stat-icon">📊</div>
                <div class="stat-value">{len(dataset.columns)}</div>
                <div class="stat-label">Columns</div>
            </div>
            <div class="stat-card emerald">
                <div class="stat-icon">💰</div>
                <div class="stat-value">₹{dataset['Annual Income (k$)'].mean():.0f}k</div>
                <div class="stat-label">Avg Income</div>
            </div>
            <div class="stat-card purple">
                <div class="stat-icon">🛍️</div>
                <div class="stat-value">{dataset['Spending Score (1-100)'].mean():.0f}</div>
                <div class="stat-label">Avg Spending</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        with st.expander("📋 View Dataset Sample", expanded=False):
            st.dataframe(dataset.head(10), use_container_width=True)

        st.markdown("### 📈 Statistical Summary")
        s1, s2 = st.columns(2)
        with s1:
            st.markdown("**Income Statistics (k₹)**")
            st.write(dataset['Annual Income (k$)'].describe())
        with s2:
            st.markdown("**Spending Score Statistics**")
            st.write(dataset['Spending Score (1-100)'].describe())

        st.markdown("---")
        st.markdown("### 🔍 Segment Distribution")
        if 'Cluster' in dataset.columns:
            cluster_counts = dataset['Cluster'].value_counts().sort_index()
            st.bar_chart(cluster_counts)
    else:
        st.warning("Dataset not available!")


# ── TAB 4: Recommendations ──
with tab4:
    st.markdown("### 💡 Personalized Recommendations")

    if predict_btn and model_loaded:
        input_data = np.array([[income, spending]])
        cluster = kmeans.predict(input_data)[0]

        recommendations = {
            0: {
                "title": "💎 Premium Customer Playbook",
                "tips": [
                    ("🎁", "Exclusive Early Access to new premium collections"),
                    ("✨", "VIP Membership with priority customer service"),
                    ("💳", "Premium loyalty points on every purchase"),
                    ("🛍️", "Invitations to exclusive appreciation events"),
                    ("📦", "Complimentary shipping on all orders"),
                ],
                "target": "High-value customer retention"
            },
            1: {
                "title": "💰 Careful Spender Playbook",
                "tips": [
                    ("💰", "Smart Deals — best price alerts & comparisons"),
                    ("📊", "Detailed quality vs. price analysis reports"),
                    ("🏷️", "Bulk discount offers for larger purchases"),
                    ("📧", "Curated newsletter of best-value items"),
                    ("🎯", "Early notification of seasonal sales events"),
                ],
                "target": "Increase purchase frequency"
            },
            2: {
                "title": "🛍️ Impulsive Buyer Playbook",
                "tips": [
                    ("⚡", "Daily flash sales and limited-time deals"),
                    ("🎪", "Exclusive limited-edition drops"),
                    ("🔔", "Instant push alerts for trending products"),
                    ("🎁", "Attractive bundle deals and combos"),
                    ("⭐", "Curated 'Hot This Week' collections"),
                ],
                "target": "Maximize purchase frequency"
            },
            3: {
                "title": "💚 Budget Customer Playbook",
                "tips": [
                    ("🏷️", "Consistent budget-friendly daily deals"),
                    ("📱", "Exclusive discount codes and vouchers"),
                    ("💵", "Best bang-for-buck product bundles"),
                    ("🎯", "Student / Senior special discounts"),
                    ("💳", "Flexible payment plans and EMI options"),
                ],
                "target": "Build loyalty and repeat purchases"
            },
            4: {
                "title": "📊 Average Customer Playbook",
                "tips": [
                    ("🎟️", "Earn and redeem loyalty points easily"),
                    ("🎁", "Targeted seasonal promotions"),
                    ("📧", "Personalized product recommendations"),
                    ("🤝", "Referral rewards for bringing friends"),
                    ("⭐", "Growing member benefits with engagement"),
                ],
                "target": "Gradual value increase"
            }
        }

        rec = recommendations.get(cluster, {})
        st.markdown(f"#### {rec.get('title')}")
        st.markdown(f"""
        <div class="strategy-card">
            <h4>🎯 Goal</h4>
            <p>{rec.get('target')}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("##### 📌 Action Items")
        for icon, text in rec.get('tips', []):
            st.markdown(f"""
            <div class="rec-item">
                <div class="rec-icon">{icon}</div>
                <div class="rec-text">{text}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="prompt-card">
            <div class="prompt-icon">💡</div>
            <div class="prompt-text">Click <strong>"Analyze & Find My Segment"</strong> first to unlock personalized recommendations.</div>
        </div>
        """, unsafe_allow_html=True)


# ── TAB 5: About ──
with tab5:
    st.markdown("### ℹ️ About This Application")

    ab1, ab2 = st.columns([2, 1])

    with ab1:
        st.markdown("""
        <div class="about-card">
            <h3>🛍️ Customer Segmentation Analysis</h3>
            <p style="color: var(--text-secondary); line-height: 1.7;">
                This application uses <strong>K-Means Clustering</strong> to segment customers into
                distinct groups based on their purchasing behavior and income levels, enabling
                targeted marketing strategies for each segment.
            </p>
            <br>
            <h3>🚀 Key Features</h3>
            <ul>
                <li><strong>🔮 Segment Finder</strong> — Real-time customer classification</li>
                <li><strong>📈 Visual Analytics</strong> — Interactive cluster visualizations</li>
                <li><strong>📊 Data Exploration</strong> — Comprehensive dataset statistics</li>
                <li><strong>💡 Smart Recommendations</strong> — Tailored marketing strategies</li>
                <li><strong>🎯 Actionable Insights</strong> — Data-driven business decisions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="about-card">
            <h3>👥 The 5 Customer Segments</h3>
            <ul>
                <li><strong>💎 Premium</strong> — High income, high spenders</li>
                <li><strong>💰 Careful</strong> — High income, low spenders</li>
                <li><strong>🛍️ Impulsive</strong> — Low income, high spenders</li>
                <li><strong>💚 Budget</strong> — Low income, low spenders</li>
                <li><strong>📊 Average</strong> — Medium income & spending</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with ab2:
        st.markdown(f"""
        <div class="about-card" style="text-align: center;">
            <h3>📋 Project Info</h3>
            <p style="color: var(--text-secondary); margin-bottom: 8px;">
                <strong>Company:</strong> SkillCraft Technology</p>
            <p style="color: var(--text-secondary); margin-bottom: 8px;">
                <strong>Program:</strong> ML Internship</p>
            <p style="color: var(--text-secondary); margin-bottom: 8px;">
                <strong>Task:</strong> #02 — K-Means Clustering</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="about-card" style="text-align: center;">
            <h3>📊 Statistics</h3>
            <div class="stat-grid" style="grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 16px;">
                <div class="stat-card cyan" style="padding: 16px;">
                    <div class="stat-value" style="font-size:1.4em;">200</div>
                    <div class="stat-label" style="font-size:0.7em;">Customers</div>
                </div>
                <div class="stat-card pink" style="padding: 16px;">
                    <div class="stat-value" style="font-size:1.4em;">5</div>
                    <div class="stat-label" style="font-size:0.7em;">Clusters</div>
                </div>
                <div class="stat-card emerald" style="padding: 16px;">
                    <div class="stat-value" style="font-size:1.4em;">2</div>
                    <div class="stat-label" style="font-size:0.7em;">Features</div>
                </div>
                <div class="stat-card purple" style="padding: 16px;">
                    <div class="stat-value" style="font-size:1.4em;">K=5</div>
                    <div class="stat-label" style="font-size:0.7em;">Optimal</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    with st.expander("🔧 Technical Stack"):
        st.markdown("""
        - **Language:** Python 3.x
        - **ML Library:** Scikit-learn (K-Means)
        - **Data Processing:** Pandas, NumPy
        - **Web Framework:** Streamlit
        - **Visualization:** Matplotlib, Seaborn
        - **Model Serialization:** Joblib
        """)

    with st.expander("📚 Learn More"):
        st.markdown("""
        - **K-Means Clustering:** Unsupervised learning algorithm for grouping similar data points
        - **Elbow Method:** Technique to find optimal cluster count by plotting inertia
        - **Customer Segmentation:** Market strategy to group customers for targeted marketing
        - **Personalization:** Tailor offerings based on each customer's predicted segment
        """)


# ── Footer ──
st.markdown("---")
st.markdown("""
<div class="footer-bar">
    Built with ❤️ using <span>Streamlit</span> · SkillCraft Technology Internship<br>
    <span style="font-size: 0.85em;">© 2026 SegmentPro — Customer Intelligence Platform v3.0</span>
</div>
""", unsafe_allow_html=True)