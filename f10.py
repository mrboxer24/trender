import requests

from bs4 import BeautifulSoup

import time

import streamlit as st

#from playsound import playsound

# Constants

FINVIZ_URL = "https://finviz.com/screener.ashx?v=111&s=ta_unusualvolume&f=sh_price_5to50%2Cta_change_u&o=-volume"

CHECK_INTERVAL = 30  #300 5 minutes in seconds

HEADERS = {'User-Agent': 'Mozilla/5.0'}

# Initialize storage for previous tickers

previous_tickers = set()

new_tickers = set()

# Streamlit setup

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.title("🔴 Finviz Unusual Volume Stock Monitor")

st.markdown("<h2 style='text-align: center;'>Real-time Scrolling Ticker of Stocks with Unusual Volume</h2>",
            unsafe_allow_html=True)

ticker_container = st.empty()


def fetch_finviz_tickers():
    """Fetch stock tickers with unusual volume from Finviz."""

    response = requests.get(FINVIZ_URL, headers=HEADERS)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract stock tickers from the screener table

    tickers = set()

    # The ticker symbols are in a specific table class

    table = soup.find("table", class_="table-light")

    if table:

        rows = table.find_all("a", class_="screener-link-primary")

        for row in rows:
            tickers.add(row.text.strip())

    return tickers


def alert_user():
    """Play a sound alert when a new stock is added."""

    #playsound('alert.mp3')


def check_new_tickers():
    """Check and update new tickers, play sound alerts, and update Streamlit display."""

    global previous_tickers, new_tickers

    current_tickers = fetch_finviz_tickers()

    new_tickers = current_tickers - previous_tickers

    # Check for new tickers

    if new_tickers:

        for ticker in new_tickers:
            print(f"New stock detected: {ticker}")

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

            f"<marquee style='font-size:30px; color:red;'>{ticker_string}</marquee>",

            unsafe_allow_html=True

        )

        time.sleep(CHECK_INTERVAL)  # Refresh every 5 minutes


if __name__ == "__main__":
    display_tickers()