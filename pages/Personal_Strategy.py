import streamlit as st
import pandas as pd
import datetime
import pickle
import numpy as np
import pages.functions.PySimFin as psf
from pages.functions.Exceptions import InvalidTicker
import time

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
    "Personal Strategy": None,
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
st.markdown(f'<p style="font-size:40px; text-align:center; font-weight:bold; ">Personal Testing</p>', unsafe_allow_html=True)
st.markdown(f"<p style='font-size:20px; text-align:left; '>Curious about market trends? - Try <b>TradeVision AI's</b> latest interactive prediction tool!🔮.</p>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size:20px; text-align:left; '>Input 3 hypothetical closing prices, and our model will forecast the next closing price - giving you a glimpse into possible market movements. Test your strategies and see how the market might react.</p>", unsafe_allow_html=True)
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; ">Select a company to predict the closing price for today ({datetime.datetime.today().strftime('%Y-%m-%d')}):</p>', unsafe_allow_html=True)

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
real_data=psf.PySimFin().get_share_prices(selected_ticker,'2025-01-01',str(datetime.datetime.today().strftime('%Y-%m-%d')))

max_fict=stock_df['Close'].max()
mid_fict=round(max_fict/2,2)
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
st.markdown(f"<p style='font-size:20px; text-align:left; '>Last financial day's closing price for <b>{comp_name}</b> is ${real_data[-1]}</p>", unsafe_allow_html=True)
st.markdown(f'<p style="font-size:20px; text-align:left; ">Enter the first closing price for <b>{comp_name}</b> to start the prediction journey!</p>', unsafe_allow_html=True)
fict1=st.slider("",min_value=0.0,max_value=max_fict,value=mid_fict,step=0.05,key='slider 1')
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:20px; text-align:left; ">Now, input the second closing price to build the trend!</p>', unsafe_allow_html=True)
fict2=st.slider("",min_value=0.0,max_value=max_fict,value=mid_fict,step=0.05,key='slider 2')
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:20px; text-align:left; ">Lastly, add the third closing price and let the model forecast your next move!</p>', unsafe_allow_html=True)
fict3=st.slider("",min_value=0.0,max_value=max_fict,value=mid_fict,step=0.05,key='slider 3')

start_date='2018-03-06'
end_date=datetime.datetime.today().strftime('%Y-%m-%d')

input_data=[fict1,fict2,fict3]
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

def price_predict():
    last_close=input_data[-1]
    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:25px; text-align:left; '><b>Today's predicted closing price for {comp_name} is:</b> ${prediction}</p>", unsafe_allow_html=True)
    if prediction>last_close*1.0501:
        st.markdown(f"<p style='font-size:22px; text-align:left; '>In this fictional case, TradeVision AI would advice you to <b>BUY</b>, since today's closing price is predicted to be more than 10% higher than yesterday's</p>", unsafe_allow_html=True)
    elif last_close*0.9501<=prediction<=last_close*1.0501:
        st.markdown(f"<p style='font-size:22px; text-align:left; '>In this fictional case, TradeVision AI would advice you to <b>HOLD</b>, since today's closing price is predicted to be around the same value as yesterday's</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='font-size:22px; text-align:left; '>In this fictional case, TradeVision AI would advice you to <b>SELL</b>, since today's closing price is predicted to be more than 5% lower yesterday's</p>", unsafe_allow_html=True)

st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
placeholder=st.empty()
time.sleep(3)
with placeholder:
    if st.button("PREDICT"):
        price_predict()