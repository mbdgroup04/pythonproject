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
    "Home": "Home.py",
    "Company Information": "pages/Company_Information.py",
    "Trading Recommendation": "pages/Trading_Recommendation.py",
    "Our Team": "pages/Our_Team.py",
    "Personal Testing": None
}

for page_name, file_path in PAGES.items():
    if file_path:
        st.sidebar.page_link(file_path, label=page_name)
    else:
        st.sidebar.write(f"### {page_name}")

def load_data():
    try:
        stock_data = pd.read_csv("data/shareprices.csv")
        stock_data["Date"] = pd.to_datetime(stock_data["Date"])
        return stock_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

stock_data = load_data()

col1,col2,col3=st.columns(3)
with col2:
    st.image("data/logo.jpg", width=200)
st.markdown(f'<p style="font-size:40px; text-align:center; font-weight:bold; ">Personal Testing</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:20px; text-align:left; "><b>TradeVision AI</b> wants to show you how well it can do even with fictional data you input in the system.</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; ">Select a company to predict the closing price for tomorrow:</p>', unsafe_allow_html=True)
comp_name = st.selectbox("", ['Apple','Amazon','Google','Microsoft','Tesla'])
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; ">First fictional closing price for {comp_name}</p>', unsafe_allow_html=True)
fict1=st.slider("",min_value=0.0,max_value=500.0,value=150.0,step=0.1)