import streamlit as st
import pandas as pd

st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] ul {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

PAGES = {
    "Home": None,
    "Company Information": "pages/Company_Information.py",
    "Trading Recommendation": "pages/Trading_Recommendation.py",
    "Our Team": "pages/Our_Team.py",
}

for page_name, file_path in PAGES.items():
    if file_path:
        st.sidebar.page_link(file_path, label=page_name)
    else:
        st.sidebar.write(f"### {page_name}")
col1,col2,col3=st.columns(3)
with col2:
    st.image("data/logo.jpg", width=200)

st.markdown(f'<p style="font-size:35px; text-align:left; ">Welcome to <b>TradeVision AI</b> -- Your Intelligent Market Companion</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:15px; text-align:left; ">You are now able to harness the power of AI for smarter trading decisions</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:20px; text-align:left; "><b>TradeVision AI</b> is a cutting-edge, AI-driven market prediction platform designed to give traders a competitive edge. By leveraging advanced machine learning models and real-time financial data, we empower you with actionable insights for informed investment decisions.</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:25px; text-align:left; font-weight:bold;">But why TradeVision AI?</p>', unsafe_allow_html=True)
