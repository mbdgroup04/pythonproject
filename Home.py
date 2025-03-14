import streamlit as st
import pandas as pd
import pages.Company_Information
import pages.Trading_Recommendation
import pages.Meet_the_Team

def load_data():
    companies = pd.read_csv("data/companies.csv")  
    return companies

companies = load_data()

def display_team_member(name, role, bio, fun_fact, image_path):
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(image_path, width=150)
    with col2:
        st.subheader(name)
        st.markdown(f"**Role:** {role}")
        st.write(bio)
        st.markdown(f"🎉 **Fun Fact:** {fun_fact}")



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


st.title("📈 Automated Daily Trading System")

st.markdown("## Overview")
st.markdown(
    """
    Welcome to the **Automated Daily Trading System**, a cutting-edge platform designed 
    to analyze stock market trends and generate predictive insights. This system integrates 
    financial data analytics and machine learning to provide real-time stock market 
    predictions and investment guidance.
    """
)

st.markdown("## System Purpose & Objectives")
st.markdown(
    """
    - **Market Forecasting**: Utilize historical stock data to predict future market trends.
    - **Investment Insights**: Support investors in making data-driven decisions.
    - **Real-time Monitoring**: Provide updated stock price information and company analytics.
    - **User-Friendly Interface**: Enable intuitive interaction with stock predictions and analytics.
    """
)
