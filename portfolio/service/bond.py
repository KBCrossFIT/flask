import QuantLib as ql

# bond = {
#     'bondExprDt': '20271031', # 만기일  
#     'irtChngDcdNm': "고정-복리", # 금리변동구분코드명(복리, 단리, 복5단2) 
#     'bondSrfcInrt': 1.00, # 채권 금리 
#     'intPayCyclCtt': "12개월", # 이자지급주기
#     'clprPrc': 9592.50, # 채권 종가
#     'kbpScrsItmsKcdNm': "AAA", # 한국신용평가유가증권종목종류코드명
#     'amount': 1000000 # 투자금액
# }

def calculate_bond(bond):
    calc_data = {
        'expectedReturn': 0,
        'riskLevel': 0, 
        'amount': 0
    }
    expr_year = int(bond['bondExprDt'][:4])
    expr_month = int(bond['bondExprDt'][4:6])
    expr_day = int(bond['bondExprDt'][6:])
    
    face_value = 100  # 액면가
    coupon_rate = bond['bondSrfcInrt'] / 100 # 연간 이자율
    current_price = bond['clprPrc'] / 100 # 현재 가격
    maturity_date = ql.Date(expr_day, expr_month, expr_year)  # 만기일
    base_date = ql.Date.todaysDate()

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
    ql.Settings.instance().evaluationDate = base_date
    
    # 복5단2의 경우
    if(bond['irtChngDcdNm'] == '고정-복5단2'):
        # 만기까지의 기간이 2년 이상일 경우: 복리채 + 단리채 계산 후 가중평균 ytm 계산
        if(base_date < maturity_date - ql.Period(2, ql.Years)):
            coupon_schedule_compound = ql.Schedule(base_date,
                                                maturity_date - ql.Period(2, ql.Years),
                                                ql.Period(int_pay_cycl),
                                                ql.NullCalendar(),
                                                ql.Unadjusted,
                                                ql.Unadjusted,
                                                ql.DateGeneration.Backward,
                                                False)

            # 복리 채권 생성
            bond_compound = ql.FixedRateBond(2, 
                                face_value, 
                                coupon_schedule_compound, 
                                [coupon_rate], 
                                ql.Actual365Fixed()
                                )

            # YTM 계산 (복리)
            ytm_compound = bond_compound.bondYield(current_price, ql.Actual365Fixed(), ql.Compounded, int_pay_cycl)
            
            coupon_schedule_simple = ql.Schedule(maturity_date - ql.Period(2, ql.Years),
                                                maturity_date,
                                                ql.Period(int_pay_cycl),
                                                ql.NullCalendar(),
                                                ql.Unadjusted,
                                                ql.Unadjusted,
                                                ql.DateGeneration.Backward,
                                                False)

            # 단리 채권 생성
            bond_simple = ql.FixedRateBond(2, 
                                face_value, 
                                coupon_schedule_simple, 
                                [coupon_rate], 
                                ql.Actual365Fixed()
                                )

            # 단리 YTM 계산
            ytm_simple = bond_simple.bondYield(current_price, ql.Actual365Fixed(), ql.Simple, int_pay_cycl)

            # 복리와 단리 수익률 고려: 가중 평균
            ytm = (ytm_compound * 5 + ytm_simple * 2) / (5 + 2)
        else: 
            # 만기까지의 기간이 2년 이하일 경우: 단리채만 계산
            coupon_schedule = ql.Schedule(base_date,
                                        maturity_date,
                                        ql.Period(int_pay_cycl),
                                        ql.NullCalendar(),
                                        ql.Unadjusted,
                                        ql.Unadjusted,
                                        ql.DateGeneration.Backward,
                                        False)

            # 단리 채권 생성
            bond_simple = ql.FixedRateBond(2, 
                                face_value, 
                                coupon_schedule, 
                                [coupon_rate], 
                                ql.Actual365Fixed()
                                )

            # 단리 YTM 계산
            ytm = bond_simple.bondYield(current_price, ql.Actual365Fixed(), ql.Simple, int_pay_cycl)
    else: 
        # 단리 or 복리
        
        coupon_schedule = ql.Schedule(base_date,
                                    maturity_date,
                                    ql.Period(int_pay_cycl),
                                    ql.NullCalendar(),
                                    ql.Unadjusted,
                                    ql.Unadjusted,
                                    ql.DateGeneration.Backward,
                                    False)
        
        # 채권 생성
        new_bond = ql.FixedRateBond(2, 
                                    face_value, 
                                    coupon_schedule, 
                                    [coupon_rate], 
                                    ql.Actual365Fixed()
                                    )
        # YTM 계산
        if(bond['irtChngDcdNm'] == '고정-복리'):
            # 복리
            ytm = new_bond.bondYield(current_price, ql.Actual365Fixed(), ql.Compounded, int_pay_cycl)
        else: 
            # 단리
            ytm = new_bond.bondYield(current_price, ql.Actual365Fixed(), ql.Simple, int_pay_cycl)

    calc_data['expectedReturn'] = round(ytm * 100, 2)
    
    # 위험등급
    if(bond['kbpScrsItmsKcdNm'] in ['']):
        calc_data['riskLevel'] = 6
    elif(bond['kbpScrsItmsKcdNm'] in ['AAA', 'AA+', 'AA', 'AA-']):
        calc_data['riskLevel'] = 5
    elif(bond['kbpScrsItmsKcdNm'] in ['A+', 'A', 'A-']):
        calc_data['riskLevel']  = 4
    elif(bond['kbpScrsItmsKcdNm'] in ['BBB+', 'BBB', 'BBB-']):
        calc_data['riskLevel']  = 3
    elif(bond['kbpScrsItmsKcdNm'] in ['BB+', 'BB', 'BB-']):
        calc_data['riskLevel']  = 2
    else:
        calc_data['riskLevel']  = 1
        
    calc_data['amount'] = bond['amount']
    
    return calc_data