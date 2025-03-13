import streamlit as st
import pandas as pd
import plotly.express as px

def display(companies):  # ✅ Accept 'companies' as an argument
    if companies.empty:
        st.error("⚠️ No company data available.")
        return

    # KPIs
    total_companies = companies.shape[0]
    avg_employees = companies["Number Employees"].mean()
    top_industries = companies["IndustryId"].value_counts().head(5)

    # Dropdown to select a company
    selected_ticker = st.selectbox("Select a Company Ticker", companies["Ticker"].dropna().unique())
    company_info = companies[companies["Ticker"] == selected_ticker]

    # Display company details
    if not company_info.empty:
        st.write(f"### {company_info.iloc[0]['Company Name']}")
        st.write(f"**Industry ID:** {company_info.iloc[0]['IndustryId']}")
        st.write(f"**Number of Employees:** {int(company_info.iloc[0]['Number Employees']) if not pd.isna(company_info.iloc[0]['Number Employees']) else 'N/A':,}".replace(",","."))
        st.write(f"**Market:** {company_info.iloc[0]['Market']}")
        st.write(f"**Currency:** {company_info.iloc[0]['Main Currency']}")
    else:
        st.warning("⚠️ No company data available.")

    # Sidebar Filters
    selected_year = st.sidebar.selectbox("Filter by Financial Year-End", ["All"] + sorted(companies["End of financial year (month)"].dropna().astype(str).unique()))
    selected_size = st.sidebar.slider("Filter by Number of Employees", 
                                        min_value=0, 
                                        max_value=int(companies["Number Employees"].fillna(0).max()), 
                                        value=(0, int(companies["Number Employees"].fillna(0).max())))

    # Apply Filters
    filtered_companies = companies.copy()
    if selected_ticker != "All":
        filtered_companies = filtered_companies[filtered_companies["Company Name"] == selected_ticker]
    if selected_year != "All":
        filtered_companies = filtered_companies[filtered_companies["End of financial year (month)"] == selected_year]
    filtered_companies = filtered_companies[
        (filtered_companies["Number Employees"] >= selected_size[0]) & 
        (filtered_companies["Number Employees"] <= selected_size[1])
    ]

    latest_data = company_info.iloc[-1]

    # Handle Missing 'Change' Column
    if 'Change' in company_info.columns:
        change_value = f"{latest_data['Change']}%"
    else:
        if len(company_info) > 1:
            change_value = f"{((latest_data['Close'] - company_info.iloc[-2]['Close']) / company_info.iloc[-2]['Close'] * 100):.2f}%"
        else:
            change_value = "N/A"

    # Display Stock Metrics
    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    st.metric(label="Current Price", value=f"${latest_data['Close']:.2f}", delta=change_value)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📈 Open", f"${latest_data['Open']:.2f}")
    col2.metric("📉 Low", f"${latest_data['Low']:.2f}")
    col3.metric("📊 High", f"${latest_data['High']:.2f}")
    col4.metric("🔄 Volume", f"{latest_data['Volume']:,}")

    st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
    st.markdown("### 📊 Candlestick Chart")
    fig_candle = go.Figure(data=[
        go.Candlestick(
            x=company_info["Date"],
            open=company_info["Open"],
            high=company_info["High"],
            low=company_info["Low"],
            close=company_info["Close"],
            name=selected_ticker
        )
    ])
    fig_candle.update_layout(title=f"{selected_ticker}", template="plotly_dark",xaxis_title="Date",yaxis_title="Close")
    st.plotly_chart(fig_candle, use_container_width=True)

    st.markdown("### 📊 Compare Stocks")
    tickers_selected = st.multiselect("Select multiple stocks:", companies["Company Name"].unique(), default=[selected_ticker])
    
    if tickers_selected:
        compare_df = companies[companies["Company Name"].isin(tickers_selected)]
        fig_compare = px.line(compare_df, x="Date", y="Close", color="Ticker", title="Stock Comparison")
        st.plotly_chart(fig_compare, use_container_width=True)

display(pd.read_csv("companies.csv"))