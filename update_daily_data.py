'''
이 스크립트의 목표는 매일 장 마감 이후에 코스피, 코스닥 전 종목의 일봉 데이터를 업데이트 하는 것이다.
그럼 순서는 어떻게 될까?
우선 체크리스트를 연다. 업데이트 날짜가 금일 날짜인지 확인한다.
금일 날짜이면 다음 스텝으로 넘어간다.
체크리스트에서 종목을 훑으면서 각 종목의 금일 데이터를 가져온다.
각 종목마다 csv 파일이 있다. 여기에 새로운 row로 데이터를 저장한다.
업데이트가 끝난 종목은 체크리스트에 데이터 업데이트 날짜를 금일 날짜로 수정한다.
모든 종목에 대해 위의 과정을 반복한다.

'''
import pandas as pd
from pykiwoom.kiwoom import *
from setting import *

def get_theme_info(code, theme_dict):
    for namecode, tickers in theme_dict.items():
        if code in tickers:
            return namecode[:-3], namecode[-3:]
    return (None, None)


kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

state = kiwoom.GetConnectState()
if state == 0:
    print("미연결")
elif state == 1:
    print("연결완료")

account_num = kiwoom.GetLoginInfo("ACCOUNT_CNT")        # 전체 계좌수
accounts = kiwoom.GetLoginInfo("ACCNO")[0]                 # 전체 계좌 리스트
user_id = kiwoom.GetLoginInfo("USER_ID")                # 사용자 ID
user_name = kiwoom.GetLoginInfo("USER_NAME")            # 사용자명
keyboard = kiwoom.GetLoginInfo("KEY_BSECGB")            # 키보드보안 해지여부
firewall = kiwoom.GetLoginInfo("FIREW_SECGB")           # 방화벽 설정 여부

print(f'{user_name}의 {accounts}계좌로 접속')

kospi_code_list = kiwoom.GetCodeListByMarket('0')
kosdaq_code_list = kiwoom.GetCodeListByMarket('10')
# etf = kiwoom.GetCodeListByMarket('8')

group = kiwoom.GetThemeGroupList(1)
temp = {}
for theme_name, theme_code in group.items():
    temp[theme_name +theme_code] = kiwoom.GetThemeGroupCode(theme_code)

lastest_checklist = pd.read_csv(CSV_DAILY_CHECKLIST, index=None, encoding='utf-8')
lastest_checklist.to_csv(CSV_LASTEST_CHECKLIST, encoding='utf-8')


