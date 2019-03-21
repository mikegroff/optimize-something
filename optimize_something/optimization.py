"""MC1-P2: Optimize a portfolio.

Copyright 2018, Georgia Institute of Technology (Georgia Tech)
Atlanta, Georgia 30332
All Rights Reserved

Template code for CS 4646/7646

Georgia Tech asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including repositories
such as github and gitlab.  This copyright statement should not be removed
or edited.

We do grant permission to share solutions privately with non-students such
as potential employers. However, sharing with other current or future
students of CS 7646 is prohibited and subject to being investigated as a
GT honor code violation.

-----do not edit anything above this line---

Student Name: Michael Groff
GT User ID: mgroff3
GT ID: 900897987
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data
import scipy.optimize as opt

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    #normed = prices/prices[0,:]

    prices_SPY = prices_SPY.div(prices_SPY.iloc[0])
    normp = prices.div(prices.iloc[0])
    length = len(syms)
    initial = np.ones(length)/length
    def sharperatio(X):
        alloced = normp*X
        port_val = alloced.sum(axis=1)
        daily_returns = (port_val / np.roll(port_val, 1)) - 1
        daily_returns = daily_returns[1:]
        return -np.sqrt(252)*daily_returns.mean()/daily_returns.std(ddof=1)

    allocs = opt.minimize(sharperatio,initial,bounds = tuple((0., 1.) for _ in range(length)), constraints = ({ 'type': 'eq', 'fun': lambda inputs: 1.0 - np.sum(inputs) })).x
    #print(allocs.sum())
    falloced = normp*allocs
    fport_val = falloced.sum(axis=1)
    fdaily_returns = (fport_val / np.roll(fport_val, 1)) - 1
    fdaily_returns = fdaily_returns[1:]
    cr =  (fport_val[-1] / fport_val[0]) - 1
    adr = fdaily_returns.mean()
    sddr = fdaily_returns.std(ddof=1)
    sr = np.sqrt(252)*adr/sddr

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([fport_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        #with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        #    print(df_temp)
        plt.figure(1)
        ax = df_temp.plot()
        ax.xaxis.set_major_locator(plt.MaxNLocator(13))
        ax.yaxis.set_major_locator(plt.MaxNLocator(13))
        plt.grid(linestyle='--')
        plt.title("Daily Portfolio Value and SPY")
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.savefig('compare.png', bbox_inches='tight')
        plt.show()
        pass


    return allocs, cr, adr, sddr, sr

def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2008,6,1)
    end_date = dt.datetime(2009,6,1)
    symbols = ['IBM', 'X', 'GLD', 'JPM']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
