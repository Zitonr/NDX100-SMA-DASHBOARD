import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
from sma import final_return, final_return_stock


# Streamlit app
def main():
    st.title('Stock Trading Strategy Simulation')

    # User input for date range
    start_date = st.date_input('Enter the start date:',datetime(2009,1,1),datetime(2009,1,1),datetime(2019,1,1))
    end_date = st.date_input('Enter the end date:',datetime(2018,1,1),start_date,datetime(2019,1,1))

    # List available stocks
    directory = 'ndx100'
    stocks = [os.fsdecode(file)[:-4] for file in os.listdir(directory) if file.endswith('.csv')]
    stocks.insert(0, 'All')
    selected_stock = st.selectbox('Select a stock:', stocks)

    if st.button('Run Strategy'):
        st.write(f"Running strategy on {selected_stock} from {start_date} to {end_date}...")
        if selected_stock == 'All':
            final_return(start_date, end_date)
        else:
            # Convert date inputs to string format
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')
                final_return_stock(start_date_str, end_date_str, selected_stock)
            # st.pyplot(fig)
        



main()
