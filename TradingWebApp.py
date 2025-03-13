import streamlit as st
import pandas as pd
import pages.Home as home  
import pages.company_info as company_info  # ✅ Import Company Info Page
import pages.Predictions as predictions  
import pages.Strategy as strategy  
import pages.Meet_the_Team as Meet_the_Team

# Load Data
def load_data():
    companies = pd.read_csv("companies.csv")  
    return companies

companies = load_data()  # ✅ Ensure 'companies' is defined

st.sidebar.markdown("Developed with ❤️ using Streamlit")
