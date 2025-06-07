import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import openai
import os

st.set_page_config(page_title="Stock Dashboard", layout="wide")

# 📌 Number Formatter

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

# Sidebar
st.sidebar.title("📊 Dashboard Menu")
menu = st.sidebar.radio("Select Option", [
    "Dashboard", "Fundamental", "Balance Sheet", "Sector Rotation", "VCP Screener", "AI Chatbot"])

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
    st.markdown("### Balance Sheet (\u20B9 Cr Approx.)")
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

    time_option = st.selectbox("\ud83d\udcc5 Select Timeframe", ["1 Day", "7 Days", "30 Days"])
    chart_type = st.selectbox("\ud83d\udcca Select Chart Type", ["Bar Chart", "Treemap", "Line Chart (Beta)"])

    days_map = {"1 Day": 1, "7 Days": 7, "30 Days": 30}
    days = days_map[time_option]

    end = datetime.date.today()
    start = end - datetime.timedelta(days=days)

    performance = {}
    for sector, stocks in sectors.items():
        returns = []
        for s in stocks:
            try:
                df = yf.download(s, start=start, end=end, progress=False)
                if not df.empty:
                    pct = (df['Close'][-1] - df['Close'][0]) / df['Close'][0] * 100
                    returns.append(pct)
            except:
                continue
        if returns:
            performance[sector] = np.mean(returns)

    perf_df = pd.DataFrame(list(performance.items()), columns=["Sector", f"{days}D Return (%)"])
    perf_df.sort_values(by=f"{days}D Return (%)", ascending=False, inplace=True)

    if chart_type == "Bar Chart":
        fig = px.bar(perf_df, x=f"{days}D Return (%)", y="Sector", orientation='h',
                     color=f"{days}D Return (%)", color_continuous_scale='RdYlGn',
                     title=f"{days}-Day Sector Returns")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Treemap":
        fig = px.treemap(perf_df, path=["Sector"], values=f"{days}D Return (%)",
                         color=f"{days}D Return (%)", color_continuous_scale='RdYlGn',
                         title=f"{days}-Day Sector Treemap")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Line Chart (Beta)":
        st.info("Line chart needs date-wise returns. This is a placeholder.")
        st.dataframe(perf_df)

# 🧠 VCP Screener
elif menu == "VCP Screener":
    st.subheader("\ud83d\udccc Volatility Contraction Pattern (VCP) Screener")
    st.write("Coming soon: VCP breakout filtering with volume and consolidation patterns")

# 🧠 AI Chatbot
elif menu == "AI Chatbot":
    st.subheader("\ud83e\udde0 Ask the AI Chatbot")
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
