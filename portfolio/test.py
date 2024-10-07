import pandas as pd
import FinanceDataReader as fdr

from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier

stock_list = [
    ["삼성전자","005930"],
    ["SK하이닉스", "000660"],
    ["기아", "000270"],
    ["카카오", "035720"],
    ["KB금융그룹", "105560"]
]
df_list=[fdr.DataReader(code[1], '2023', '2024')['Close'] for code in stock_list]
df = pd.concat(df_list, axis=1)
df.columns = [name for name, code in stock_list]
df.head(10)

mu = mean_historical_return(df);
S = CovarianceShrinkage(df).ledoit_wolf()

ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()
print(weights)
cleaned_weights = ef.clean_weights()
print(cleaned_weights)

performance = ef.portfolio_performance()
print(performance)

