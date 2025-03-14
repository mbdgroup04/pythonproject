import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import pages.functions.PySimFin as psf
from pages.functions.Exceptions import InvalidTicker
import datetime
import pickle

def load_data():
    try:
        stock_data = pd.read_csv("data/shareprices.csv")
        stock_data["Date"] = pd.to_datetime(stock_data["Date"])
        return stock_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

stock_data = load_data()

if stock_data.empty:
    st.error("⚠️ No stock data available. Please upload a valid CSV file.")
    st.stop()

if "Ticker" not in stock_data.columns or "Close" not in stock_data.columns:
    st.error("The dataset does not contain the required 'Ticker' or 'Close' column.")
    st.stop()

selected_ticker = st.selectbox("📌 Choose a stock ticker:", stock_data["Ticker"].unique())

stock_df = stock_data[stock_data["Ticker"] == selected_ticker]

if stock_df.empty:
    st.warning("⚠️ No stock data available for this company.")
    st.stop() 

last_close_price = round(stock_df.iloc[-1]["Close"],2)

if "toggle" not in st.session_state:
    st.session_state["toggle"] = False

if st.button("🔀 Randomize Prediction"):
    next_day_price = last_close_price * (1 + (0.05 * (-1 if st.session_state["toggle"] else 1)))
    st.session_state["toggle"] = not st.session_state["toggle"]
else:
    next_day_price = round(last_close_price * 1.02,2)

upper_threshold = round(last_close_price * 1.10,2)
lower_threshold = round(last_close_price * 0.95,2)

if next_day_price > upper_threshold:
    action = "✅ BUY"
    action_color = "green"
elif lower_threshold <= next_day_price <= upper_threshold:
    action = "⏳ HOLD"
    action_color = "yellow"
else:
    action = "❌ SELL"
    action_color = "red"

st.markdown(f"""
### 📈 Trading Decision
- **Predicted Price:** ${next_day_price:.2f}
- **Last Close Price:** ${last_close_price:.2f}
- **Action:** <span style="color:{action_color}; font-weight:bold;">{action}</span>
""", unsafe_allow_html=True)

st.markdown("### 📊 Historical Stock Price Trend")
fig = px.line(stock_df, x="Date", y="Close", title=f"{selected_ticker} Stock Price Over Time")
st.plotly_chart(fig, use_container_width=True)

st.markdown("### 🔍 Predicted Price vs. Trading Thresholds")
threshold_df = pd.DataFrame({
    "Category": ["Lower Threshold (-5%)", "Last Close Price", "Upper Threshold (+10%)", "Predicted Price"],
    "Price": [lower_threshold, last_close_price, upper_threshold, next_day_price]
})

fig_threshold = px.bar(threshold_df, x="Category", y="Price", 
                        color="Category", title="Thresholds & Predicted Price", text="Price")
fig_threshold.update_layout(showlegend=False)
st.plotly_chart(fig_threshold, use_container_width=True)


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