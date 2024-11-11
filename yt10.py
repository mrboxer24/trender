
import requests

from bs4 import BeautifulSoup

import time

import streamlit as st

from playsound import playsound


# Constants

YAHOO_URL = "https://finance.yahoo.com/markets/stocks/trending/"

CHECK_INTERVAL = 300  # 5 minutes in seconds


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

    response = requests.get(YAHOO_URL)

    soup = BeautifulSoup(response.text, 'html.parser')



    # Extract stock tickers

    tickers = set()

    for symbol in soup.select('a.Fw(600)'):

        tickers.add(symbol.text.strip())



    return tickers


def alert_user():

    """Play a sound alert when a new stock is added."""

    playsound('alert.mp3')


def check_new_tickers():

    """Check and update new tickers, play sound alerts, and update Streamlit display."""

    global previous_tickers, new_tickers


    current_tickers = fetch_trending_stocks()

    new_tickers = current_tickers - previous_tickers


    # Check for new tickers

    if new_tickers:

        for ticker in new_tickers:

            print(f"New stock added: {ticker}")

            alert_user()  # Play sound alert


        # Update previous tickers for the next check

        previous_tickers.update(new_tickers)


# Streamlit Ticker Display

def display_tickers():

    while True:

        check_new_tickers()

        # Display scrolling style tickers

        ticker_string = " | ".join(new_tickers)

        ticker_container.markdown(

            f"<marquee style='font-size:30px; color:green;'>{ticker_string}</marquee>",

            unsafe_allow_html=True

        )

        time.sleep(CHECK_INTERVAL)  # Refresh every 5 minutes


if __name__ == "__main__":

    display_tickers()