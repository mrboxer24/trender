
import requests

from bs4 import BeautifulSoup

import time
import pandas as pd
import json

import streamlit as st
import winsound

import pyttsx3
from io import StringIO




def alert_user(symbol):
    """Play a beep sound alert and read the stock symbol out loud."""
    # Play a beep sound
    frequency = 1000  # Hertz
    duration = 500  # Milliseconds
    winsound.Beep(frequency, duration)

    # Initialize text-to-speech engine
    engine = pyttsx3.init()
    engine.say(f"New stock added: {symbol}")
    engine.runAndWait()


# Constants

YAHOO_URL = "https://finance.yahoo.com/markets/stocks/trending/"

CHECK_INTERVAL = 60  # 5 minutes in seconds


# Initialize storage for previous tickers

previous_tickers = set()

new_tickers = set()


# Streamlit setup

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
st.title("🟢 Yahoo Finance Trending Stocks")
st.markdown("<h2 style='text-align: center;'>Real-time Scrolling Stock Ticker</h2>", unsafe_allow_html=True)
ticker_container = st.empty()


def fetch_trending_stocks():

    """Fetch trending stock symbols from Yahoo Finance."""
    r = requests.get(YAHOO_URL)
    # print(r.content)
    soup = BeautifulSoup(r.content, 'lxml')
    table = soup.find_all('table')[0]
    # Wrap the HTML content in StringIO
    html_content = StringIO(str(table))
    df = pd.read_html(html_content)

    #print(df[0].to_json(orient='records'))
    jdata = json.loads(df[0].to_json(orient='records'))

    response = requests.get(YAHOO_URL)

    soup = BeautifulSoup(response.text, 'html.parser')



    # Extract stock tickers

    tickers = set()
    for s in jdata:
        tickers.add(s["Symbol"])

    return tickers



def check_new_tickers():

    """Check and update new tickers, play sound alerts, and update Streamlit display."""

    global previous_tickers, new_tickers


    current_tickers = fetch_trending_stocks()

    new_tickers = current_tickers - previous_tickers


    # Check for new tickers

    if new_tickers:

        for ticker in new_tickers:

            print(f"New stock added: {ticker}")

            alert_user(ticker)  # Play sound alert


        # Update previous tickers for the next check

        previous_tickers.update(new_tickers)


# Streamlit Ticker Display

def display_tickers():

    while True:

        check_new_tickers()

        # Display scrolling style tickers

        ticker_string = " | ".join(new_tickers)

        ticker_container.markdown(

            f"<marquee style='font-size:80px; color:green;'>{ticker_string}</marquee>",

            unsafe_allow_html=True

        )

        time.sleep(CHECK_INTERVAL)  # Refresh every 5 minutes


if __name__ == "__main__":

    display_tickers()