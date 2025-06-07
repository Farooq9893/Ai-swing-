import streamlit as st
import yfinance as yf
import pandas as pd
 st.set_page_config(page_title="Stock Dashboard", layout="wide")
 
 st.sidebar.title("📊 Dashboard Menu")
 menu = st.sidebar.radio("Select Option", ["Dashboard", "Fundamental", "Balance Sheet", "Sector Rotation", "Study Material", "AI Chatbot"])
 
 st.title("📈 Stock Analysis Dashboard")
 
 if menu == "Dashboard":
     st.subheader("📊 Market Overview")
         stock = st.text_input("Enter Stock Ticker (e.g., TCS.NS, INFY.NS)", "TCS.NS")
             data = yf.download(stock, period="6mo", interval="1d")
                                                                         st.write("Coming soon: Chatbot for stock Q&A based on your data")
 
                 elif menu == "Fundamental":
                     st.subheader("🔍 Fundamental Analysis")
                         ticker = st.text_input("Enter Stock Ticker for FA", "TCS.NS")
                             info = yf.Ticker(ticker).info
                                 st.json(info)
 
                                 elif menu == "Balance Sheet":
                                     st.subheader("📘 Balance Sheet Viewer")
                                         ticker = st.text_input("Enter Stock Ticker for BS", "TCS.NS")
                                             bs = yf.Ticker(ticker).balance_sheet
                                                 st.write(bs)
 
                                                 elif menu == "Sector Rotation":
                                                     st.subheader("🔄 Sector Rotation Analysis")
                                                         st.write("Coming soon: Sector heatmaps, momentum rotation, etc.")
 
                                                         elif menu == "Study Material":
                                                             st.subheader("📚 Study Material & Videos")
                                                                 st.write("Telegram Group: [@Farooq898233](https://t.me/Farooq898233)")
 
                                                                 elif menu == "AI Chatbot":
                                                                     st.subheader("🤖 Ask the AI Chatbot")
                                                                         st.write("Coming soon: Chatbot for stock Q&A based on your data")                                                                        st.write("Coming soon: Chatbot for stock Q&A based on your data")
