# fund = {
#     "yield1": 8.85, # 1개월 수익률
#     "yield3": 6.70, # 3개월 수익률
#     'yield6': 0.78, # 6개월 수익률
#     'yield12': -3.45, # 12개월 수익률
#     'riskLevel': 1, # 위험등급
#     'advancedFee': 1.00, # 선취 수수료
#     'totalPayoffRate': 1.56, # 총 보수
#     'amount': 1000000 # 투자금액
# }

def calculate_fund(fund):
    calc_data = {
        'expectedReturn': 0,
        'riskLevel': 0, 
        'amount': 0
    }
    
    # 수익률 계산
    if fund['yield12'] is not None:
        calc_data['expectedReturn'] = fund['yield12'] - fund['advancedFee'] - fund['totalPayoffRate']
    elif fund['yield6'] is not None:
        calc_data['expectedReturn'] = fund['yield6'] - fund['advancedFee'] - fund['totalPayoffRate']
    elif fund['yield3'] is not None:
        calc_data['expectedReturn'] = fund['yield3'] - fund['advancedFee'] - fund['totalPayoffRate']
    else:
        calc_data['expectedReturn'] = fund['yield1'] - fund['advancedFee'] - fund['totalPayoffRate']

    # 위험도 저장
    calc_data['riskLevel'] = fund['riskLevel'] 

    calc_data['amount'] = fund['amount']

    return calc_data

# print(calculate_fund(fund))
