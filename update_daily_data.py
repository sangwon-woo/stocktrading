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
import time
import pandas as pd
import numpy as np


from setting import *
from update_checklist import *
from datetime import datetime

def get_stock_trade_data_until_now(kiwoom, code, name, today, STOCK_ITEM_DTYPE, TRADEDATA_DTYPE, next=0):
    
    recent_df = kiwoom.block_request('opt10081', 
                                    종목코드=code, 
                                    기준일자=today, 
                                    수정주가구분=1, 
                                    output='주식일봉차트조회',
                                    next=next)
    recent_df = recent_df.rename(columns=STOCK_ITEM_DTYPE)
    recent_df['날짜'] = pd.to_datetime(recent_df['날짜'])
    recent_df['종목코드'] = code
    recent_df = recent_df[recent_df.columns[:8]]
    recent_df = recent_df[['종목코드', '날짜', '시가', '고가', '저가', '종가', '거래량']]
    recent_df.insert(1, '종목명', name)
    recent_df = recent_df.astype(TRADEDATA_DTYPE)
    
    return recent_df

if __name__ == '__main__':
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

    update_checklist()


    


    today_checklist = pd.read_csv(CSV_DAILY_CHECKLIST, index=None, encoding='utf-8')
    lastest_checklist = pd.read_csv(CSV_LASTEST_CHECKLIST, index=None, encoding='utf-8')


    kospi_code_list_until_now = kiwoom.GetCodeListByMarket('0')
    kosdaq_code_list_until_now = kiwoom.GetCodeListByMarket('10')


    for i, kcwh in enumerate(kospi_code_list_we_have):
        code = kcwh
        name = kiwoom.GetMasterCodeName(code)
        print(f'{name}({code}) => 처리시작', end=' ')
        kcwh_df = pd.read_csv(DIR_KOSPI_DAILY + f'\\{code}.csv', encoding='utf-8', dtype=TRADEDATA_DTYPE, parse_dates=['날짜'])
        
        max_date = kcwh_df['날짜'].max()
        min_date = kcwh_df['날짜'].min()
            
        if max_date == pd.Timestamp(TODAY):
            print(f'오늘 날짜까지 업데이트 완료된 상태')
            continue
        
        if min_date < datetime(2010, 1, 1):
            
            kcwh_df = kcwh_df[kcwh_df['날짜'] > '2010-01-01']
            min_date = kcwh_df['날짜'].min()
        
        print(f"기존 데이터는 {str(min_date)[:10]}부터 {str(max_date)[:10]}까지 존재", end=' ')
        
        if code in kospi_code_list_until_now:
            print(f'현재까지 코스피에서 거래중', end=' ')
        else:
            # 새로운 종목이므로 데이터 프레임을 새로 만들어서 저장해야함
            pass
        
            continue
            
        recent_df = get_stock_trade_data_until_now(code, name, TODAY, STOCK_ITEM_DTYPE, TRADEDATA_DTYPE)
        API_COUNT += 1
        
        lastest_df = recent_df[recent_df['날짜'] > max_date]
        if lastest_df.shape[0]:
            print(f'오늘까지의 데이터에 비해 {lastest_df.shape[0]}일치 부족', end=' ')
            kcwh_df = kcwh_df.append(lastest_df, ignore_index=True).sort_values(by=['날짜'], ascending=False).reset_index(drop=True)
            kcwh_df.to_csv(DIR_KOSPI_DAILY + f'\\{code}.csv', encoding='utf-8', index=None)
            print('업데이트 및 저장 완료', end=' ')
            today_checklist.loc[today_checklist['종목코드'] == code, '일봉관리여부'] = True
            today_checklist.loc[today_checklist['종목코드'] == code, '일봉최종수정일'] = TODAY
            print(f'today_checklist에 업데이트 완료 {i+1}/{kospi_cnt_we_have} ({API_COUNT})')
            
        time.sleep(0.6)

    for i, kcwh in enumerate(kosdaq_code_list_we_have):
        code = kcwh
        name = kiwoom.GetMasterCodeName(code)
        print(f'{name}({code}) => 처리시작', end=' ')
        kcwh_df = pd.read_csv(DIR_KOSDAQ_DAILY + f'\\{code}.csv', encoding='utf-8', dtype=TRADEDATA_DTYPE, parse_dates=['날짜'])
        
        max_date = kcwh_df['날짜'].max()
        min_date = kcwh_df['날짜'].min()
            
        if max_date == pd.Timestamp(TODAY):
            print(f'오늘 날짜까지 업데이트 완료된 상태')
            continue
        
        if min_date < datetime(2010, 1, 1):
            
            kcwh_df = kcwh_df[kcwh_df['날짜'] > '2010-01-01']
            min_date = kcwh_df['날짜'].min()
        
        print(f"기존 데이터는 {str(min_date)[:10]}부터 {str(max_date)[:10]}까지 존재", end=' ')
        
        if code in kosdaq_code_list_until_now:
            print(f'현재까지 코스닥에서 거래중', end=' ')
        else:
            # 새로운 종목이므로 데이터 프레임을 새로 만들어서 저장해야함
            pass
        
            continue
            
        recent_df = get_stock_trade_data_until_now(code, name, TODAY, STOCK_ITEM_DTYPE, TRADEDATA_DTYPE)
        API_COUNT += 1
        
        lastest_df = recent_df[recent_df['날짜'] > max_date]
        if lastest_df.shape[0]:
            print(f'오늘까지의 데이터에 비해 {lastest_df.shape[0]}일치 부족', end=' ')
            kcwh_df = kcwh_df.append(lastest_df, ignore_index=True).sort_values(by=['날짜'], ascending=False).reset_index(drop=True)
            kcwh_df.to_csv(DIR_KOSDAQ_DAILY + f'\\{code}.csv', encoding='utf-8', index=None)
            print('업데이트 및 저장 완료', end=' ')
            today_checklist.loc[today_checklist['종목코드'] == code, '일봉관리여부'] = True
            today_checklist.loc[today_checklist['종목코드'] == code, '일봉최종수정일'] = TODAY
            print(f'today_checklist에 업데이트 완료 {i+1}/{kosdaq_cnt_we_have} ({API_COUNT})')
            
        time.sleep(0.6)