from pykiwoom.kiwoom import *
import time
import pandas as pd


kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)
state = kiwoom.GetConnectState()
if state == 0:
    print("미연결")
elif state == 1:
    print("연결완료")
account_num = kiwoom.GetLoginInfo("ACCOUNT_CNT")        # 전체 계좌수
accounts = kiwoom.GetLoginInfo("ACCNO")                 # 전체 계좌 리스트
user_id = kiwoom.GetLoginInfo("USER_ID")                # 사용자 ID
user_name = kiwoom.GetLoginInfo("USER_NAME")            # 사용자명
keyboard = kiwoom.GetLoginInfo("KEY_BSECGB")            # 키보드보안 해지여부
firewall = kiwoom.GetLoginInfo("FIREW_SECGB")           # 방화벽 설정 여부

# print("전체 계좌수:", account_num)
# print("전체 계좌 리스트:", accounts)
# print("사용자 ID:", user_id)
# print("사용자명:", user_name)
# print("키보드보안 해지 여부:", keyboard)
# print("방화벽 설정 여부:", firewall)

kospi = kiwoom.GetCodeListByMarket('0')
kosdaq = kiwoom.GetCodeListByMarket('10')
etf = kiwoom.GetCodeListByMarket('8')

print("코스피 종목 수:", len(kospi))
print("코스닥 종목 수:", len(kosdaq))
print("ETF 종목 수:", len(etf))

kospi_name, kosdaq_name, etf_name = [], [], []

for _kospi in kospi:
    kospi_name.append(kiwoom.GetMasterCodeName(_kospi))
for _kosdaq in kosdaq:
    kosdaq_name.append(kiwoom.GetMasterCodeName(_kosdaq))
for _etf in etf:
    etf_name.append(kiwoom.GetMasterCodeName(_etf))

# print(kospi_name)
# print(kosdaq_name)
# print(etf_name)

# TR 요청 (연속조회)
dfs = []
df = kiwoom.block_request("opt10080",
                          종목코드="005930",
                          틱범위="1",
                          수정주가구분=1,
                          output="주식분봉차트조회",
                          next=0)
# df.to_csv('1분봉.csv', index=None)
df.to_excel('1분봉.xlsx', index=None)
# dfs.append(df)

# # while kiwoom.tr_remained:
# #     df = kiwoom.block_request("opt10081",
# #                               종목코드="005930",
# #                               틱범위="1",
# #                               수정주가구분=1,
# #                               output="주식분봉차트조회",
# #                               next=2)
# #     dfs.append(df)
# #     time.sleep(1)

# # df = pd.concat(dfs)
# # df.to_excel("005930.xlsx")