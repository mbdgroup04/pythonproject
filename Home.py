import streamlit as st

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
    "Personal Strategy": "pages/Personal_Strategy.py",
    "Our Team": "pages/Our_Team.py"
}

for page_name, file_path in PAGES.items():
    if file_path:
        st.sidebar.page_link(file_path, label=page_name)
    else:
        st.sidebar.write(f"### {page_name}")
col1,col2,col3=st.columns(3)
with col2:
    st.image("data/logo.jpg", width=200)

st.markdown(f'<p style="font-size:25px; text-align:left; "><br></p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:35px; text-align:left; ">Welcome to <b>TradeVision AI</b> -- Your Intelligent Market Companion</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:15px; text-align:left; ">You are now able to harness the power of AI for smarter trading decisions</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:25px; text-align:left; "><br></p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:20px; text-align:left; "><b>TradeVision AI</b> is a cutting-edge, AI-driven market prediction platform designed to give traders a competitive edge. By leveraging advanced machine learning models and real-time financial data, we empower you with actionable insights for informed investment decisions.</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:25px; text-align:left; "><br></p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:25px; text-align:left; font-weight:bold;">But why TradeVision AI?</p>', unsafe_allow_html=True)
st.markdown("""
- **AI-Powered Market Forecasts** – Our predictive models analyze historical trends and real-time market signals to anticipate stock movements with precision.
- **Data-Driven Insights** – Access in-depth analytics and visualizations that decode complex financial patterns, helping you stay ahead of market trends.
- **Live Data Integration** – Stay updated with real-time stock prices, financial indicators, and trading signals, seamlessly pulled from the SimFin API.
- **Smart Trading Signals** – Receive clear Buy/Sell/Hold recommendations based on predictive analytics, simplifying decision-making for all traders.
- **Cloud-Based & Accessible Anywhere** – Our sleek and interactive web app ensures seamless access from any device, anytime.
""")
st.markdown(f'<p style="font-size:25px; text-align:left; "><br></p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:25px; text-align:left;font-weight:bold;">Ready to Elevate Your Trading Game?</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:25px; text-align:left; ">Sign up today and experience the future of AI-driven trading with TradeVision AI!</p>', unsafe_allow_html=True)
website_url = "https://pythonproject-fsaanv6ra5zqqx7r2wch4a.streamlit.app/Trading_Recommendation"
if st.button('I WANT TO PREDICT'):
    st.markdown(f'<meta http-equiv="refresh" content="0; URL={website_url}">', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:25px; text-align:left; "><br></p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:20px; text-align:left; ">You are now using the free version - great start!🚀 In the premium version, you will unlock multi-day forecasts, deeper financial analysis, and smarter trading strategies to stay ahead of the market!</p>', unsafe_allow_html=True)