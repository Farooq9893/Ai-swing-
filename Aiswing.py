import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Stock Dashboard", layout="wide")

# 📌 Number Formatter Function
def format_number(val):
    if val is None:
        return "N/A"
    elif isinstance(val, float) and 0 < val < 1:
        return f"{val * 100:.2f}%"
    elif isinstance(val, (int, float)):
        if val >= 1e7:
            return f"{val / 1e7:.2f} Cr"
        elif val >= 1e5:
            return f"{val / 1e5:.2f} Lac"
        else:
            return f"{val:.2f}"
    else:
        return str(val)

st.sidebar.title("📊 Dashboard Menu")
menu = st.sidebar.radio("Select Option", ["Dashboard", "Fundamental", "Balance Sheet", "Sector Rotation", "Study Material", "AI Chatbot"])

st.title("📈 Stock Analysis Dashboard")

# 📊 Market Overview
if menu == "Dashboard":
    st.subheader("📊 Market Overview")
    stock = st.text_input("Enter Stock Ticker (e.g., TCS.NS, INFY.NS)", "TCS.NS")
    data = yf.download(stock, period="6mo", interval="1d")
    st.line_chart(data['Close'])

# 🔍 Fundamental Analysis
elif menu == "Fundamental":
    st.subheader("🔍 Fundamental Analysis")
    ticker = st.text_input("Enter Stock Ticker for FA", "TCS.NS")
    info = yf.Ticker(ticker).info

    fundamentals = {
        "Name": info.get("shortName", "N/A"),
        "Sector": info.get("sector", "N/A"),
        "Market Cap": info.get("marketCap", "N/A"),
        "PE Ratio": info.get("trailingPE", "N/A"),
        "EPS": info.get("trailingEps", "N/A"),
        "Book Value": info.get("bookValue", "N/A"),
        "52 Week High": info.get("fiftyTwoWeekHigh", "N/A"),
        "52 Week Low": info.get("fiftyTwoWeekLow", "N/A"),
        "Return on Equity": info.get("returnOnEquity", "N/A"),
        "Dividend Yield": info.get("dividendYield", "N/A")
    }

    formatted_fundamentals = {k: format_number(v) for k, v in fundamentals.items()}
    st.markdown("### 📊 Key Fundamentals")
    st.table(pd.DataFrame.from_dict(formatted_fundamentals, orient="index", columns=["Value"]))

# 📘 Balance Sheet
elif menu == "Balance Sheet":
    st.subheader("📘 Balance Sheet Viewer")
    ticker = st.text_input("Enter Stock Ticker for BS", "TCS.NS")
    bs = yf.Ticker(ticker).balance_sheet
    st.markdown("### Balance Sheet (₹ Crore Approx.)")
    st.dataframe(bs.T)  # Transpose to show columns as years

# 🔄 Sector Rotation
elif menu == "Sector Rotation":
    st.subheader("🔄 Sector Rotation Analysis")
    st.write("Coming soon: Sector heatmaps, momentum rotation, etc.")

# 📚 Study Material
elif menu == "Study Material":
    st.subheader("📚 Study Material & Videos")
    st.write("Telegram Group: [@Farooq898233](https://t.me/Farooq898233)")

# 🤖 AI Chatbot
elif menu == "AI Chatbot":
    st.subheader("🤖 Ask the AI Chatbot")
    st.write("Coming soon: Chatbot for stock Q&A based on your data")
