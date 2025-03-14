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

selected_comp_name = st.selectbox("Please select a company:", stock_data["Company Name"].unique())

stock_df = stock_data[stock_data["Company Name"] == selected_comp_name]
selected_ticker=stock_df.iloc[0]["Ticker"]

min_date = datetime.date(2018, 1, 1)
max_date = datetime.date.today()

st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
col1,col2=st.columns(2)
with col1:
    start_date=str(st.date_input('Please insert start date',min_value=min_date,max_value=max_date))
with col2:
    end_date=str(st.date_input('Please insert end date',min_value=min_date,max_value=max_date))
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
input_data=psf.PySimFin().get_share_prices(selected_ticker,start_date,end_date)
latest_data=np.array([input_data],dtype=object)

model_AAPL=pickle.load(open('models/picklemodel_AAPL.pkl','rb'))
model_AMZN=pickle.load(open('models/picklemodel_AMZN.pkl','rb'))
model_GOOG=pickle.load(open('models/picklemodel_GOOG.pkl','rb'))
model_MSFT=pickle.load(open('models/picklemodel_MSFT.pkl','rb'))
model_TSLA=pickle.load(open('models/picklemodel_TSLA.pkl','rb'))

if selected_ticker=='AAPL':
    prediction=round(model_AAPL.predict(latest_data)[0],2)
elif selected_ticker=='AMZN':
    prediction=round(model_AMZN.predict(latest_data)[0],2)
elif selected_ticker=='GOOG':
    prediction=round(model_GOOG.predict(latest_data)[0],2)
elif selected_ticker=='MSFT':
    prediction=round(model_MSFT.predict(latest_data)[0],2)
elif selected_ticker=='TSLA':
    prediction=round(model_TSLA.predict(latest_data)[0],2)
else:
    raise InvalidTicker('Please insert a valid ticker.')

last_stock_df=stock_df[stock_df["Date"] <= pd.to_datetime(end_date)]
st.markdown("### 📊 Historical Stock Price Trend + Predicted Price")
fig = px.line(last_stock_df, x="Date", y="Close", title=f"{selected_comp_name}'s Stock Price Over Time")
fig.add_scatter(
    x=[end_date],
    y=[prediction],
    mode="markers",
    marker=dict(color="red", size=10, symbol="star"),
    name="Predicted Price"
)
st.plotly_chart(fig, use_container_width=True)

st.markdown(f"<p style='font-size:30px; text-align:left; font-weight:bold; '>Next day's stock price for {selected_comp_name}</p>", unsafe_allow_html=True)
col1,col2,col3=st.columns(3)
with col2:
    st.markdown(f"<p style='font-size:60px; text-align:left; font-weight:bold; '>{prediction} $</p>", unsafe_allow_html=True)