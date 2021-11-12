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
from os import rename
import time
import pandas as pd
import numpy as np
from pykiwoom.kiwoom import *
from setting import *
from datetime import datetime

def get_stock_trade_data_until_now(kiwoom, code, name, today, STOCK_ITEM_DTYPE, TRADEDATA_DTYPE, next=0):
    
    recent_df = kiwoom.block_request('opt10081', 
                                    종목코드=code, 
                                    기준일자=today, 
                                    수정주가구분=1, 
                                    output='주식일봉차트조회',
                                    next=next)
    if not recent_df['종목코드'].any():
        return None
    recent_df = recent_df.rename(columns=STOCK_ITEM_DTYPE)
    recent_df['날짜'] = pd.to_datetime(recent_df['날짜'])
    recent_df['종목코드'] = code
    recent_df = recent_df[recent_df.columns[:8]]
    recent_df = recent_df[['종목코드', '날짜', '시가', '고가', '저가', '종가', '거래량']]
    recent_df.insert(1, '종목명', name)
    recent_df = recent_df.astype(TRADEDATA_DTYPE)
    
    return recent_df

def iter_kospi(kiwoom, today_checklist, kospi_code_list_until_now):
    global API_COUNT

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
            print(f'현재 코스피에서 거래 안됨', end=' ')
            
        recent_df = get_stock_trade_data_until_now(kiwoom,
                                                    code, 
                                                    name, 
                                                    TODAY, 
                                                    STOCK_ITEM_DTYPE, 
                                                    TRADEDATA_DTYPE)
        API_COUNT += 1

        if not recent_df:
            print(f'현재 데이터를 불러올 수 없는 상태')
            continue
        
        compare_df = kcwh_df.loc[ :recent_df.shape[0]-2, :]

        if not recent_df.loc[1:, :].reset_index(drop=True).equals(compare_df):
            print()
            while kiwoom.tr_remained:    
                temp_df = get_stock_trade_data_until_now(kiwoom, 
                                                        code,
                                                        kiwoom.GetMasterCodeName(code), 
                                                        TODAY, 
                                                        STOCK_ITEM_DTYPE, 
                                                        TRADEDATA_DTYPE, 
                                                        next=2)
                API_COUNT += 1

                if temp_df['날짜'].min() < pd.Timestamp('20100101'):
                    temp_df = temp_df[temp_df['날짜'] > pd.Timestamp('20100101')]
                    recent_df = recent_df.append(temp_df, ignore_index=True)
                    break

                recent_df = recent_df.append(temp_df, ignore_index=True)

                print("API_COUNT :", API_COUNT)
                time.sleep(0.6)

            recent_df.to_csv(DIR_KOSPI_DAILY + f'\\{code}.csv', encoding='utf-8', index=None)
            print('업데이트 및 저장 완료', end=' ')

            today_checklist.loc[today_checklist['종목코드'] == code, '일봉관리여부'] = True
            today_checklist.loc[today_checklist['종목코드'] == code, '일봉최종수정일'] = TODAY
            print(f'today_checklist에 업데이트 완료 {i+1}/{kospi_cnt_we_have} ({API_COUNT})')

            continue

        lastest_df = recent_df[recent_df['날짜'] > max_date]

        if lastest_df.shape[0]:
            print(f'오늘까지의 데이터에 비해 {lastest_df.shape[0]}일치 부족', end=' ')

            kcwh_df = (kcwh_df.append(lastest_df, ignore_index=True)
                              .sort_values(by=['날짜'], ascending=False)
                              .reset_index(drop=True))
            kcwh_df.to_csv(DIR_KOSPI_DAILY + f'\\{code}.csv', encoding='utf-8', index=None)
            print('업데이트 및 저장 완료', end=' ')

            today_checklist.loc[today_checklist['종목코드'] == code, '일봉관리여부'] = True
            today_checklist.loc[today_checklist['종목코드'] == code, '일봉최종수정일'] = TODAY
            print(f'today_checklist에 업데이트 완료 {i+1}/{kospi_cnt_we_have} ({API_COUNT})')
            
        time.sleep(0.6)

def iter_kosdaq(kiwoom, today_checklist, kosdaq_code_list_until_now):
    global API_COUNT

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
            print(f'현재 코스닥에서 거래 안됨', end=' ')
            
        recent_df = get_stock_trade_data_until_now(kiwoom,
                                                    code, 
                                                    name, 
                                                    TODAY, 
                                                    STOCK_ITEM_DTYPE, 
                                                    TRADEDATA_DTYPE)
        API_COUNT += 1

        if not recent_df:
            print(f'현재 데이터를 불러올 수 없는 상태')
            continue
        
        compare_df = kcwh_df.loc[ :recent_df.shape[0]-2, :]

        if not recent_df.loc[1:, :].reset_index(drop=True).equals(compare_df):
            while kiwoom.tr_remained:    
                temp_df = get_stock_trade_data_until_now(kiwoom, 
                                                        code,
                                                        kiwoom.GetMasterCodeName(code), 
                                                        TODAY, 
                                                        STOCK_ITEM_DTYPE, 
                                                        TRADEDATA_DTYPE, 
                                                        next=2)
                API_COUNT += 1

                if temp_df['날짜'].min() < pd.Timestamp('20100101'):
                    temp_df = temp_df[temp_df['날짜'] > pd.Timestamp('20100101')]
                    recent_df = recent_df.append(temp_df, ignore_index=True)
                    break

                recent_df = recent_df.append(temp_df, ignore_index=True)

                print("API_COUNT :", API_COUNT)
                time.sleep(0.6)
                
            recent_df.to_csv(DIR_KOSDAQ_DAILY + f'\\{code}.csv', encoding='utf-8', index=None)
            print('업데이트 및 저장 완료', end=' ')

            today_checklist.loc[today_checklist['종목코드'] == code, '일봉관리여부'] = True
            today_checklist.loc[today_checklist['종목코드'] == code, '일봉최종수정일'] = TODAY
            print(f'today_checklist에 업데이트 완료 {i+1}/{kospi_cnt_we_have} ({API_COUNT})')

            continue

        lastest_df = recent_df[recent_df['날짜'] > max_date]

        if lastest_df.shape[0]:
            print(f'오늘까지의 데이터에 비해 {lastest_df.shape[0]}일치 부족', end=' ')

            kcwh_df = (kcwh_df.append(lastest_df, ignore_index=True)
                              .sort_values(by=['날짜'], ascending=False)
                              .reset_index(drop=True))
            kcwh_df.to_csv(DIR_KOSDAQ_DAILY + f'\\{code}.csv', encoding='utf-8', index=None)
            print('업데이트 및 저장 완료', end=' ')

            today_checklist.loc[today_checklist['종목코드'] == code, '일봉관리여부'] = True
            today_checklist.loc[today_checklist['종목코드'] == code, '일봉최종수정일'] = TODAY
            print(f'today_checklist에 업데이트 완료 {i+1}/{kosdaq_cnt_we_have} ({API_COUNT})')
            
        time.sleep(0.6)

def iter_daily_data(kiwoom):

    today_checklist = pd.read_csv(CSV_TODAY_CHECKLIST, encoding='utf-8', dtype=CHECKLIST_DTYPE)


    kospi_code_list_until_now = kiwoom.GetCodeListByMarket('0')
    kosdaq_code_list_until_now = kiwoom.GetCodeListByMarket('10')

    iter_kospi(kiwoom, today_checklist, kospi_code_list_until_now)
    print('코스피 목록 완료')
    iter_kosdaq(kiwoom, today_checklist, kosdaq_code_list_until_now)
    print('코스닥 목록 완료')

    today_checklist.to_csv(CSV_TODAY_CHECKLIST, encoding='utf-8', index=None)
    print('today_checklist 업데이트 완료')






if __name__ == '__main__':
    kiwoom = Kiwoom()
    kiwoom.CommConnect(block=True)

    state = kiwoom.GetConnectState()
    if state == 0:
        print("미연결")
    elif state == 1:
        print("연결완료")

    iter_daily_data(kiwoom)


