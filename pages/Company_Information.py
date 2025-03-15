import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pages.functions.PySimFin as psf
import datetime

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
    "Company Information": None,
    "Trading Recommendation": "pages/Trading_Recommendation.py",
    "Personal Strategy": "pages/Personal_Strategy.py",
    "Our Team": "pages/Our_Team.py"
}

for page_name, file_path in PAGES.items():
    if file_path:
        st.sidebar.page_link(file_path, label=page_name)
    else:
        st.sidebar.write(f"### {page_name}")

def load_data():
    companies = pd.read_csv("data/companies.csv")  
    return companies

companies = load_data()

def display(companies):
    if companies.empty:
        st.error("⚠️ No company data available.")
        return
    df3=pd.read_csv("data/shareprices.csv")

    col1,col2,col3=st.columns(3)
    with col2:
        st.image("data/logo.jpg", width=200)
    st.markdown(f'<p style="font-size:40px; text-align:center; font-weight:bold; ">Company Information</p>', unsafe_allow_html=True)

    comp_name = st.selectbox("Please select a company:", ['Apple','Amazon','Google','Microsoft','Tesla'])
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

    company_info = companies[companies["Company Name"] == selected_comp_name]
    stock_df=df3[df3["Company Name"]==selected_comp_name]
    selected_ticker=stock_df.iloc[0]["Ticker"]
    real_data=psf.PySimFin().get_share_prices(selected_ticker,'2025-01-01',str(datetime.datetime.today().strftime('%Y-%m-%d')))
    year_list=['2018','2019','2020','2021','2022','2023','2024']
    selected_year=st.selectbox("Please select a fiscal year:",year_list)
    state_data=psf.PySimFin().get_financial_statements(selected_ticker,selected_year)
    if state_data[1]!=0:
        revenue=f"${state_data[1]//1000000:,}"
    else:
        revenue="NaN"
    if state_data[2]!=0:
        gross_profit=f"${state_data[2]//1000000:,}"
    else:
        gross_profit="NaN"

    if not company_info.empty:
        st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size:36px; text-align:center; font-weight:bold; ">{comp_name}</p>', unsafe_allow_html=True)
        cola,colb=st.columns(2)
        with cola:
            st.markdown(f'<p style="font-size:16px; text-align:center; font-weight:bold; ">Market: {company_info.iloc[0]['Market']}</p>', unsafe_allow_html=True)
        with colb:
            st.markdown(f'<p style="font-size:16px; text-align:center; font-weight:bold; ">Currency: {company_info.iloc[0]['Main Currency']}</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
        colc,cold,cole,colf=st.columns(4)
        colc.metric(f"**Number of Employees**", f"{int(company_info.iloc[0]['Number Employees']) if not pd.isna(company_info.iloc[0]['Number Employees']) else 'N/A':,}")    
        cold.metric(f"**Fical Year selected**", f"{selected_year}")
        cole.metric(f"**Revenue (in millions)**", f"{revenue}")
        colf.metric(f"**Gross Profit (in millions)**", f"{gross_profit}")
    else:
        st.warning("⚠️ No company data available.")

    latest_data = real_data[-1]

    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:25px; text-align:left; font-weight:bold; '>Today's Price:</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:26px; text-align:left; '>${latest_data['Close']:.2f}</p>", unsafe_allow_html=True)
    
    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:25px; text-align:left; font-weight:bold; '>{selected_comp_name}'s metrics in average:</p>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📈 Open", f"${latest_data['Open']:.2f}")
    col2.metric("📉 Low", f"${latest_data['Low']:.2f}")
    col3.metric("📊 High", f"${latest_data['High']:.2f}")
    col4.metric("🔄 Volume", f"{latest_data['Volume']:,}")

    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:25px; text-align:left; font-weight:bold; '>📊 Candlestick Chart</p>", unsafe_allow_html=True)
    fig_candle = go.Figure(data=[
        go.Candlestick(
            x=stock_df["Date"],
            open=stock_df["Open"],
            high=stock_df["High"],
            low=stock_df["Low"],
            close=stock_df["Close"],
            name=selected_comp_name
        )
    ])
    fig_candle.update_layout(title=f"{selected_comp_name}", template="plotly_dark",xaxis_title="Date",yaxis_title="Close")
    st.plotly_chart(fig_candle, use_container_width=True)

    st.markdown(f"<p style='font-size:25px; text-align:left; font-weight:bold; '>📊 Stock Comparison</p>", unsafe_allow_html=True)
    comps_selected = st.multiselect("Please select multiple companies:", df3["Company Name"].unique(), default=[selected_comp_name])
    
    if comps_selected:
        compare_df = df3[df3["Company Name"].isin(comps_selected)]
        fig_compare = px.line(compare_df, x="Date", y="Close", color="Ticker", title="Stock Comparison")
        st.plotly_chart(fig_compare, use_container_width=True)

display(pd.read_csv("data/companies.csv"))
