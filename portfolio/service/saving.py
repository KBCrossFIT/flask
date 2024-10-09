import pandas as pd

# saving = {
#     'rsrvType': 'F', # 예금/적금 구분
#     'saveTerm': 12, # 만기
#     'intrType': "복리", # 단리/복리
#     'intrRate': 3.50, # 금리(최저, 최대는 프론트에서 선택)
#     'amount': 1000000, # 예금의 경우 총액, 적금의 경우 월 납입액
# }

def calculate_saving(saving):
    calc_data = {
        'expectedReturn': 0,
        'riskLevel': 6, 
        'amount': 0
    }
    
    calc_data['amount'] = saving['amount']
    
    if saving['intrType'] == '단리':
        expected_return = saving['intrRate'] * (saving['saveTerm'] / 12)
    else:
        if saving['rsrvType'] == '':  # 예금
            expected_return = ((1 + saving['intrRate'] / 100 / 12) ** (saving['saveTerm']) - 1) * 100
        else:  # 적금
            total_amount = 0
            for i in range(saving['saveTerm']):
                total_amount += saving['amount'] * (1 + saving['intrRate'] / 100 / 12) ** ((saving['saveTerm']) - i)
                expected_return = (total_amount - (saving['amount'] * saving['saveTerm'])) / (saving['amount'] * saving['saveTerm']) * 100
                
    calc_data['expectedReturn'] = round(expected_return, 2)
    
    return calc_data
    
# print(calculate_saving(saving))