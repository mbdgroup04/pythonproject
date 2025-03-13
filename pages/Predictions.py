import streamlit as st
import pandas as pd
import plotly.express as px
import pages.functions.PySimFin as psf
from pages.functions.Exceptions import InvalidTicker
import datetime
import pickle

# Load Data
@st.cache_data
def load_data():
    try:
        stock_data = pd.read_csv("shareprices.csv")  # Ensure this file has stock data
        stock_data["Date"] = pd.to_datetime(stock_data["Date"])  # Convert Date to datetime format
        return stock_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return empty DataFrame if error occurs

stock_data = load_data()

st.title("🔮 Market Predictions")
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)

st.markdown("""
    📌 **This page provides predictive analytics based on historical stock data.**
    
    - **View stock price trends**
    - **Analyze predictive models**
    - **Compare predicted vs. actual prices**
""")

# Ensure stock_data is not empty before proceeding
if stock_data.empty:
    st.error("No stock data available. Please upload a valid CSV file.")
    st.stop()

# Check if 'Ticker' exists in the dataset
if "Ticker" not in stock_data.columns:
    st.error("The dataset does not contain a 'Ticker' column.")
    st.stop()

# Dropdown to select a stock
st.markdown("### Select a Company for Prediction")
selected_ticker = st.selectbox("Choose a stock ticker:", stock_data["Ticker"].unique())

# Filter stock data for the selected ticker
stock_df = stock_data[stock_data["Ticker"] == selected_ticker]

# Ensure stock data exists
if stock_df.empty:
    st.warning("No stock data available for this company.")
    st.stop()  # Use st.stop() instead of return

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

model_AAPL=pickle.load(open('picklemodel_AAPL.pkl','rb'))
model_AMZN=pickle.load(open('picklemodel_AMZN.pkl','rb'))
model_GOOG=pickle.load(open('picklemodel_GOOG.pkl','rb'))
model_MSFT=pickle.load(open('picklemodel_MSFT.pkl','rb'))
model_TSLA=pickle.load(open('picklemodel_TSLA.pkl','rb'))

if selected_ticker=='AAPL':
    prediction=model_AAPL.predict(input_data)
elif selected_ticker=='AMZN':
    prediction=model_AMZN.predict(input_data)
elif selected_ticker=='GOOG':
    prediction=model_GOOG.predict(input_data)
elif selected_ticker=='MSFT':
    prediction=model_MSFT.predict(input_data)
elif selected_ticker=='TSLA':
    prediction=model_TSLA.predict(input_data)
else:
    raise InvalidTicker('Please insert a valid ticker.')

st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
st.markdown(f"<p style='font-size:20px; text-align:left; font-weight:bold; '>Next's day's price is: {prediction}</p>", unsafe_allow_html=True)