import numpy as np
import FinanceDataReader as fdr

from pypfopt.expected_returns import mean_historical_return
from datetime import datetime
from pandas.tseries.offsets import BDay

stock = {
    "stockCode": '035720',  # 주식코드
    "amount": 10  # 주식 수
}

def calculate_stock(stock):
    calc_data = {
        'expectedReturn': 0,
        'riskLevel': 0,
        'amount': 0
    }
    
    # 주식코드로 개별 종목에 대해 3년치 데이터를 받아옴(1년 영업일 252일 기준으로 3년 전부터 오늘 기준 1영업일 전까지)
    ticker = stock['stockCode']
    start_date = (datetime.today() - BDay(756)).strftime('%Y-%m-%d')
    end_date = (datetime.today() - BDay(1)).strftime('%Y-%m-%d')
    
    # 주식 데이터 가져오기
    df = fdr.DataReader(ticker, start_date, end_date)

    # 주식 가격이 존재하는지 확인
    if df.empty:
        raise ValueError("주식 데이터가 없습니다.")

    # 기대수익률 계산
    expected_return = mean_historical_return(df['Close'].dropna()) * 100
    calc_data['expectedReturn'] = round(expected_return[0], 2)

    # 수익률 변동성 계산
    std = np.std(df['Change'].dropna()) #표준편차 계산
    volatility = std * np.sqrt(252) * 100

    if(volatility > 25):
        calc_data['riskLevel'] = 1
    elif(volatility > 15):
        calc_data['riskLevel'] = 2
    elif(volatility > 10):
        calc_data['riskLevel'] = 3
    elif(volatility > 5):
        calc_data['riskLevel'] = 4
    elif(volatility > 0.5):
        calc_data['riskLevel'] = 5
    else:
        calc_data['riskLevel'] = 6

    calc_data['amount'] = stock['amount'] * df.loc[end_date, 'Close']

    # 샤프 비율 계산 (주석 처리된 부분)
    risk_free_rate = 0.01  # 무위험 이자율 (예: 1%)
    sharpe_ratio = (expected_return - risk_free_rate) / volatility

    return calc_data

# 계산 결과 출력
print(calculate_stock(stock))
