import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import streamlit as st

def final_return_stock(start_date,end_date, selected_stock):
# Set your initial budget

    directory = os.fsencode('ndx100')

    # Initialize variables for tracking shares bought and sold
    money_gained = 0
    money_spent = 0
    final_money_spent = 0
    final_money_gained = 0
    final_money = 0
    budget = []
    money_sequence = []
    # Create the "Graphs" directory if it doesn't exist
    if not os.path.exists("Graphs"):
        os.makedirs("Graphs")

    file = selected_stock + '.csv'
    print(f"Transactions for {file}")
    # Read the CSV file
    df = pd.read_csv('ndx100/' + os.fsdecode(file))

    # Calculate 50-day SMA
    df['Short_SMA'] = df['CLOSE'].rolling(window=50).mean()

    # Calculate 200-day SMA
    df['Long_SMA'] = df['CLOSE'].rolling(window=200).mean()

    # Convert 'DATE' column to datetime format
    df['DATE'] = pd.to_datetime(df['DATE'])

    # Filter dataframe based on user input date range
    # df = df[(df['DATE'] >= start_date) & (df['DATE'] <= end_date)]
    df = df.query('DATE >= @start_date and DATE <= @end_date').reset_index()


    # Find intersections
    df['Signal'] = 0  # Initialize a column to mark intersections
    position = 0
    for i in range(1, len(df)):
        try:
            if df.at[i, 'Short_SMA'] > df.at[i, 'Long_SMA'] and df.at[i - 1, 'Short_SMA'] <= df.at[i - 1, 'Long_SMA']:
                # Check if budget allows buying
                df.at[i, 'Signal'] = 1  # Upward crossover
                st.write(f"BUY at {df.at[i, 'DATE']}")
                money_spent += df.at[i, 'CLOSE']
                position += 1

            elif df.at[i, 'Short_SMA'] < df.at[i, 'Long_SMA'] and df.at[i - 1, 'Short_SMA'] >= df.at[i - 1, 'Long_SMA']:
                if (position > 0):
                    df.at[i, 'Signal'] = -1  # Downward crossover
                    st.write(f"SELL at {df.at[i, 'DATE']}")
                    money_gained += df.at[i, 'CLOSE']
                    position -= 1
            budget.append(money_gained - money_spent)
            total_money = position * df.at[i, 'CLOSE'] + money_gained - money_spent
            money_sequence.append(total_money)
        except KeyError as e:
            st.write(e)
            continue
    try:
        money_gained += position*df['CLOSE'].iloc[-1]
        final_money_gained += money_gained
        final_money_spent += money_spent
        money_gained, money_spent = 0,0

    except:
        pass

    max_borrowing = min(budget) * -1
    final_money = money_sequence[-1]
    final_return = (final_money - max_borrowing)/max_borrowing

    fig, ax = plt.subplots(figsize=(15, 6))
    ax.plot(df['DATE'], df['Short_SMA'], label='50-day SMA', linestyle='--', color='blue')
    ax.plot(df['DATE'], df['Long_SMA'], label='200-day SMA', linestyle='--', color='green')
    ax.plot(df['DATE'], df['CLOSE'], label='Closing price', linestyle='-', color='black', linewidth=1)
    ax.fill_between(df['DATE'], df['Short_SMA'], df['Long_SMA'], where=df['Short_SMA'] >= df['Long_SMA'],
                    facecolor='green', interpolate=True, alpha=0.3)
    ax.fill_between(df['DATE'], df['Short_SMA'], df['Long_SMA'], where=df['Short_SMA'] < df['Long_SMA'],
                    facecolor='red', interpolate=True, alpha=0.3)
    upward_crossings = df[df['Signal'] == 1]
    downward_crossings = df[df['Signal'] == -1]
    ax.scatter(upward_crossings['DATE'], upward_crossings['Short_SMA'], marker='^', color='green',
               label='Upward crossover')
    ax.scatter(downward_crossings['DATE'], downward_crossings['Short_SMA'], marker='v', color='red',
               label='Downward crossover')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.set_title(f"{os.path.splitext(selected_stock)[0]} Stock prices")
    ax.legend()

    
    fig2, ax2 = plt.subplots(figsize=(15, 6))
    ax2.plot(df['DATE'][1:],money_sequence, label='Money sequence', linestyle='-', color='black', linewidth=3)
    ax2.set_xlabel('Date')
    ax2.set_title('Cash on hand evolution')
    ax2.set_ylabel('Money')

    st.pyplot(fig)
    st.pyplot(fig2)
    st.write(f'Return from {start_date} to {end_date} is {final_return*100:.2f}%')
    

def final_return(start_date,end_date):
# Set your initial budget

    directory = os.fsencode('ndx100')

    # Initialize variables for tracking shares bought and sold
    money_gained = 0
    money_spent = 0
    final_money_spent = 0
    final_money_gained = 0
    final_budget = []
    final_money = []
    money_sequences = []
    budget_sequences = []
    
    # Create the "Graphs" directory if it doesn't exist
    if not os.path.exists("Graphs"):
        os.makedirs("Graphs")

    for file in os.listdir(directory):
        budget_sequence = []
        money_sequence = []
        print(f"Transactions for {file}")
        # Read the CSV file
        df = pd.read_csv('ndx100/' + os.fsdecode(file))

        # Calculate 50-day SMA
        df['Short_SMA'] = df['CLOSE'].rolling(window=50).mean()

        # Calculate 200-day SMA
        df['Long_SMA'] = df['CLOSE'].rolling(window=200).mean()

        # Convert 'DATE' column to datetime format
        df['DATE'] = pd.to_datetime(df['DATE'])

        # Filter dataframe based on user input date range
        # df = df[(df['DATE'] >= start_date) & (df['DATE'] <= end_date)]
        df = df.query('DATE >= @start_date and DATE <= @end_date').reset_index()



        # Find intersections
        df['Signal'] = 0  # Initialize a column to mark intersections
        position = 0
        for i in range(1, len(df)):
            try:
                if df.at[i, 'Short_SMA'] > df.at[i, 'Long_SMA'] and df.at[i - 1, 'Short_SMA'] <= df.at[i - 1, 'Long_SMA']:
                    # Check if budget allows buying
                    df.at[i, 'Signal'] = 1  # Upward crossover
                    print(f"BUY at {df.at[i, 'DATE']}")
                    money_spent += df.at[i, 'CLOSE']
                    position += 1
                    
                elif df.at[i, 'Short_SMA'] < df.at[i, 'Long_SMA'] and df.at[i - 1, 'Short_SMA'] >= df.at[i - 1, 'Long_SMA']:
                    if (position > 0):
                        df.at[i, 'Signal'] = -1  # Downward crossover
                        print(f"SELL at {df.at[i, 'DATE']}")
                        money_gained += df.at[i, 'CLOSE']
                        position -= 1
                total_money = position * df.at[i, 'CLOSE'] + money_gained - money_spent
                money_sequence.append(total_money)
                budget_sequence.append(money_gained - money_spent)
            except KeyError:
                continue
        try:
            money_gained += position*df['CLOSE'].iloc[-1]
            final_money_gained += money_gained
            final_money_spent += money_spent
            money_gained, money_spent = 0,0
            money_sequences.append(money_sequence)  
            budget_sequences.append(budget_sequence)
        except:
            continue

    for i in range(len(money_sequences[0])):
        money_on_date = 0
        for sequence in money_sequences:
            try:
                money_on_date += sequence[i]
            except:
                pass
        final_money.append(money_on_date)

    for i in range(len(budget_sequences[0])):
        money_on_date = 0
        for sequence in budget_sequences:
            try:
                money_on_date += sequence[i]
            except:
                pass
        final_budget.append(money_on_date)

    fig2, ax2 = plt.subplots(figsize=(15, 6))
    ax2.plot(df['DATE'][1:],final_money, label='Money sequence', linestyle='-', color='black', linewidth=3)
    ax2.set_xlabel('Date')
    ax2.set_title('Cash on hand evolution')
    ax2.set_ylabel('Money')

    max_borrow = min(final_budget) * -1
    final_return = (final_money[-1] - max_borrow)/max_borrow

    st.pyplot(fig2)
    st.write(f'Return from {start_date} to {end_date} is {final_return*100:.2f}%')
    