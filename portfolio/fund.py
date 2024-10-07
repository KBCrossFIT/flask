import pandas as pd
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier

# 펀드 데이터
fund_list = [
    ["펀드A", 0.02, 0.03, 0.04, 0.05, 3, 0.01, 0.015, 1000000],
    ["펀드B", 0.01, 0.015, 0.02, 0.03, 2, 0.005, 0.01, 1000000],
    ["펀드C", 0.025, 0.035, 0.045, 0.06, 4, 0.015, 0.02, 1000000],
    ["펀드D", 0.015, 0.025, 0.035, 0.04, 5, 0.02, 0.025, 1000000],
    ["펀드E", 0.03, 0.04, 0.05, 0.07, 1, 0.005, 0.012, 1000000]
]

# 데이터프레임으로 변환
df = pd.DataFrame(fund_list, columns=["이름", "1개월 수익률", "3개월 수익률", "6개월 수익률", "12개월 수익률", "위험등급", "선취 수수료", "총 보수", "투자금액"])

# 연환산 수익률 계산
def annualized_return(row):
    return row['12개월 수익률']  # 12개월 수익률을 연환산 수익률로 사용

df['연환산 수익률'] = df.apply(annualized_return, axis=1)

# 변동성 계산 함수
def calculate_volatility(row):
    # 위험등급에 따라 변동성 추정 (1~6 등급)
    return (7 - row['위험등급']) * 0.1  # 등급이 높을수록 변동성이 낮다고 가정 (0.1~0.5 범위)

df['변동성'] = df.apply(calculate_volatility, axis=1)

# 포트폴리오 최적화
mu = df['연환산 수익률']
S = pd.DataFrame(index=df.index, columns=df.index)

# 공분산 행렬 생성 (위험도와 투자금액으로 추정)
for i in range(len(df)):
    for j in range(len(df)):
        S.iloc[i, j] = df.loc[i, '변동성'] * df.loc[j, '변동성'] * 0.01  # 변동성의 조합으로 공분산 생성

ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()  # 샤프 비율 최대화
print("최적 비율:", weights)

# 비율 정리
cleaned_weights = ef.clean_weights()
print("정리된 비율:", cleaned_weights)

# 포트폴리오 성과 계산
performance = ef.portfolio_performance()
print("포트폴리오 성과:", performance)