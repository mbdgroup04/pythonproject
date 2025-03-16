# **Automated Daily Trading System**

## **Project Overview**

This project implements an **Automated Daily Trading System** that integrates **machine learning (ML)** for predicting stock market movements with a **Streamlit-based web application**. The system provides real-time stock analysis, forecasts price movements, and simulates trading strategies.

## **Project Features**

- **Machine Learning Model:** Predicts daily stock price movements.
- **Real-Time Stock Data Integration:** Fetches live data using the **SimFin API**.
- **Automated Trading Strategy:** Simulates buy/sell decisions based on ML predictions.
- **User-Friendly Web Application:** Interactive dashboard built with **Streamlit**.
- **Cloud Deployment:** Accessible without local installations.

## **Setup and Installation**

### **Requirements**

Ensure you have the following installed:

- Python 3.8+
- pip
- Virtual environment (optional but recommended)

### **Installation Steps**

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd pythonproject
   ```
2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application:**
   ```bash
   streamlit run Home.py
   ```

## **Usage Guide**

1. Open the **web application**.
2. Go to the Trading Recommendation tab.
3. Select a company from the provided list.
4. View real-time **market trends, ML predictions, and trading strategy results**.
5. Make decisions based on the prediction result.
6. Have a go at the fictional data simulation in the Personal Testing tab.

## **Project Structure**

```
.
├── Home.py                       # Main entry point for Streamlit web application
├── Trading_Recommendation.py     # Trading logic and simulation
├── PySimFin.py                   # API wrapper for SimFin data fetching
├── Model_Training.ipynb          # ML model training and evaluation
├── Exceptions.py                 # File for creation of the exceptions
├── Company_Information.py        # Page for the information of the company
├── Trading_Recommendation.py     # Page for the trading prediction and analysis
├── Personal_Testing.py           # Page for the personal testing with fictional data
├── Our_Team.py                   # Page with the team's basic information
├── api.env                       # File to hide the API Key
├── app.log                       # File with the saved logs
├── requirements.txt              # Dependencies
├── requirements.txt              # File to hide non-relevant data for the user
└── README.txt                    # Project documentation
```

## **Challenges & Future Improvements**

- **Challenges:**
  - Handling data imbalance.
  - Performance variability across stocks.
- **Future Enhancements:**
  - Expand stock selection.
  - Improve model accuracy with advanced ML techniques.
  - Enhance trading strategy with risk management techniques.

## **Contributors**

- SANTIAGO BOTERO
- NITIN JANGIR
- SANTIAGO RUIZ
- LEONARDO V. KIETZELL
- GIZELA THOMAS




