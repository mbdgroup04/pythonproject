import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
@st.cache_data
def load_data():
    try:
        stock_data = pd.read_csv("shareprices.csv")  # Ensure the file exists
        stock_data["Date"] = pd.to_datetime(stock_data["Date"])  # Convert Date column
        return stock_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

stock_data = load_data()

# Ensure stock_data is not empty before proceeding
if stock_data.empty:
    st.error("⚠️ No stock data available. Please upload a valid CSV file.")
    st.stop()

# Check if 'Ticker' exists in the dataset
if "Ticker" not in stock_data.columns or "Close" not in stock_data.columns:
    st.error("The dataset does not contain the required 'Ticker' or 'Close' column.")
    st.stop()

# Select a stock ticker
selected_ticker = st.selectbox("📌 Choose a stock ticker:", stock_data["Ticker"].unique())

# Filter stock data for the selected ticker
stock_df = stock_data[stock_data["Ticker"] == selected_ticker]

# Ensure stock data exists
if stock_df.empty:
    st.warning("⚠️ No stock data available for this company.")
    st.stop()  # Replaces `return`

# Get the last closing price (d-1)
last_close_price = stock_df.iloc[-1]["Close"]

# Initialize session state for toggling prediction
if "toggle" not in st.session_state:
    st.session_state["toggle"] = False

# Simulated next-day predicted price (Replace with an ML model when available)
if st.button("🔀 Randomize Prediction"):
    next_day_price = last_close_price * (1 + (0.05 * (-1 if st.session_state["toggle"] else 1)))
    st.session_state["toggle"] = not st.session_state["toggle"]
else:
    next_day_price = last_close_price * 1.02  # Default: +2% increase (for demo)

# Define thresholds
upper_threshold = last_close_price * 1.10  # +10% threshold
lower_threshold = last_close_price * 0.95  # -5% threshold

# Determine trading action
if next_day_price > upper_threshold:
    action = "✅ BUY"
    action_color = "green"
elif lower_threshold <= next_day_price <= upper_threshold:
    action = "⏳ HOLD"
    action_color = "yellow"
else:
    action = "❌ SELL"
    action_color = "red"

# 📊 Display Trading Decision
st.markdown(f"""
### 📈 Trading Decision
- **Predicted Price:** ${next_day_price:.2f}
- **Last Close Price:** ${last_close_price:.2f}
- **Action:** <span style="color:{action_color}; font-weight:bold;">{action}</span>
""", unsafe_allow_html=True)

# 📉 Historical Stock Prices
st.markdown("### 📊 Historical Stock Price Trend")
fig = px.line(stock_df, x="Date", y="Close", title=f"{selected_ticker} Stock Price Over Time")
st.plotly_chart(fig, use_container_width=True)

# 📊 Visualizing Prediction vs. Thresholds
st.markdown("### 🔍 Predicted Price vs. Trading Thresholds")
threshold_df = pd.DataFrame({
    "Category": ["Lower Threshold (-5%)", "Last Close Price", "Upper Threshold (+10%)", "Predicted Price"],
    "Price": [lower_threshold, last_close_price, upper_threshold, next_day_price]
})

fig_threshold = px.bar(threshold_df, x="Category", y="Price", 
                        color="Category", title="Thresholds & Predicted Price", text="Price")
fig_threshold.update_layout(showlegend=False)
st.plotly_chart(fig_threshold, use_container_width=True)
