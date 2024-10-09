import QuantLib as ql

bond = {
    'bondIssuDt': '20221031', # 발행일
    'bondExprDt': '20271031', # 만기일  
    'irtChngDcdNm': "고정-복리", # 금리변동구분코드명(복리, 단리, 복5단2) 
    'bondSrfcInrt': 8.00, # 채권 금리 
    'intPayCyclCtt': "12개월", # 이자지급주기
    'clprPrc': 9592.50, # 채권 종가
    'kbpScrsItmsKcdNm': "", # 한국신용평가유가증권종목종류코드명
    'amount': "" # 투자금액
}

def calculate_bond(bond):
    calc_data = {
        'expectedReturn': 0,
        'riskLevel': 0, 
        'amount': 0
    }
    # issu_year = int(bond['bondIssuDt'][:4])
    # issu_month = int(bond['bondIssuDt'][4:6])
    # issu_day = int(bond['bondIssuDt'][6:])
    expr_year = int(bond['bondExprDt'][:4])
    expr_month = int(bond['bondExprDt'][4:6])
    expr_day = int(bond['bondExprDt'][6:])
    
    face_value = 100  # 액면가
    coupon_rate = bond['bondSrfcInrt'] / 100 # 연간 이자율
    current_price = bond['clprPrc'] / 100 # 현재 가격
    # issu_date = ql.Date(issu_day, issu_month, issu_year)
    maturity_date = ql.Date(expr_day, expr_month, expr_year)  # 만기일
    base_date = ql.Date.todaysDate()
    # ql.Date(today.day, today.month, today.year)  # 결제일

    if(bond['intPayCyclCtt'] == "1개월"):
        int_pay_cycl = ql.Period(1, ql.Months)
    elif(bond['intPayCyclCtt'] == "3개월"):
        int_pay_cycl = ql.Quarterly
    elif(bond['intPayCyclCtt'] == "6개월"):
        int_pay_cycl = ql.Semiannual
    elif(bond['intPayCyclCtt'] == "12개월"):
        int_pay_cycl = ql.Annual
    else:
        int_pay_cycl = ql.Annual
        
    # QuantLib에서 날짜 설정
    # ql.Settings.instance().evaluationDate = base_date
    # base_date
    print(base_date)
    print(maturity_date)
    print(int_pay_cycl)
    print(face_value)
    print(coupon_rate)
    
    # 채권 생성
    coupon_schedule = ql.Schedule(base_date,
                                maturity_date,
                                ql.Period(int_pay_cycl),
                                ql.NullCalendar(),
                                ql.Unadjusted,
                                ql.Unadjusted,
                                ql.DateGeneration.Backward,
                                False)

    new_bond = ql.FixedRateBond(2, 
                                face_value, 
                                coupon_schedule, 
                                [1, coupon_rate], 
                                ql.Actual365Fixed()
                                )

    if(bond['irtChngDcdNm'] == '고정-복리'):
        # YTM 계산
        ytm = new_bond.bondYield(current_price, ql.Actual365Fixed(), ql.Compounded, int_pay_cycl, base_date)
    else: 
        ytm = new_bond.bondYield(current_price, ql.Actual365Fixed(), ql.Simple, int_pay_cycl)

    calc_data['expectedReturn'] = ytm
    
    
    
    
    # # 복5단2의 경우
    # if(bond['irtChngDcdNm'] == '고정-복5단2'):
    #     if(base_date < maturity_date - ql.Period(2, ql.Years)):
    #         coupon_schedule_compound = ql.Schedule(base_date,
    #                                             maturity_date - ql.Period(2, ql.Years),
    #                                             ql.Period(int_pay_cycl),
    #                                             ql.NullCalendar(),
    #                                             ql.Unadjusted,
    #                                             ql.Unadjusted,
    #                                             ql.DateGeneration.Backward,
    #                                             False)

    #         # 복리 채권 생성
    #         # bond_compound = ql.FixedRateBond(1, ql.NullCalendar(), face_value, coupon_schedule_compound, [coupon_rate])
    #         bond_compound = ql.FixedRateBond(base_date, 
    #                                         face_value, 
    #                                         coupon_schedule_compound, 
    #                                         [coupon_rate], 
    #                                         ql.Actual360,
    #                                         ql.Following,
    #                                         100.0,
    #                                         issu_date,
    #                                         ql.NullCalendar,
    #                                         ql.Period(1, ql.Months), 
    #                                         ql.NullCalendar(),
    #                                         ql.Unadjusted,
    #                                         False,
    #                                         ql.Actual360()
    #                                         )


    #         # YTM 계산 (복리)
    #         ytm_compound = bond_compound.yieldRate(current_price, ql.Actual360(), ql.Bond.Yield, ql.Compounded)
            
    #         coupon_schedule_simple = ql.Schedule(maturity_date - ql.Period(2, ql.Years),
    #                                             maturity_date,
    #                                             ql.Period(int_pay_cycl),
    #                                             ql.NullCalendar(),
    #                                             ql.Unadjusted,
    #                                             ql.Unadjusted,
    #                                             ql.DateGeneration.Backward,
    #                                             False)

    #         # 단리 채권 생성
    #         bond_simple = ql.FixedRateBond(1, ql.NullCalendar(), face_value, coupon_schedule_simple, [coupon_rate])

    #         # 단리 YTM 계산
    #         ytm_simple = bond_simple.yieldRate(current_price, ql.Actual360(), ql.Bond.Yield, ql.Simple)

    #         # 복리와 단리 수익률 고려: 가중 평균
    #         ytm = (ytm_compound * 5 + ytm_simple * 2) / (5 + 2)
    #     else: 
    #         coupon_schedule = ql.Schedule(base_date,
    #                                             maturity_date,
    #                                             ql.Period(int_pay_cycl),
    #                                             ql.NullCalendar(),
    #                                             ql.Unadjusted,
    #                                             ql.Unadjusted,
    #                                             ql.DateGeneration.Backward,
    #                                             False)

    #         # 단리 채권 생성
    #         bond_simple = ql.FixedRateBond(1, ql.NullCalendar(), face_value, coupon_schedule, [coupon_rate])

    #         # 단리 YTM 계산
    #         ytm = bond_simple.yieldRate(current_price, ql.Actual360(), ql.Bond.Yield, ql.Simple)
    # else: 
    #     # 채권 생성
    #     coupon_schedule = ql.Schedule(base_date,
    #                                 maturity_date,
    #                                 ql.Period(int_pay_cycl),
    #                                 ql.NullCalendar(),
    #                                 ql.Unadjusted,
    #                                 ql.Unadjusted,
    #                                 ql.DateGeneration.Backward,
    #                                 False)

    #     new_bond = ql.FixedRateBond(20241009, 
    #                                         face_value, 
    #                                         coupon_schedule, 
    #                                         [coupon_rate], 
    #                                         ql.Actual360(),
    #                                         )

    #     if(bond['irtChngDcdNm'] == '고정-복리'):
    #         # YTM 계산
    #         ytm = new_bond.bondYield(current_price, ql.Actual360(), ql.Compounded, int_pay_cycl)
    #     else: 
    #         ytm = new_bond.bondYield(current_price, ql.Actual360(), ql.Simple)
    
    # calc_data['expectedReturn'] = ytm
    
    # 위험등급
    
    if(bond['kbpScrsItmsKcdNm'] in ['']):
        calc_data['expectedReturn'] = 6
    elif(bond['kbpScrsItmsKcdNm'] in ['AAA', 'AA+', 'AA', 'AA-']):
        calc_data['expectedReturn'] = 5
    elif(bond['kbpScrsItmsKcdNm'] in ['A+', 'A', 'A-']):
        calc_data['expectedReturn'] = 4
    elif(bond['kbpScrsItmsKcdNm'] in ['BBB+', 'BBB', 'BBB-']):
        calc_data['expectedReturn'] = 3
    elif(bond['kbpScrsItmsKcdNm'] in ['BB+', 'BB', 'BB-']):
        calc_data['expectedReturn'] = 2
    else:
        calc_data['expectedReturn'] = 1
        
    calc_data['amount'] = bond['amount']
    
    return calc_data

# data = calculate_bond(bond)
# print(data)













# def calculate_ytm(price, face_value, coupon_rate, years, iterations=1000, tolerance=1e-6):
#     """
#     채권의 YTM을 계산하는 함수입니다.

#     :param price: 채권의 현재 가격
#     :param face_value: 채권의 액면가
#     :param coupon_rate: 채권의 쿠폰 금리 (연간 이자율)
#     :param years: 채권의 만기까지 남은 기간 (연 단위)
#     :param iterations: 수치적 방법을 반복할 최대 횟수
#     :param tolerance: 정확도 기준
#     :return: 연환산 수익률(YTM)
#     """
#     # 연간 쿠폰 지급액
#     coupon_payment = face_value * coupon_rate

#     # 수치적 방법을 이용한 YTM 계산 (이분법 사용)
#     lower_bound = 0.0
#     upper_bound = 1.0  # 초기 상한선은 100%로 설정
#     for i in range(iterations):
#         ytm = (lower_bound + upper_bound) / 2
#         total_value = sum([coupon_payment / (1 + ytm)**t for t in range(1, years + 1)]) + \
#                       face_value / (1 + ytm)**years
#         # 가격 비교 후 YTM 조정
#         if total_value < price:
#             upper_bound = ytm
#         else:
#             lower_bound = ytm

#         # 수렴 조건 체크
#         if abs(total_value - price) < tolerance:
#             break

#     return ytm

# # 예시 데이터
# current_price = 950  # 현재 채권 가격
# face_value = 1000    # 액면가
# coupon_rate = 0.05   # 5% 쿠폰 금리
# maturity_years = 5   # 만기 5년

# ytm = calculate_ytm(current_price, face_value, coupon_rate, maturity_years)
# print(f"채권의 YTM: {ytm * 100:.2f}%")

# def calculate_volatility(returns):
#     """
#     채권 수익률의 변동성을 계산하는 함수입니다.

#     :param returns: 채권 수익률 리스트 (과거 수익률 데이터)
#     :return: 수익률의 변동성 (표준 편차)
#     """
#     # 수익률의 표준 편차를 계산하여 변동성을 반환
#     return np.std(returns)

# # 예시 데이터 (과거 수익률)
# bond_returns = [0.01, 0.015, -0.002, 0.005, -0.01, 0.02, 0.005]  # 수익률 예시
# volatility = calculate_volatility(bond_returns)
# print(f"채권 수익률 변동성: {volatility:.4f}")