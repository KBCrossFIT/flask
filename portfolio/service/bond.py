import numpy as np

def calculate_ytm(price, face_value, coupon_rate, years, iterations=1000, tolerance=1e-6):
    """
    채권의 YTM을 계산하는 함수입니다.

    :param price: 채권의 현재 가격
    :param face_value: 채권의 액면가
    :param coupon_rate: 채권의 쿠폰 금리 (연간 이자율)
    :param years: 채권의 만기까지 남은 기간 (연 단위)
    :param iterations: 수치적 방법을 반복할 최대 횟수
    :param tolerance: 정확도 기준
    :return: 연환산 수익률(YTM)
    """
    # 연간 쿠폰 지급액
    coupon_payment = face_value * coupon_rate

    # 수치적 방법을 이용한 YTM 계산 (이분법 사용)
    lower_bound = 0.0
    upper_bound = 1.0  # 초기 상한선은 100%로 설정
    for i in range(iterations):
        ytm = (lower_bound + upper_bound) / 2
        total_value = sum([coupon_payment / (1 + ytm)**t for t in range(1, years + 1)]) + \
                      face_value / (1 + ytm)**years
        # 가격 비교 후 YTM 조정
        if total_value < price:
            upper_bound = ytm
        else:
            lower_bound = ytm

        # 수렴 조건 체크
        if abs(total_value - price) < tolerance:
            break

    return ytm

# 예시 데이터
current_price = 950  # 현재 채권 가격
face_value = 1000    # 액면가
coupon_rate = 0.05   # 5% 쿠폰 금리
maturity_years = 5   # 만기 5년

ytm = calculate_ytm(current_price, face_value, coupon_rate, maturity_years)
print(f"채권의 YTM: {ytm * 100:.2f}%")

def calculate_volatility(returns):
    """
    채권 수익률의 변동성을 계산하는 함수입니다.

    :param returns: 채권 수익률 리스트 (과거 수익률 데이터)
    :return: 수익률의 변동성 (표준 편차)
    """
    # 수익률의 표준 편차를 계산하여 변동성을 반환
    return np.std(returns)

# 예시 데이터 (과거 수익률)
bond_returns = [0.01, 0.015, -0.002, 0.005, -0.01, 0.02, 0.005]  # 수익률 예시
volatility = calculate_volatility(bond_returns)
print(f"채권 수익률 변동성: {volatility:.4f}")