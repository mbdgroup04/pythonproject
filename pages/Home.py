import streamlit as st
import pandas as pd

# Function to display team member profiles
def display_team_member(name, role, bio, fun_fact, image_path):
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(image_path, width=150)
    with col2:
        st.subheader(name)
        st.markdown(f"**Role:** {role}")
        st.write(bio)
        st.markdown(f"🎉 **Fun Fact:** {fun_fact}")

# Main function to display the Home page

st.title("📈 Automated Daily Trading System")

# System Overview
st.markdown("## Overview")
st.markdown(
    """
    Welcome to the **Automated Daily Trading System**, a cutting-edge platform designed 
    to analyze stock market trends and generate predictive insights. This system integrates 
    financial data analytics and machine learning to provide real-time stock market 
    predictions and investment guidance.
    """
)

# System Purpose and Objectives
st.markdown("## System Purpose & Objectives")
st.markdown(
    """
    - **Market Forecasting**: Utilize historical stock data to predict future market trends.
    - **Investment Insights**: Support investors in making data-driven decisions.
    - **Real-time Monitoring**: Provide updated stock price information and company analytics.
    - **User-Friendly Interface**: Enable intuitive interaction with stock predictions and analytics.
    """
)


