import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pages.functions.PySimFin as psf
from pages.functions.Exceptions import InvalidTicker
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
    "Company Information": "pages/Company_Information.py",
    "Trading Recommendation": "pages/Trading_Recommendation.py",
    "Meet The Team": "pages/Meet_the_Team.py",
}

for page_name, file_path in PAGES.items():
    if file_path:
        st.sidebar.page_link(file_path, label=page_name)
    else:
        st.sidebar.write(f"### {page_name}")

def display(companies):
    if companies.empty:
        st.error("⚠️ No company data available.")
        return
    df3=pd.read_csv("data/shareprices.csv")

    selected_comp_name = st.selectbox("Please select a company:", companies["Company Name"].unique())
    company_info = companies[companies["Company Name"] == selected_comp_name]
    stock_df=df3[df3["Company Name"]==selected_comp_name]
    selected_ticker=stock_df.iloc[0]["Ticker"]
    year_list=['2018','2019','2020','2021','2022','2023','2024']
    selected_year=st.selectbox("Please select a fiscal year:",year_list)
    state_data=psf.PySimFin().get_financial_statements(selected_ticker,selected_year)

    if not company_info.empty:
        st.write(f"### {selected_comp_name}")
        st.write(f"**Number of Employees:** {int(company_info.iloc[0]['Number Employees']) if not pd.isna(company_info.iloc[0]['Number Employees']) else 'N/A':,}".replace(",","."))
        st.write(f"**Market:** {company_info.iloc[0]['Market']}")
        st.write(f"**Currency:** {company_info.iloc[0]['Main Currency']}")
        st.write(f"**Fical Year selected:** {state_data[0]}")
        st.write(f"**Revenue:** {state_data[1]}")
        st.write(f"**Gross Profit:** {state_data[2]}")
    else:
        st.warning("⚠️ No company data available.")

    latest_data = stock_df.iloc[-1]

    if 'Change' in stock_df.columns:
        change_value = f"{latest_data['Change']}%"
    else:
        if len(stock_df) > 1:
            change_value = f"{((latest_data['Close'] - stock_df.iloc[-2]['Close']) / stock_df.iloc[-2]['Close'] * 100):.2f}%"
        else:
            change_value = "N/A"

    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; ">Current Price:</p>', unsafe_allow_html=True)
    st.metric(label="", value=f"${latest_data['Close']:.2f}", delta=change_value)
    
    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:20px; text-align:left; font-weight:bold; '>{selected_comp_name}'s metrics in average:</p>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📈 Open", f"${latest_data['Open']:.2f}")
    col2.metric("📉 Low", f"${latest_data['Low']:.2f}")
    col3.metric("📊 High", f"${latest_data['High']:.2f}")
    col4.metric("🔄 Volume", f"{latest_data['Volume']:,}")

    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    st.markdown("### 📊 Candlestick Chart")
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

    st.markdown("### 📊 Compare Stocks")
    comps_selected = st.multiselect("Please select multiple companies:", df3["Company Name"].unique(), default=[selected_comp_name])
    
    if comps_selected:
        compare_df = df3[df3["Company Name"].isin(comps_selected)]
        fig_compare = px.line(compare_df, x="Date", y="Close", color="Ticker", title="Stock Comparison")
        st.plotly_chart(fig_compare, use_container_width=True)

display(pd.read_csv("data/companies.csv"))
