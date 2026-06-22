# app.py – Garud AI v4  |  Indigo Dark Dashboard
# Multi-module threat detection: Scam · Fake News · Toxic Speech · Financial Fraud · Misinformation
# Plus an ML-powered spam classifier (Naive Bayes, trained on real SMS data)

import streamlit as st
import time
from engine import analyze
from ml_engine import predict_spam

# ── SVG Icon Library (clean line-icons, replaces emoji for a polished look) ──
ICONS = {
    "eagle": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 12l4 2 2 6 4-4 4 4 2-6 4-2z"/></svg>',
    "shield": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l8 4v6c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V6z"/></svg>',
    "mail": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M2 6l10 7 10-7"/></svg>',
    "radar": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/><path d="M12 3v4M12 17v4M3 12h4M17 12h4"/></svg>',
    "hook": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3v10a4 4 0 008 0V8"/><circle cx="6" cy="3" r="1.5" fill="currentColor"/><path d="M18 14l2 2-4 4"/></svg>',
    "newspaper": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h13a2 2 0 012 2v13a1 1 0 01-1 1H6a2 2 0 01-2-2z"/><path d="M4 4v14a2 2 0 002 2"/><path d="M8 8h7M8 12h7M8 16h4"/></svg>',
    "alert-triangle": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l10 18H2z"/><path d="M12 10v4M12 17.5v.01"/></svg>',
    "dollar": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v10M9.5 9.5c0-1.4 1.2-2 2.5-2s2.5.8 2.5 2-1 1.6-2.5 2-2.5.7-2.5 2 1.1 2 2.5 2 2.5-.6 2.5-2"/></svg>',
    "flask": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 2h6M10 2v6l-5 11a1.5 1.5 0 001.4 2h11.2a1.5 1.5 0 001.4-2L14 8V2"/><path d="M8.5 14h7"/></svg>',
    "check-circle": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/></svg>',
    "alert": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l9 16H3z"/><path d="M12 9.5v3.5M12 16v.01"/></svg>',
    "x-octagon": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8 2h8l6 6v8l-6 6H8l-6-6V8z"/><path d="M9.5 9.5l5 5M14.5 9.5l-5 5"/></svg>',
    "brain": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3a3 3 0 00-3 3v1a3 3 0 00-2 5 3 3 0 002 5v1a3 3 0 003 3M15 3a3 3 0 013 3v1a3 3 0 012 5 3 3 0 01-2 5v1a3 3 0 01-3 3M9 3a3 3 0 016 0M9 21a3 3 0 006 0"/></svg>',
    "shield-check": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l8 4v6c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V6z"/><path d="M9 12l2 2 4-4"/></svg>',
    "satellite": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="2"/><path d="M5 5l3 3M19 5l-3 3M5 19l3-3M19 19l-3-3"/><path d="M2 5l3-3M22 5l-3-3M2 19l3 3M22 19l-3 3"/></svg>',
    "pencil": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 013 3L7 19l-4 1 1-4z"/></svg>',
    "clock": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>',
    "link": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 17H7a5 5 0 010-10h2M15 7h2a5 5 0 010 10h-2M8 12h8"/></svg>',
    "lock": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="11" width="16" height="9" rx="2"/><path d="M8 11V7a4 4 0 018 0v4"/></svg>',
    "gift": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="9" width="18" height="11" rx="1"/><path d="M3 9v0a3 3 0 016 0M21 9v0a3 3 0 00-6 0M12 9v11M3 9h18"/></svg>',
    "eye": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/></svg>',
    "spiral": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 12a4 4 0 11-4-4M12 12a8 8 0 10-8-8M12 12a4 4 0 004 4M12 12a8 8 0 008 8"/></svg>',
    "megaphone": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11v2a1 1 0 001 1h2l4 4V6L6 10H4a1 1 0 00-1 1z"/><path d="M14 7a4 4 0 010 10M17 4a8 8 0 010 16"/></svg>',
    "sword": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 19l9-9M14 10l5-5 2 2-5 5M14 10l3 3M5 19l-2 2M5 19l2 2"/></svg>',
    "ban": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M6 6l12 12"/></svg>',
    "trending-up": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/></svg>',
    "bar-chart": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 20V10M12 20V4M19 20v-7"/></svg>',
    "id-card": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="20" height="14" rx="2"/><circle cx="8" cy="12" r="2"/><path d="M14 10h6M14 14h4"/></svg>',
    "coins": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="9" r="6"/><path d="M14.5 6a6 6 0 11-.1 12.1M9 9h0"/></svg>',
    "activity": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 8L9 4l-3 8H2"/></svg>',
    "theater-masks": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="10" r="6"/><circle cx="15" cy="14" r="6"/><path d="M7 9h0M11 9h0M13 15h0M17 15h0"/></svg>',
}

def icon(name, color="currentColor", size=None):
    """Return an inline SVG icon string with a given color (and optional size override)."""
    svg = ICONS.get(name, "")
    svg = svg.replace("currentColor", color)
    if size:
        svg = svg.replace('width="16"', f'width="{size}"').replace('height="16"', f'height="{size}"')
        svg = svg.replace('width="18"', f'width="{size}"').replace('height="18"', f'height="{size}"')
        svg = svg.replace('width="14"', f'width="{size}"').replace('height="14"', f'height="{size}"')
        svg = svg.replace('width="22"', f'width="{size}"').replace('height="22"', f'height="{size}"')
    return f'<span style="display:inline-flex; vertical-align:middle;">{svg}</span>'

# ── Page Setup ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Garud AI – Threat Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS — Indigo Dark Theme ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0a0e1a;
    color: #cbd3e6;
}
.main { background-color: #0a0e1a; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem !important; max-width: 1180px; position: relative; z-index: 1; }

/* ── Animated circuit-grid backdrop ── */
.stApp {
    background-color: #0a0e1a;
    background-image:
        linear-gradient(rgba(99,102,241,0.07) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.07) 1px, transparent 1px),
        radial-gradient(circle at 15% 0%, rgba(99,102,241,0.10), transparent 45%),
        radial-gradient(circle at 85% 100%, rgba(56,189,248,0.06), transparent 45%);
    background-size: 42px 42px, 42px 42px, auto, auto;
    background-position: 0 0, 0 0, 0 0, 0 0;
    background-attachment: fixed;
    animation: gridDrift 60s linear infinite;
    position: relative;
}

@keyframes gridDrift {
    0%   { background-position: 0 0, 0 0, 0 0, 0 0; }
    100% { background-position: 420px 420px, 420px 420px, 0 0, 0 0; }
}

/* Traveling circuit pulses — thin glowing lines that sweep across the grid */
.stApp::before, .stApp::after {
    content: "";
    position: fixed;
    pointer-events: none;
    z-index: 0;
}
.stApp::before {
    top: 18%;
    left: -20%;
    width: 45%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.55), transparent);
    box-shadow: 0 0 8px rgba(99,102,241,0.4);
    animation: travelRight 8s ease-in-out infinite;
}
.stApp::after {
    top: 68%;
    right: -20%;
    width: 35%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56,189,248,0.5), transparent);
    box-shadow: 0 0 8px rgba(56,189,248,0.35);
    animation: travelLeft 11s ease-in-out infinite;
    animation-delay: 2.5s;
}
@keyframes travelRight {
    0%   { left: -45%; opacity: 0; }
    10%  { opacity: 1; }
    85%  { opacity: 1; }
    100% { left: 105%; opacity: 0; }
}
@keyframes travelLeft {
    0%   { right: -35%; opacity: 0; }
    10%  { opacity: 1; }
    85%  { opacity: 1; }
    100% { right: 105%; opacity: 0; }
}

/* Respect users who've asked for less motion */
@media (prefers-reduced-motion: reduce) {
    .stApp, .stApp::before, .stApp::after { animation: none !important; }
}

/* ── Header ── */
.g-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #1c2436;
    margin-bottom: 2rem;
}
.g-brand { display: flex; align-items: center; gap: 12px; }
.g-brand-icon {
    width: 42px; height: 42px;
    border-radius: 11px;
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem;
    box-shadow: 0 4px 16px rgba(99,102,241,0.35);
}
.g-brand-text h1 {
    font-size: 1.3rem;
    font-weight: 700;
    color: #f1f4fb;
    margin: 0;
    letter-spacing: -0.01em;
}
.g-brand-text p {
    font-size: 0.75rem;
    color: #5b6478;
    margin: 2px 0 0;
}
.g-status {
    display: flex;
    align-items: center;
    gap: 7px;
    background: #131a2c;
    border: 1px solid #232c44;
    border-radius: 999px;
    padding: 6px 14px;
    font-size: 12px;
    color: #818cf8;
    font-weight: 500;
}
.g-status-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #4ade80;
}

/* ── Input Card ── */
.g-input-card {
    background: #0f1525;
    border: 1px solid #1c2436;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}
.g-card-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: #818cf8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.85rem;
    display: flex;
    align-items: center;
    gap: 6px;
}

.stTextArea textarea {
    background: #0a0e1a !important;
    border: 1px solid #232c44 !important;
    border-radius: 10px !important;
    color: #e2e7f5 !important;
    font-size: 14.5px !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
.stTextArea textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder { color: #3f4a63 !important; }

.stButton > button {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 1.5rem !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    width: 100% !important;
    transition: opacity 0.15s, transform 0.15s !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.3) !important;
}
.stButton > button:hover { opacity: 0.92 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* ── Module legend (left rail) ── */
.legend-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid #161d30;
    font-size: 12.5px;
    color: #7c869c;
}
.legend-row:last-child { border-bottom: none; }
.legend-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.legend-name { color: #c2c9dc; font-weight: 500; }

/* ── Overall Risk Banner ── */
.risk-banner {
    border-radius: 16px;
    padding: 1.85rem 2.25rem;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.5rem;
    background: #0f1525;
    border: 1px solid #1c2436;
}
.rb-score {
    font-size: 3.2rem;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.02em;
}
.rb-label { font-size: 0.8rem; color: #5b6478; margin-top: 6px; font-weight: 500; }
.rb-level {
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: -0.01em;
}
.rb-sublabel { font-size: 0.78rem; color: #5b6478; margin-top: 4px; text-align: right; }
.rb-pills { display: flex; gap: 4px; margin-top: 10px; justify-content: flex-end; }
.rb-pill { width: 10px; height: 22px; border-radius: 3px; }

/* ── Stats strip ── */
.stats-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 1.5rem;
}
.stat-box {
    background: #0f1525;
    border: 1px solid #1c2436;
    border-radius: 12px;
    padding: 1rem 1.1rem;
}
.stat-box .stat-num { font-size: 1.5rem; font-weight: 700; color: #f1f4fb; line-height: 1; }
.stat-box .stat-lbl { font-size: 0.75rem; color: #5b6478; margin-top: 5px; font-weight: 500; }

/* ── Module Grid ── */
.module-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    margin-bottom: 1.25rem;
}
@media (max-width: 900px) {
    .module-grid { grid-template-columns: repeat(3, 1fr); }
    .stats-strip { grid-template-columns: repeat(2, 1fr) !important; }
}
@media (max-width: 600px) {
    .module-grid { grid-template-columns: repeat(2, 1fr); }
}
.mod-card {
    background: #0f1525;
    border: 1px solid #1c2436;
    border-radius: 14px;
    padding: 1.15rem 1rem;
    transition: border-color 0.15s, transform 0.15s;
}
.mod-card:hover { border-color: #2d3a5c; transform: translateY(-2px); }
.mod-card:focus-within { outline: 2px solid #6366f1; outline-offset: 2px; }

@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.risk-banner, .stats-strip, .ml-card, .signals-card, .tips-card, .safe-banner {
    animation: fadeSlideUp 0.4s ease-out both;
}
.risk-banner  { animation-delay: 0.00s; }
.stats-strip  { animation-delay: 0.08s; }
.ml-card      { animation-delay: 0.42s; }
.signals-card, .safe-banner { animation-delay: 0.50s; }
.tips-card    { animation-delay: 0.58s; }

/* Module grid: each card animates in sequence, left to right */
.module-grid { animation: none; }
.module-grid .mod-card {
    animation: fadeSlideUp 0.4s ease-out both;
    opacity: 0;
}
.module-grid .mod-card:nth-child(1) { animation-delay: 0.16s; }
.module-grid .mod-card:nth-child(2) { animation-delay: 0.21s; }
.module-grid .mod-card:nth-child(3) { animation-delay: 0.26s; }
.module-grid .mod-card:nth-child(4) { animation-delay: 0.31s; }
.module-grid .mod-card:nth-child(5) { animation-delay: 0.36s; }

@media (prefers-reduced-motion: reduce) {
    .risk-banner, .stats-strip, .module-grid .mod-card, .ml-card, .signals-card, .tips-card, .safe-banner {
        animation: none !important;
        opacity: 1 !important;
    }
}

/* ── Visible focus rings for keyboard navigation (a11y) ── */
.stTextArea textarea:focus-visible,
.stButton > button:focus-visible {
    outline: 2px solid #818cf8 !important;
    outline-offset: 2px !important;
}
.sig-chip:focus-visible, .legend-row:focus-visible {
    outline: 2px solid #818cf8;
    outline-offset: 2px;
}
.mod-icon-circle {
    width: 34px; height: 34px;
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.05rem;
    margin-bottom: 0.7rem;
}
.mod-name { font-size: 0.72rem; font-weight: 600; color: #5b6478; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 4px; }
.mod-score { font-size: 1.55rem; font-weight: 700; line-height: 1; letter-spacing: -0.01em; }
.mod-level { font-size: 0.72rem; font-weight: 600; margin-top: 3px; }
.mod-track { background: #1c2436; border-radius: 999px; height: 4px; margin-top: 0.7rem; overflow: hidden; }
.mod-fill { height: 4px; border-radius: 999px; }

/* ── ML Verdict Card ── */
.ml-card {
    background: #0f1525;
    border: 1px solid #1c2436;
    border-radius: 16px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.5rem;
}
.ml-left { display: flex; align-items: flex-start; gap: 14px; max-width: 65%; }
.ml-badge {
    width: 38px; height: 38px;
    border-radius: 10px;
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
}
.ml-title { font-size: 0.95rem; font-weight: 600; color: #e2e7f5; margin: 0 0 4px; }
.ml-desc { font-size: 0.8rem; color: #5b6478; line-height: 1.55; margin: 0; }
.ml-right { text-align: right; flex-shrink: 0; }
.ml-score { font-size: 1.9rem; font-weight: 700; line-height: 1; }
.ml-label { font-size: 0.75rem; font-weight: 600; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.04em; }

/* ── Signals Section ── */
.signals-card {
    background: #0f1525;
    border: 1px solid #1c2436;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.25rem;
}
.section-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: #818cf8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 1rem;
}
.sig-group { margin-bottom: 0.9rem; }
.sig-group:last-child { margin-bottom: 0; }
.sig-group-name {
    font-size: 0.74rem;
    font-weight: 600;
    color: #7c869c;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 6px;
}
.sig-chips { display: flex; flex-wrap: wrap; gap: 6px; }
.sig-chip {
    background: #131a2c;
    border: 1px solid #232c44;
    border-radius: 999px;
    padding: 5px 13px;
    font-size: 0.78rem;
    color: #c2c9dc;
    font-weight: 500;
    transition: border-color 0.15s, background 0.15s;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}
.sig-chip:hover { border-color: #6366f1; background: #161d30; }

/* ── Tips Section ── */
.tips-card {
    background: #0f1525;
    border: 1px solid #1c2436;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.25rem;
}
.tip-line {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 0.55rem 0;
    border-bottom: 1px solid #161d30;
    font-size: 0.85rem;
    color: #a3acc2;
    line-height: 1.5;
}
.tip-line:last-child { border-bottom: none; padding-bottom: 0; }
.tip-marker { color: #818cf8; font-weight: 700; flex-shrink: 0; }

/* ── Safe state banner ── */
.safe-banner {
    background: #0f1f17;
    border: 1px solid #1d4e3a;
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    text-align: center;
    color: #4ade80;
    font-weight: 500;
    font-size: 0.9rem;
    margin-bottom: 1.25rem;
}

/* ── Idle state ── */
.idle-state {
    text-align: center;
    padding: 3.5rem 2rem;
    color: #2d3650;
}

@media (max-width: 640px) {
    .ml-card { flex-direction: column; align-items: flex-start; gap: 1rem; }
    .ml-right { text-align: left; }
    .ml-left { max-width: 100%; }
    .risk-banner { flex-direction: column; align-items: flex-start; gap: 1rem; }
    .rb-sublabel, .rb-pills { text-align: left; justify-content: flex-start; }
    .block-container { padding: 1.25rem 1.25rem 3rem !important; }
}

/* ── Footer ── */
.g-footer {
    text-align: center;
    color: #2d3650;
    font-size: 0.75rem;
    padding-top: 1.5rem;
    border-top: 1px solid #131a2c;
    margin-top: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="g-header">
    <div class="g-brand">
        <div class="g-brand-icon">{icon('eagle', color='white', size=22)}</div>
        <div class="g-brand-text">
            <h1>Garud AI</h1>
            <p>Threat Intelligence Dashboard · v4.0</p>
        </div>
    </div>
    <div class="g-status">
        <div class="g-status-dot"></div>
        Engine Active
    </div>
</div>
""", unsafe_allow_html=True)

# ── LAYOUT ────────────────────────────────────────────────────────────────────
left_col, right_col = st.columns([1, 1.55], gap="large")

with left_col:
    st.markdown('<div class="g-input-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="g-card-label">{icon("mail", color="#818cf8", size=15)} Message to analyze</div>', unsafe_allow_html=True)
    user_text = st.text_area(
        label="Message to analyze",
        placeholder="Paste any message, email, headline, or chat here...",
        height=170,
        label_visibility="collapsed",
        help="Paste the SMS, email, or message text you want Garud AI to scan for threats.",
        key="garud_input",
    )
    char_count = len(user_text) if user_text else 0
    st.markdown(f'<div style="text-align:right; font-size:0.7rem; color:#3f4a63; margin-top:-0.6rem; margin-bottom:0.6rem;">{char_count} characters</div>', unsafe_allow_html=True)
    analyze_btn = st.button("Analyze Message", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Module legend
    st.markdown('<div class="g-input-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="g-card-label">{icon("satellite", color="#818cf8", size=15)} Detection modules</div>', unsafe_allow_html=True)
    MODULES_INFO = [
        ("#6366f1", "hook",       "Scam Detection",  "Phishing, urgency, fake prizes"),
        ("#38bdf8", "newspaper",  "Fake News",       "Sensationalism, conspiracy"),
        ("#f472b6", "alert-triangle", "Hate Speech", "Threats, slurs, discrimination"),
        ("#fb923c", "dollar",     "Financial Fraud", "Ponzi, advance fee, ID theft"),
        ("#a78bfa", "flask",      "Misinformation",  "Health myths, science denial"),
    ]
    for color, icon_name, name, desc in MODULES_INFO:
        st.markdown(f"""
        <div class="legend-row">
            <div class="legend-dot" style="background:{color};"></div>
            <span style="display:inline-flex; align-items:center; gap:6px;">{icon(icon_name, color=color, size=14)} <span class="legend-name">{name}</span> — {desc}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    if not analyze_btn:
        st.markdown(f"""
        <div class="g-input-card idle-state">
            <div style="margin-bottom:0.75rem; opacity:0.3; display:flex; justify-content:center;">{icon('eagle', color='#5b6478', size=44)}</div>
            <div style="font-size:0.95rem; font-weight:600; color:#5b6478;">Awaiting input</div>
            <div style="font-size:0.8rem; color:#3f4a63; margin-top:4px;">Paste a message on the left and click analyze</div>
        </div>
        """, unsafe_allow_html=True)

    elif not user_text.strip():
        st.markdown(f"""
        <div class="g-input-card idle-state" role="alert">
            <div style="margin-bottom:0.6rem; opacity:0.5; display:flex; justify-content:center; color:#fbbf24;">{icon('pencil', color='#fbbf24', size=28)}</div>
            <div style="font-size:0.95rem; font-weight:600; color:#fbbf24;">No message yet</div>
            <div style="font-size:0.8rem; color:#3f4a63; margin-top:4px;">Please paste a message on the left before analyzing</div>
        </div>
        """, unsafe_allow_html=True)

    else:
        with st.spinner("Scanning for threats..."):
            time.sleep(0.3)
            result = analyze(user_text)
            ml_result = predict_spam(user_text)

        ov = result["overall"]
        RISK_ICON_NAMES = {"Low": "check-circle", "Medium": "alert", "High": "x-octagon"}
        ov_icon_svg = icon(RISK_ICON_NAMES.get(ov["level"], "alert"), color=ov["color"], size=15)

        st.markdown('<div role="status" aria-live="polite" aria-label="Analysis complete">', unsafe_allow_html=True)

        # ── Overall Risk Banner ──
        rb_html = f'<div class="risk-banner" style="border-color:{ov["color"]}40;">'
        rb_html += f'<div><div class="rb-score" style="color:{ov["color"]}">{ov["score"]}%</div>'
        rb_html += '<div class="rb-label">Overall Threat Score</div></div>'
        rb_html += f'<div><div class="rb-level" style="color:{ov["color"]}; display:flex; align-items:center; gap:6px; justify-content:flex-end;">{ov_icon_svg}{ov["level"]} Risk</div>'
        rb_html += '<div class="rb-sublabel">Garud AI Verdict</div>'
        filled = ov["score"] // 14
        pills = "".join(
            f'<div class="rb-pill" style="background:{ov["color"] if i < filled else "#1c2436"};"></div>'
            for i in range(7)
        )
        rb_html += f'<div class="rb-pills">{pills}</div></div></div>'
        st.markdown(rb_html, unsafe_allow_html=True)

        # ── Stats Strip ──
        total_sigs = sum(len(result[k]["signals"]) for k in ["scam","fake_news","toxic","fraud","misinfo"])
        active_mods = sum(1 for k in ["scam","fake_news","toxic","fraud","misinfo"] if result[k]["score"] >= 30)
        st.markdown(f"""
        <div class="stats-strip">
            <div class="stat-box"><div class="stat-num" style="color:#818cf8;">{total_sigs}</div><div class="stat-lbl">Signals Found</div></div>
            <div class="stat-box"><div class="stat-num" style="color:#38bdf8;">{active_mods}</div><div class="stat-lbl">Modules Triggered</div></div>
            <div class="stat-box"><div class="stat-num" style="color:{ov['color']};">{ov['score']}%</div><div class="stat-lbl">Risk Score</div></div>
            <div class="stat-box"><div class="stat-num" style="color:#a78bfa;">5</div><div class="stat-lbl">Modules Checked</div></div>
        </div>
        """, unsafe_allow_html=True)

        # ── Module Cards ──
        MOD_META = [
            ("scam",      "#6366f1", "hook",            "Scam"),
            ("fake_news", "#38bdf8", "newspaper",       "Fake News"),
            ("toxic",     "#f472b6", "alert-triangle",  "Hate"),
            ("fraud",     "#fb923c", "dollar",          "Fraud"),
            ("misinfo",   "#a78bfa", "flask",           "Misinfo"),
        ]
        cards = ""
        MOD_RISK_ICON_NAMES = {"Low": "check-circle", "Medium": "alert", "High": "x-octagon"}
        for key, color, icon_name, label in MOD_META:
            m = result[key]
            risk_icon_svg = icon(MOD_RISK_ICON_NAMES.get(m["level"], "alert"), color=m["color"], size=12)
            cards += f"""
            <div class="mod-card" tabindex="0" aria-label="{label}: {m['score']} percent, {m['level']} risk">
                <div class="mod-icon-circle" style="background:{color}1a; color:{color};">{icon(icon_name, color=color, size=17)}</div>
                <div class="mod-name">{label}</div>
                <div class="mod-score" style="color:{m['color']};">{m['score']}%</div>
                <div class="mod-level" style="color:{m['color']}; display:flex; align-items:center; gap:4px;">{risk_icon_svg}{m['level']}</div>
                <div class="mod-track"><div class="mod-fill" style="width:{m['score']}%; background:{color};"></div></div>
            </div>"""
        st.markdown(f'<div class="module-grid">{cards}</div>', unsafe_allow_html=True)

        # ── ML Verdict Card ──
        if ml_result["available"]:
            mc = ml_result["color"]
            st.markdown(f"""
            <div class="ml-card">
                <div class="ml-left">
                    <div class="ml-badge">{icon('brain', color='white', size=16)}</div>
                    <div>
                        <p class="ml-title">AI-Powered Verdict (Machine Learning)</p>
                        <p class="ml-desc">Naive Bayes classifier trained on 5,500+ real SMS messages. Independent statistical prediction — confirms or contrasts the rule-based result above.</p>
                    </div>
                </div>
                <div class="ml-right">
                    <div class="ml-score" style="color:{mc};">{ml_result['score']}%</div>
                    <div class="ml-label" style="color:{mc};">{ml_result['label']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="ml-card">
                <div class="ml-left">
                    <div class="ml-badge">{icon('brain', color='white', size=16)}</div>
                    <div>
                        <p class="ml-title">AI-Powered Verdict (Machine Learning)</p>
                        <p class="ml-desc">Model not found. Run <code>python train_model.py</code> once to enable this feature.</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Detected Signals ──
        any_signal = any(result[k]["signals"] for k in ["scam","fake_news","toxic","fraud","misinfo"])

        if any_signal:
            sig_html = f'<div class="signals-card"><div class="section-label" style="display:flex; align-items:center; gap:6px;">{icon("alert-triangle", color="#818cf8", size=14)}Detected Threat Signals</div>'
            for key, color, icon_name, label in MOD_META:
                sigs = result[key]["signals"]
                if sigs:
                    chips = "".join(f'<span class="sig-chip">{icon(s["icon"], color=color, size=12)}{s["name"]}</span>' for s in sigs)
                    sig_html += f"""
                    <div class="sig-group">
                        <div class="sig-group-name"><div class="legend-dot" style="background:{color};"></div>{icon(icon_name, color=color, size=13)}{label}</div>
                        <div class="sig-chips">{chips}</div>
                    </div>"""
            sig_html += '</div>'
            st.markdown(sig_html, unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="safe-banner" style="display:flex; align-items:center; justify-content:center; gap:8px;">{icon("check-circle", color="#4ade80", size=16)}No threat signals detected — this message appears safe.</div>', unsafe_allow_html=True)

        # ── Safety Tips ──
        tips_html = f'<div class="tips-card"><div class="section-label" style="display:flex; align-items:center; gap:6px;">{icon("shield-check", color="#818cf8", size=14)}Safety Recommendations</div>'
        for tip in result["tips"]:
            tips_html += f'<div class="tip-line"><span class="tip-marker">›</span><span>{tip}</span></div>'
        tips_html += '</div>'
        st.markdown(tips_html, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)  # close aria-live wrapper

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="g-footer" style="display:flex; align-items:center; justify-content:center; gap:6px;">
    Garud AI v4.0 · Rule-Based + ML Hybrid Detection · Hackathon Edition {icon('eagle', color='#2d3650', size=12)}
</div>
""", unsafe_allow_html=True)
