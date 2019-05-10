# -*- coding: utf-8 -*-
"""
Created this assignment for Wealthy, It's a command line tool to which takes user input
like stock symbol, start day, end day and outputs on which days the stock should be bought and
and sold to get maximum profit, it also calculates mean, standard deviation for given time interval.

Created on 11th May, 2019

@author: Shalini Jha
"""

import csv
import sys
from datetime import datetime, timedelta
from dateutil.parser import parse
from time import strptime
import statistics
import argparse


def get_data(path):
    stock = {}
    with open(path, 'r') as file:
        reader = csv.DictReader(file, ('StockName', 'StockDate', 'StockPrice'))
        next(reader)
        for row in reader:
            try:
                if row['StockName'] not in stock:
                    stock[row['StockName']] = {parse(row['StockDate']): float(row['StockPrice'])}
                else:
                    stock[row['StockName']][parse(row['StockDate'])] = float(row['StockPrice'])

            except ValueError:
                print("Data is missing in", row['StockName'], row['StockDate'], row['StockPrice'])
        return stock

    # Adapted from http://norvig.com/spell-correct.html


def known(stock, words):
    """The subset of `words` that appear in the dictionary of stock."""
    return set(w for w in words if w in stock)


def edits1(word):
    """All edits that are one edit away from `word`."""
    letters = 'abcdefghijklmnopqrstuvwxyz'.upper()
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def correction(symbol, stock):
    """Most probable spelling correction for word."""
    return known(stock, edits1(symbol))


# End of reference from http://norvig.com/spell-correct.html


def walk_days(start_date, end_date):
    date = start_date
    while date <= end_date:
        yield date
        date = date + timedelta(days=1)


def buy_and_sell(stock, symbol, start_date, end_date):
    stock_price_dictionary = {}
    if symbol in stock:
        earliest_date = min(stock[symbol])
        latest_date = max(stock[symbol])
        if end_date < start_date:
            print("end date can't be before start date ")
            return None
        if end_date < earliest_date or latest_date < start_date:
            print("we don't have data for the requested period")
            return None
        if start_date not in stock[symbol]:
            if earliest_date > start_date:
                print("we don't have data before", earliest_date)
                start_date = earliest_date
            else:
                list_of_dates_before_startdate = [x for x in stock[symbol] if x < start_date]
                prev_price = stock[symbol][max(list_of_dates_before_startdate)]

        for date in walk_days(start_date, end_date):
            if date in stock[symbol]:
                prev_price = stock_price_dictionary[date] = stock[symbol][date]
            else:
                stock_price_dictionary[date] = prev_price
        mean_value = statistics.mean(stock_price_dictionary.values())
        std_dev = statistics.stdev(stock_price_dictionary.values())
        buy_date = min(stock_price_dictionary, key=lambda date: stock_price_dictionary[date])
        sell_date = max(stock_price_dictionary, key=lambda date: stock_price_dictionary[date])
        profit = (stock_price_dictionary[sell_date] - stock_price_dictionary[buy_date]) * 100
        buy_date= buy_date.date().strftime('%d-%b-%Y')
        sell_date = sell_date.date().strftime('%d-%b-%Y')
        if profit == 0:
            buy_date = 'None'
            sell_date = 'None'
            print("stockprice didn't change during this period")

        return mean_value, std_dev, buy_date, sell_date, profit
                                          


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Stock price analysis')
    parser.add_argument("path", help="path to the csv file to process")
    args = parser.parse_args()
    try:
        stock = get_data(args.path)
    except OSError:
        print("Can't find file or can't open file. Exiting.")
        exit()
    except csv.Error:
        print("Can't parse input file. Exiting.")
        exit()


    def yes_or_no(message):
        while True:
            answer = input(message).lower()
            if answer == 'yes' or answer == 'y':
                return "yes"
            elif answer == 'no' or answer == 'n':
                return "no"
            else:
                print("Please respond with (y)es or (n)o")
                if input("Press 1 to exit or any other key to continue") == "1":
                    sys.exit()


    def get_date(message):
        while True:
            answer = input(message)
            try:
                return parse(answer)
            except (ValueError, OverflowError):
                print("Error: Please enter valid date")
                if input("Press 1 to exit or any other key to continue") == "1":
                    sys.exit()


    while True:
        symbol = input('Welcome Agent! Which stock you need to process?":- ').upper()
        if symbol not in stock:
            for stockname in correction(symbol, stock):
                if yes_or_no(f'Oops! Do you mean {stockname}? y or n: ') == 'yes':
                    symbol = stockname
                    break
            else:
                print(f"{symbol} not in dataset")
                continue
        start_date = get_date('"From which date you want to start":- ')
        end_date = get_date('"Till which date you want to analyze":- ')

        buy_and_sell_result = buy_and_sell(stock, symbol, start_date, end_date)
        if buy_and_sell_result is not None:
            print('"Here is you result":- Mean: {},Std: {}, Buy Date: {}, Sell Date: {}, Profit: {}'.format(
                *buy_and_sell_result))

        if yes_or_no("Do you want to continue? (y or n):-") == "no":
            break
