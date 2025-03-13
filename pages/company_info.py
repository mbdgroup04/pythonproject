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

    col1, col2 = st.columns(2)
    col1.metric("Total Companies Listed", total_companies)
    col2.metric("Avg. Employees per Company", f"{avg_employees:,.0f}")

    # Dropdown to select a company
    ticker = st.selectbox("Select a Company Ticker", companies["Ticker"].dropna().unique())
    company_info = companies[companies["Ticker"] == ticker]

    # Display company details
    if not company_info.empty:
        st.write(f"### {company_info.iloc[0]['Company Name']}")
        st.write(f"**Industry ID:** {company_info.iloc[0]['IndustryId']}")
        st.write(f"**Number of Employees:** {int(company_info.iloc[0]['Number Employees']) if not pd.isna(company_info.iloc[0]['Number Employees']) else 'N/A'}")
        st.write(f"**Market:** {company_info.iloc[0]['Market']}")
        st.write(f"**Currency:** {company_info.iloc[0]['Main Currency']}")
    else:
        st.warning("⚠️ No company data available.")

    # Sidebar Filters
    st.sidebar.markdown("### 🔍 Filter Companies")
    selected_ticker = st.sidebar.selectbox("Select a Company", ["All"] + list(companies["Company Name"].dropna().unique()))
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

    # Industry Distribution Chart
    st.markdown("### 🏢 Industry Distribution")

    # Convert IndustryId to string (prevents it from being treated as a number)
    filtered_companies = filtered_companies.copy()
    filtered_companies["IndustryId"] = filtered_companies["IndustryId"].astype(str)

    # Count the number of companies in each industry
    industry_counts = filtered_companies["IndustryId"].value_counts().reset_index()
    industry_counts.columns = ["Industry", "Company Count"]

    # Take the top 10 industries for better readability
    industry_counts = industry_counts.head(10).sort_values(by="Company Count", ascending=False)

    # Plot fixed bar chart
    fig = px.bar(
        industry_counts, 
        x="Industry", 
        y="Company Count", 
        title="Top Industries by Number of Companies",
        text="Company Count",  # Display company count on bars
        template="plotly_white"  # Use a cleaner layout
    )

    # Improve layout
    fig.update_traces(marker_color="blue", textposition="outside")
    fig.update_xaxes(title_text="Industry", tickangle=-45)  # Rotate labels for readability
    fig.update_yaxes(title_text="Company Count")

    # Show fixed chart
    st.plotly_chart(fig)

    # Top Companies by Employees
    st.markdown("### 🏆 Top Companies by Employee Count")
    top_companies = filtered_companies.nlargest(10, "Number Employees")[["Company Name", "Number Employees"]]
    st.dataframe(top_companies)
