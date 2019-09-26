import pprint
import datetime as dt
import yfinance as yf
from operator import mul
#from pandas_datareader import data as pdr
import pandas as pd
from pandas import DataFrame

# TODO:
# - Remove holding in a portfolio
# - Personal return
# - Portfolio return
# - Portfolio total market value
# - Portfolio total cost
# - Dividends and splits :(
# - Cash position?
# - Graphed periodic returns

# Fundamentals TODO:
# - ROE
# - BV growth
# - EPS growth
# - Sales growth
# - Dividends
# - Debt / FCF?
# - FCF

# start_sp = dt.datetime(2013,1,1)
# end_sp = dt.datetime(2018,3,9)
# end_of_last_year = dt.datetime(2018,12,29)
# stocks_start = dt.datetime(2013,1,1)
# stocks_end = dt.datetime(2018,3,9)
# yf.pdr_override()

# print("Total number of " + str(holding1.tickerStr) + ": " + str(holding1.totalShares()))
# print("Average cost: " + str(holding1.avgCost()))
# print("Last quote: " + str(holding1.lastQuote()))
# print("G/L: " + str(holding1.gl()))

#sp500 = pdr.get_data_yahoo('^GSPC')
#fl = yf.Ticker("FL")
#print(fl.financials)

		# print("Total number of " + str(this.tickerStr) + ": " + str(this.totalShares()))
		# print("Average cost: " + str(this.avgCost()))
		# print("Last quote: " + str(this.lastQuote()))
		# print("G/L: " + str(this.gl()))

class Portfolio:
	def __init__(this,total,currancy):
		this.total = total
		this.equity = 0
		this.currancy = currancy
		this.numHoldings = 0
		this.holdings = []
		
	def addPosition(this,holding,index):
		this.holdings.append(holding)
		this.numHoldings += 1
		this.total -= sum(holding.price)

	def qprint(this):
		print("Ticker\tLot\tCost\tQuote\tG/L")
		for i in this.holdings:
			i.qprint()
		print("Cash: " + str(this.total))

class Stock:
	def __init__(this,ticker):
		this.tickerStr = ticker
		this.ticker = yf.Ticker(ticker)
		this.info = this.ticker.info
		this.bs = this.ticker.balance_sheet.fillna(0)
		this.fin = this.ticker.financials.fillna(0)

	def lastQuote(this):
		return this.ticker.info["regularMarketPrice"]

	def debt(this):
		return int(this.bs.iloc[17,0])

	def marketCap(this):
		return this.info["marketCap"]

	def cash(this):
		return int(this.bs.iloc[1,0])

	def ev(this):
		return this.marketCap()+this.debt()-this.cash()

	def oe(this):
		return int(this.fin.iloc[9,0])

	def am(this):
		return round(this.ev()/this.oe(),2)

class Holding:
	def __init__(this,ticker,shares,price,date):
		this.tickerStr = ticker
		this.shares = []
		this.date = []
		this.price = []
		this.numLots = 0
		this.shares.append(shares)
		this.price.append(price)
		this.date.append(date)
		this.numLots += 1
		this.ticker = yf.Ticker(ticker)
		this.info = this.ticker.info
		this.bs = this.ticker.balance_sheet.fillna(0)
		this.fin = this.ticker.financials.fillna(0)

	def addLot(this,shares,price,date):
		this.shares.append(shares)
		this.price.append(price)
		this.date.append(date)
		this.numLots += 1

	def totalShares(this):
		return sum(this.shares)

	def avgCost(this):
		return sum(map(mul,this.shares,this.price))/sum(this.shares)

	def lastQuote(this):
		return this.ticker.info["regularMarketPrice"]

	def gl(this):
		lq = this.ticker.info["regularMarketPrice"]
		ac = sum(map(mul,this.shares,this.price))/sum(this.shares)
		ts = sum(this.shares)
		return round((lq - ac) * ts, 2)

	def qprint(this):
		print(str(this.tickerStr)+'\t'+str(this.totalShares())+'\t'+str(this.avgCost())+'\t'+str(this.lastQuote())+'\t'+str(this.gl()))

	def debt(this):
		return int(this.bs.iloc[17,0])

	def marketCap(this):
		return this.info["marketCap"]

	def cash(this):
		return int(this.bs.iloc[1,0])

	def ev(this):
		return this.marketCap()+this.debt()-this.cash()

	def oe(this):
		return int(this.fin.iloc[9,0])

	def am(this):
		return round(this.ev()/this.oe(),2)

yf.pdr_override()
holding1 = Holding("AAPL",10,190,dt.date(2019,8,20))
holding2 = Holding("SYF",50,34.5,dt.date(2019,7,20))

holding1.addLot(15,200,dt.date(2019,8,22))

cadPort = Portfolio(50000,"CAD")
cadPort.addPosition(holding1,cadPort.numHoldings)
cadPort.addPosition(holding2,cadPort.numHoldings)

cadPort.qprint()

temp = Stock("BBBY")
df = temp.bs.fillna(0)
print(temp.am())
