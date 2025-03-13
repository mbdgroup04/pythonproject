import streamlit as st
import pandas as pd
import plotly.express as px

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

# 📈 Show a line chart of historical stock prices
st.markdown("### 📈 Historical Stock Price Trend")
fig = px.line(stock_df, x="Date", y="Close", title=f"{selected_ticker} Stock Price Over Time")
st.plotly_chart(fig, use_container_width=True)

# ✅ Placeholder: Add Machine Learning Predictions Here
st.markdown("### 🔍 Future Stock Price Predictions (Coming Soon!)")
st.info("📊 Predictive analytics models will be integrated soon.")
