import pandas as pd
import numpy as np
import FinanceDataReader as fdr

from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier

from portfolio.service.saving import calculate_saving
from portfolio.service.fund import calculate_fund
from portfolio.service.bond import calculate_bond
from portfolio.service.stock import calculate_stock

# portfolio_items = [
#     {
#         "productId": 1,
#         "productType": "F",
#         "yield1": 8.85, 
#         "yield3": 6.70, 
#         "yield6": 0.78, 
#         "yield12": -3.45, 
#         "riskLevel": 1, 
#         "advancedFee": 1.00, 
#         "totalPayoffRate": 1.56, 
#         "amount": 1000000 
#     },
#     {
#         "productId": 2,
#         "productType": "S",
#         "rsrvType": "F", 
#         "saveTerm": 12, 
#         "intrType": "복리", 
#         "intrRate": 3.50,
#         "amount": 1000000, 
#     },
#     {
#         "stockCode": "035720", 
#         "amount": 10  
#     }
# ]

def calculate_portfolio(portfolio_items):
    print(portfolio_items)
    
    mu = []
    risks = []
    amount = []
    weights = []
    portfolio = {
        "total": 0,
        "expectedReturn": 0,
        "riskLevel": 0,
        "portfolioItems": []
    }
    
    for i in range(len(portfolio_items)):
        portfolio_item = {
            "productId" : 0,
            "stockCode" : "",
            "amount" : 0,
            "expectedReturn" : 0,
            "riskLevel" : 0
        }
        
        temp = []
        portfolio_item["productId"] = portfolio_items[i].get("productId")
        portfolio_item["stockCode"] = portfolio_items[i].get("stockCode")
        portfolio_item["amount"] = portfolio_items[i].get("amount")        
        if(portfolio_items[i].get('productType') == "S"):
            temp = calculate_saving(portfolio_items[i])
        elif(portfolio_items[i].get('productType') == "F"):
            # portfolio_item["productId"] = portfolio_items[i].get("productId")
            temp = calculate_fund(portfolio_items[i])
            
        elif(portfolio_items[i].get('productType') == "B"):
            # portfolio_item["productId"] = portfolio_items[i].get("productId")
            temp = calculate_bond(portfolio_items[i])
        else:
            # portfolio_item["stockCode"] = portfolio_items[i].get("stockCode")
            temp = calculate_stock(portfolio_items[i])

        # temp return 값은 expectedReturn, riskLevel, amount

        portfolio_item['expectedReturn'] = temp['expectedReturn']
        mu.append(temp['expectedReturn'])
        portfolio_item['riskLevel'] = temp['riskLevel']
        risks.append(temp['riskLevel'])
        portfolio['total'] += temp['amount']
        amount.append(temp['amount'])
        portfolio["portfolioItems"].append(portfolio_item)
    
    for i in range(len(amount)):
        weights.append(amount[i] / portfolio['total'])
    
    
    portfolio['expectedReturn'] = round(np.dot(mu, weights), 2)
    portfolio['riskLevel'] = round(np.dot(risks, weights), 2)
    
    print(portfolio)
    
    return portfolio

# print(calculate(portfolio_items))