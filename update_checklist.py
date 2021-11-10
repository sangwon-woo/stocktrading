'''
이 스크립트의 목표는 매일 장 마감 이후 체크리스트를 업데이트 하는 것이다.
그럼 순서는 어떻게 될까?
우선 체크리스트를 연다. 
코스피, 코스닥 종목과 관련 정보를 키움 증권 api를 통해 받아온다. 
기존 체크리스트에서 달라진 것이 어디에 있는지 확인한다. 
달라진 것은 따로 문서를 만들어서 관리한다.
안 달라진 것은 최종 수정일만 당일 날짜로 업데이트 한다. 
그리고 다시 저장한다. 
'''

import pandas as pd
import os
from pykiwoom.kiwoom import *
from setting import *


kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

state = kiwoom.GetConnectState()
if state == 0:
    print("미연결")
elif state == 1:
    print("연결완료")
    
lastest_checklist = pd.read_csv(CSV_DAILY_CHECKLIST, 
                                encoding='utf-8', 
                                dtype=CHECKLIST_DTYPE)

today_checklist = {
    '시장명':[], 
    '종목명':[], 
    '종목코드':[], 
    '감리구분':[], 
    '상장일자':[], 
    '종목상태':[], 
    '체크최종수정일':[]
}

kospi_code_list_until_now = kiwoom.GetCodeListByMarket('0')
kosdaq_code_list_until_now = kiwoom.GetCodeListByMarket('10')


for code in kospi_code_list_until_now:
    
    today_checklist['시장명'].append('kospi')
    today_checklist['종목명'].append(kiwoom.GetMasterCodeName(code))
    today_checklist['종목코드'].append(code)
    today_checklist['감리구분'].append(kiwoom.GetMasterConstruction(code))
    today_checklist['상장일자'].append(kiwoom.GetMasterListedStockDate(code))
    today_checklist['종목상태'].append(kiwoom.GetMasterStockState(code))
    today_checklist['체크최종수정일'].append(TODAY)
    
for code in kosdaq_code_list_until_now:
    today_checklist['시장명'].append('kosdaq')
    today_checklist['종목명'].append(kiwoom.GetMasterCodeName(code))
    today_checklist['종목코드'].append(code)
    today_checklist['감리구분'].append(kiwoom.GetMasterConstruction(code))
    today_checklist['상장일자'].append(kiwoom.GetMasterListedStockDate(code))
    today_checklist['종목상태'].append(kiwoom.GetMasterStockState(code))
    today_checklist['체크최종수정일'].append(TODAY)
    
today_checklist = pd.DataFrame(today_checklist)
today_checklist = today_checklist.assign(일봉관리여부=False)
today_checklist = today_checklist.assign(일봉최종수정일=0)
today_checklist = today_checklist.assign(일봉최초날짜=0)
today_checklist = today_checklist.assign(일봉최근날짜=0)
today_checklist = today_checklist.assign(분봉관리여부=False)
today_checklist = today_checklist.assign(분봉최종수정일=0)

kospi_code_list_we_have = [i[:-4] for i in os.listdir(DIR_KOSPI_DAILY) if i.endswith('.csv')]
kosdaq_code_list_we_have = [i[:-4] for i in os.listdir(DIR_KOSDAQ_DAILY) if i.endswith('.csv')]
total_code_list_we_have = set(kospi_code_list_we_have) | set(kosdaq_code_list_we_have)