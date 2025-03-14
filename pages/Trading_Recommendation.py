import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
    "Trading Recommendation": None,
    "Personal Testing": "pages/Personal_Testing.py",
    "Our Team": "pages/Our_Team.py"
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
st.markdown(f'<p style="font-size:40px; text-align:center; font-weight:bold; ">Trading Recommendation</p>', unsafe_allow_html=True)

st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; ">Select a company to predict the closing price for tomorrow:</p>', unsafe_allow_html=True)
comp_name = st.selectbox("", ['Apple','Amazon','Google','Microsoft','Tesla'])
if comp_name=='Apple':
    selected_comp_name='APPLE INC'
elif comp_name=='Amazon':
    selected_comp_name='AMAZON COM INC'
elif comp_name=='Google':
    selected_comp_name='Alphabet (Google)'
elif comp_name=='Microsoft':
    selected_comp_name='MICROSOFT CORP'
else:
    selected_comp_name='Tesla'

stock_df = stock_data[stock_data["Company Name"] == selected_comp_name]
selected_ticker=stock_df.iloc[0]["Ticker"]

real_data=psf.PySimFin().get_dataframe(selected_ticker)
fig = px.line(stock_df, x="Date", y="Close", title="")

start_date='2018-03-06'
end_date=datetime.datetime.today().strftime('%Y-%m-%d')

input_data=psf.PySimFin().get_share_prices(selected_ticker,start_date,end_date)
latest_data=np.array([input_data],dtype=object)

model_AAPL=pickle.load(open('models/picklemodel_AAPL.pkl','rb'))
model_AMZN=pickle.load(open('models/picklemodel_AMZN.pkl','rb'))
model_GOOG=pickle.load(open('models/picklemodel_GOOG.pkl','rb'))
model_MSFT=pickle.load(open('models/picklemodel_MSFT.pkl','rb'))
model_TSLA=pickle.load(open('models/picklemodel_TSLA.pkl','rb'))

if input_data!=[0,0,0]:
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
else:
    prediction=0

def price_predict():
    last_close=input_data[-1]
    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:25px; text-align:left; '><b>Today's predicted closing price for {comp_name} is:</b> ${prediction}</p>", unsafe_allow_html=True)
    if prediction>last_close*1.101:
        st.markdown(f"<p style='font-size:22px; text-align:left; '>Your dearest companion TradeVision AI advices you to <b>BUY</b>, since today's closing price is predicted to be more than 10% higher than yesterday's (${last_close})</p>", unsafe_allow_html=True)
    elif last_close*0.9501<=prediction<=last_close*1.101:
        st.markdown(f"<p style='font-size:22px; text-align:left; '>Your dearest companion TradeVision AI advices you to <b>HOLD</b>, since today's closing price is predicted to be around the same value as yesterday's (${last_close})</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='font-size:22px; text-align:left; '>Your dearest companion TradeVision AI advices you to <b>SELL</b>, since today's closing price is predicted to be more than 5% lower yesterday's (${last_close})</p>", unsafe_allow_html=True)

if st.button("PREDICT"):
    price_predict()
    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    st.markdown(f"### 📊 Historical + Predicted Closing Price for {comp_name}")
    fig.add_trace(go.Scatter(x=real_data["Date"],y=real_data["Close"],mode="lines",name="Real-Time API Data",line=dict(color="magenta")))
    fig.add_scatter(x=[end_date],y=[prediction],mode="markers",marker=dict(color="red", size=10, symbol="star"),name="Predicted Price")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    st.markdown(f"### 📊 Historical Closing Prices for {comp_name}")
    st.plotly_chart(fig, use_container_width=True)