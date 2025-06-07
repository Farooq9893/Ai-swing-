import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Stock Dashboard", layout="wide")

# 📌 Number Formatter Function
def format_number(val):
    if val is None:
        return "N/A"
    elif isinstance(val, float) and 0 < abs(val) < 1:
        return f"{val * 100:.2f}%"
    elif isinstance(val, (int, float)):
        if abs(val) >= 1e7:
            return f"{val / 1e7:.2f} Cr"
        elif abs(val) >= 1e5:
            return f"{val / 1e5:.2f} Lac"
        else:
            return f"{val:.2f}"
    else:
        return str(val)

st.sidebar.title("📊 Dashboard Menu")
menu = st.sidebar.radio("Select Option", ["Dashboard", "Fundamental", "Balance Sheet", "Sector Rotation", "AI Chatbot"])

st.title("📈 Stock Analysis Dashboard")

# 📊 Market Overview
if menu == "Dashboard":
    st.subheader("📊 Market Overview")
    stock = st.text_input("Enter Stock Ticker (e.g., TCS.NS, INFY.NS)", "TCS.NS")
    data = yf.download(stock, period="6mo", interval="1d")
    st.line_chart(data['Close'])

# 🔍 Fundamental Analysis
elif menu == "Fundamental":
    st.subheader("🔍 Multi-Year Financial Data")
    ticker = st.text_input("Enter Stock Ticker", "TCS.NS")
    stock = yf.Ticker(ticker)
    fin = stock.financials.fillna(0).T
    fin.index = fin.index.strftime("%Y")
    fin = fin.applymap(format_number)
    st.markdown("### 📌 Annual Financial Metrics")
    st.dataframe(fin.T)

    st.markdown("### 📈 EPS (Quarter over Quarter)")
    q_earn = stock.quarterly_earnings
    if not q_earn.empty:
        q_earn.index = q_earn.index.strftime("%b %Y")
        q_earn['EPS'] = q_earn['Earnings Per Share'].apply(format_number)
        st.table(q_earn[['EPS']].T)
    else:
        st.warning("EPS quarterly data not available.")

# 📘 Balance Sheet
elif menu == "Balance Sheet":
    st.subheader("📘 Balance Sheet Viewer")
    ticker = st.text_input("Enter Stock Ticker for BS", "TCS.NS")
    bs = yf.Ticker(ticker).balance_sheet.fillna(0).T
    bs.index = bs.index.strftime("%Y")
    bs = bs.applymap(format_number)
    st.markdown("### Balance Sheet (₹ Cr Approx.)")
    st.dataframe(bs.T)

# 🔄 Sector Rotation
elif menu == "Sector Rotation":
    st.subheader("🔄 Sector Rotation Analysis")
    st.write("Coming soon: Sector heatmaps, momentum rotation, etc.")

# 🤖 AI Chatbot
elif menu == "AI Chatbot":
    st.subheader("🤖 Ask the AI Chatbot")
    st.write("Coming soon: Chatbot for stock Q&A based on your data")import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
from openai import OpenAI
import openai
import os

st.set_page_config(page_title="Stock Dashboard", layout="wide")

# 📌 Number Formatter Function
def format_number(val):
    if val is None:
        return "N/A"
    elif isinstance(val, float) and 0 < abs(val) < 1:
        return f"{val * 100:.2f}%"
    elif isinstance(val, (int, float)):
        if abs(val) >= 1e7:
            return f"{val / 1e7:.2f} Cr"
        elif abs(val) >= 1e5:
            return f"{val / 1e5:.2f} Lac"
        else:
            return f"{val:.2f}"
    else:
        return str(val)

st.sidebar.title("📊 Dashboard Menu")
menu = st.sidebar.radio("Select Option", ["Dashboard", "Fundamental", "Balance Sheet", "Sector Rotation", "AI Chatbot"])

st.title("📈 Stock Analysis Dashboard")

# 📊 Market Overview
if menu == "Dashboard":
    st.subheader("📊 Market Overview")
    stock = st.text_input("Enter Stock Ticker (e.g., TCS.NS, INFY.NS)", "TCS.NS")
    data = yf.download(stock, period="6mo", interval="1d")
    st.line_chart(data['Close'])

# 🔍 Fundamental Analysis
elif menu == "Fundamental":
    st.subheader("🔍 Multi-Year Financial Data")
    ticker = st.text_input("Enter Stock Ticker", "TCS.NS")
    stock = yf.Ticker(ticker)
    fin = stock.financials.fillna(0).T
    fin.index = fin.index.strftime("%Y")
    fin = fin.applymap(format_number)
    st.markdown("### 📌 Annual Financial Metrics")
    st.dataframe(fin.T)

    st.markdown("### 📈 EPS (Quarter over Quarter)")
    q_earn = stock.quarterly_earnings
    if not q_earn.empty:
        q_earn.index = q_earn.index.strftime("%b %Y")
        q_earn['EPS'] = q_earn['Earnings Per Share'].apply(format_number)
        st.table(q_earn[['EPS']].T)
    else:
        st.warning("EPS quarterly data not available.")

# 📘 Balance Sheet
elif menu == "Balance Sheet":
    st.subheader("📘 Balance Sheet Viewer")
    ticker = st.text_input("Enter Stock Ticker for BS", "TCS.NS")
    bs = yf.Ticker(ticker).balance_sheet.fillna(0).T
    bs.index = bs.index.strftime("%Y")
    bs = bs.applymap(format_number)
    st.markdown("### Balance Sheet (₹ Cr Approx.)")
    st.dataframe(bs.T)

# 🔄 Sector Rotation
elif menu == "Sector Rotation":
    st.subheader("🔄 Sector Rotation Heatmap")
    sectors = {
        "IT": ["TCS.NS", "INFY.NS", "WIPRO.NS"],
        "Banks": ["HDFCBANK.NS", "ICICIBANK.NS", "AXISBANK.NS"],
        "Pharma": ["SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS"],
        "FMCG": ["HINDUNILVR.NS", "ITC.NS", "DABUR.NS"]
    }

    performance = {}
    end = datetime.date.today()
    start = end - datetime.timedelta(days=30)

    for sector, stocks in sectors.items():
        returns = []
        for s in stocks:
            try:
                df = yf.download(s, start=start, end=end)
                if not df.empty:
                    pct = (df['Close'][-1] - df['Close'][0]) / df['Close'][0] * 100
                    returns.append(pct)
            except:
                continue
        if returns:
            performance[sector] = np.mean(returns)

    perf_df = pd.DataFrame(list(performance.items()), columns=["Sector", "30D Return (%)"])
    fig = px.imshow([perf_df["30D Return (%)"].tolist()], 
                    labels=dict(x=perf_df["Sector"].tolist(), y=["Return"], color="% Return"),
                    text_auto=True, color_continuous_scale='RdYlGn')
    st.plotly_chart(fig)

# 🤖 AI Chatbot
elif menu == "AI Chatbot":
    st.subheader("🤖 Ask the AI Chatbot")
    openai.api_key = st.secrets["openai_api_key"] if "openai_api_key" in st.secrets else os.getenv("OPENAI_API_KEY")
    user_input = st.text_input("Ask your stock question:")
    if user_input:
        with st.spinner("Generating response..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful financial assistant."},
                        {"role": "user", "content": user_input}
                    ]
                )
                st.markdown(f"**Answer:** {response['choices'][0]['message']['content']}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
