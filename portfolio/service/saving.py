import pandas as pd
import FinanceDataReader as fdr

from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier

import pandas as pd

# 예적금 데이터
product_list = [
    ["won플러스예금", "예금", 36, "단리", 3.00, 3.00, 1000000],
    ["KDB 자유적금", "적금", 24, "단리", 2.77, 2.77, 100000],
    ["KB국민프리미엄적금", "적금", 12, "단리", 2.75, 3.65, 100000],
    ["NH직장인월복리적금", "적금", 12, "복리", 3.32, 4.12, 100000],
    ["미즈월복리정기예금", "예금", 36, "복리", 2.78, 2.98, 1000000]
]

# 데이터프레임으로 변환
df = pd.DataFrame(product_list, columns=["이름", "분류", "만기(개월)", "단리/복리", "최저 금리", "최대 금리", "금액"])

# 연환산 수익률 계산 함수
def calculate_annualized_return(row):
    if row['단리/복리'] == "단리":
        return row['최저 금리']  # 단리는 최저 금리로 가정
    else:
        # 복리 수익률 계산 (최대 금리를 사용하여 계산)
        return ((1 + row['최대 금리'] / 100) ** (row['만기(개월)'] / 12)) - 1

# 연환산 수익률 컬럼 추가
df['연환산 수익률'] = df.apply(calculate_annualized_return, axis=1)

# 변동성은 0으로 가정
df['변동성'] = 0

# 결과 출력
print("예적금 데이터:")
print(df[['이름', '연환산 수익률', '변동성']])

# 포트폴리오 비율 최적화
# 각 예적금의 금액에 따른 비율 계산
total_investment = df['금액'].sum()
df['비율'] = df['금액'] / total_investment

# 결과 출력
print("\n포트폴리오 비율:")
print(df[['이름', '비율']])