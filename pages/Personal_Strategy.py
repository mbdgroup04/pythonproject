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
st.markdown(f'<p style="font-size:40px; text-align:center; font-weight:bold; ">Personal Strategy</p>', unsafe_allow_html=True)
st.markdown(f"<p style='font-size:20px; text-align:left; '>Curious about market trends? - Try <b>TradeVision AI's</b> latest interactive prediction tool!</p>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size:20px; text-align:left; '>Input three hypothetical closing prices, and our model will forecast the next closing price - giving you a glimpse into possible market movements. Test your strategies and see how the market might react.</p>", unsafe_allow_html=True)
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
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
all_data=psf.PySimFin().get_dataframe(selected_ticker)

st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
st.markdown(f"<p style='font-size:20px; text-align:left; '>Last financial day's closing price for <b>{comp_name}</b> was ${real_data[-1]}</p>", unsafe_allow_html=True)
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:20px; text-align:left; ">Enter the first closing price for <b>{comp_name}</b> to start the prediction journey!</p>', unsafe_allow_html=True)
fict1=st.slider("",min_value=0.0,max_value=550.0,value=160.0,step=0.05,key='slider 1')
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:20px; text-align:left; ">Now, input the second closing price to build the trend!</p>', unsafe_allow_html=True)
fict2=st.slider("",min_value=0.0,max_value=550.0,value=160.0,step=0.05,key='slider 2')
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:20px; text-align:left; ">Lastly, add the third closing price and let the model forecast your next move!</p>', unsafe_allow_html=True)
fict3=st.slider("",min_value=0.0,max_value=550.0,value=160.0,step=0.05,key='slider 3')

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
    last_close1=real_data[-1]
    last_close2=input_data[-1]
    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:25px; text-align:left; '><b>Here's how your trend plays out!📈</b></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:22px; text-align:left; '>🔹You entered closing prices of ${fict1}, ${fict2}, and ${fict3} for the next three days, shaping our prediction model.</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:22px; text-align:left; '>🔹Based on your inputs, the forecasted closing price for the following day is ${prediction}.</p>", unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:25px; text-align:left; '><b>What this means for you:</b></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:25px; text-align:left; '>📊 Compared to your last input (${fict3}):</p>", unsafe_allow_html=True)
    if prediction>last_close2*1.0501:
        st.markdown(f"<p style='font-size:22px; text-align:left; '>The predicted price suggests a <b>BUY</b> move based on the trend you created.</p>", unsafe_allow_html=True)
    elif last_close2*0.9501<=prediction<=last_close2*1.0501:
        st.markdown(f"<p style='font-size:22px; text-align:left; '>The predicted price suggests a <b>HOLD</b> move based on the trend you created.</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='font-size:22px; text-align:left; '>The predicted price suggests a <b>SELL</b> move based on the trend you created.</p>", unsafe_allow_html=True)
    
    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:25px; text-align:left; '>💡Compared to today's actual closing price (${last_close1}):</p>", unsafe_allow_html=True)
    if prediction>last_close1*1.0501:
        st.markdown(f"<p style='font-size:22px; text-align:left; '>If your predicted market conditions will appear, this signals a <b>BUY</b> recommendation based on today's price.", unsafe_allow_html=True)
    elif last_close1*0.9501<=prediction<=last_close1*1.0501:
        st.markdown(f"<p style='font-size:22px; text-align:left; '>If your predicted market conditions will appear, this signals a <b>HOLD</b> recommendation based on today's price.</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='font-size:22px; text-align:left; '>If your predicted market conditions will appear, this signals a <b>SELL</b> recommendation based on today's price.</p>", unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:25px; text-align:left; '>Use these insights to test your strategy, refine your decisions, and see how well your predictions align with market movements!</p>", unsafe_allow_html=True)

st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:12px; text-align:left; ">(Please bear in mind, if an error pops up after clicking on predict, please wait a few seconds for the page to reload and click again. Sorry for the inconvenience.)</p>', unsafe_allow_html=True)

placeholder=st.empty()
time.sleep(3)
predict_clicked = placeholder.button("PREDICT")
if predict_clicked:
    price_predict()