import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import pages.functions.PySimFin as psf
from pages.functions.Exceptions import InvalidTicker
import datetime
import pickle

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
    "Meet The Team": "pages/Meet_the_Team.py",
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

selected_ticker = st.selectbox("📌 Choose a stock ticker:", stock_data["Ticker"].unique())

stock_df = stock_data[stock_data["Ticker"] == selected_ticker]

st.markdown("### 📊 Historical Stock Price Trend")
fig = px.line(stock_df, x="Date", y="Close", title=f"{selected_ticker} Stock Price Over Time")
st.plotly_chart(fig, use_container_width=True)

st.title("🔮 Market Predictions")
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)

st.markdown("""
    📌 **This page provides predictive analytics based on historical stock data.**
    
    - **View stock price trends**
    - **Analyze predictive models**
    - **Compare predicted vs. actual prices**
""")

if stock_data.empty:
    st.error("No stock data available. Please upload a valid CSV file.")
    st.stop()

if "Ticker" not in stock_data.columns:
    st.error("The dataset does not contain a 'Ticker' column.")
    st.stop()

st.markdown("### Select a Company for Prediction")
selected_ticker = st.selectbox("Choose a stock ticker:", stock_data["Ticker"].unique())

stock_df = stock_data[stock_data["Ticker"] == selected_ticker]

if stock_df.empty:
    st.warning("No stock data available for this company.")
    st.stop()

min_date = datetime.date(2018, 1, 1)
max_date = datetime.date.today()

st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
col1,col2=st.columns(2)
with col1:
    start_date=str(st.date_input('Please insert start date',min_value=min_date,max_value=max_date))
with col2:
    end_date=str(st.date_input('Please insert end date',min_value=min_date,max_value=max_date))
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
st.title("Prediction result:")
input_data=psf.PySimFin().get_share_prices(selected_ticker,start_date,end_date)
latest_data=np.array([input_data],dtype=object)

model_AAPL=pickle.load(open('models/picklemodel_AAPL.pkl','rb'))
model_AMZN=pickle.load(open('models/picklemodel_AMZN.pkl','rb'))
model_GOOG=pickle.load(open('models/picklemodel_GOOG.pkl','rb'))
model_MSFT=pickle.load(open('models/picklemodel_MSFT.pkl','rb'))
model_TSLA=pickle.load(open('models/picklemodel_TSLA.pkl','rb'))

if selected_ticker=='AAPL':
    prediction=model_AAPL.predict(latest_data)[0]
elif selected_ticker=='AMZN':
    prediction=model_AMZN.predict(latest_data)[0]
elif selected_ticker=='GOOG':
    prediction=model_GOOG.predict(latest_data)[0]
elif selected_ticker=='MSFT':
    prediction=model_MSFT.predict(latest_data)[0]
elif selected_ticker=='TSLA':
    prediction=model_TSLA.predict(latest_data)[0]
else:
    raise InvalidTicker('Please insert a valid ticker.')

st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
col1,col2,col3=st.columns(3)
with col2:
    st.markdown(f"<p style='font-size:60px; text-align:left; font-weight:bold; '>{round(prediction,2)} $</p>", unsafe_allow_html=True)