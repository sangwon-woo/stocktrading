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
from pykiwoom.kiwoom import *
from setting import *
from update_daily_data import get_stock_trade_data_until_now


def init_checklist(kospi, kosdaq):
    today_checklist = {
        '시장명':[], 
        '종목명':[], 
        '종목코드':[], 
        '감리구분':[], 
        '상장일자':[], 
        '종목상태':[], 
        '체크최종수정일':[]
    }




    for code in kospi:
        
        today_checklist['시장명'].append('kospi')
        today_checklist['종목명'].append(kiwoom.GetMasterCodeName(code))
        today_checklist['종목코드'].append(code)
        today_checklist['감리구분'].append(kiwoom.GetMasterConstruction(code))
        today_checklist['상장일자'].append(kiwoom.GetMasterListedStockDate(code))
        today_checklist['종목상태'].append(kiwoom.GetMasterStockState(code))
        today_checklist['체크최종수정일'].append(TODAY)
        
    for code in kosdaq:
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

    return today_checklist

def iter_checklist(today_checklist):

    for code in total_code_list_we_have:

        if code in kospi_code_list_we_have:
            stock_df = pd.read_csv(DIR_KOSPI_DAILY + f'\\{code}.csv', encoding='utf-8', dtype=TRADEDATA_DTYPE, parse_dates=['날짜'])
            min_date = stock_df['날짜'].min().strftime('%Y%m%d')
            max_date = stock_df['날짜'].max().strftime('%Y%m%d')
            today_checklist.loc[today_checklist['종목코드'] == code, '일봉관리여부'] = True
            today_checklist.loc[today_checklist['종목코드'] == code, '일봉최종수정일'] = TODAY
            today_checklist.loc[today_checklist['종목코드'] == code, '일봉최초날짜'] = min_date
            today_checklist.loc[today_checklist['종목코드'] == code, '일봉최근날짜'] = max_date

            print(f'{code}완료', end=' ')
        else:
            stock_df = pd.read_csv(DIR_KOSDAQ_DAILY + f'\\{code}.csv', encoding='utf-8', dtype=TRADEDATA_DTYPE, parse_dates=['날짜'])
            min_date = stock_df['날짜'].min().strftime('%Y%m%d')
            max_date = stock_df['날짜'].max().strftime('%Y%m%d')
            today_checklist.loc[today_checklist['종목코드'] == code, '일봉관리여부'] = True
            today_checklist.loc[today_checklist['종목코드'] == code, '일봉최종수정일'] = TODAY
            today_checklist.loc[today_checklist['종목코드'] == code, '일봉최초날짜'] = min_date
            today_checklist.loc[today_checklist['종목코드'] == code, '일봉최근날짜'] = max_date

            print(f'{code}완료', end=' ')

    return today_checklist

def save_new_stock_data(not_tracked_list):
    global API_COUNT

    for code in not_tracked_list['종목코드'].values:

        first_df = get_stock_trade_data_until_now(code, 
                                                    kiwoom.GetMasterCodeName(code), 
                                                    TODAY, STOCK_ITEM_DTYPE, 
                                                    TRADEDATA_DTYPE)
        API_COUNT += 1
        market = not_tracked_list[not_tracked_list['종목코드'] == code].values[0][0]

        while kiwoom.tr_remained:

            temp_df = get_stock_trade_data_until_now(code, 
                                                    kiwoom.GetMasterCodeName(code), 
                                                    TODAY, 
                                                    STOCK_ITEM_DTYPE, 
                                                    TRADEDATA_DTYPE, 
                                                    next=2)
            API_COUNT += 1

            if temp_df['날짜'].min() < pd.Timestamp('20100101'):
                temp_df = temp_df[temp_df['날짜'] > pd.Timestamp('20100101')]
                first_df = first_df.append(temp_df, ignore_index=True)
                break

            first_df = first_df.append(temp_df, ignore_index=True)

            print("API_COUNT :", API_COUNT)
            time.sleep(0.6)
        else:
            print("API_COUNT :", API_COUNT)
            time.sleep(0.6)

        if market == 'kospi':
            first_df.to_csv(DIR_KOSPI_DAILY + f'\\{code}.csv', encoding='utf-8', index=None)
        else:
            first_df.to_csv(DIR_KOSDAQ_DAILY + f'\\{code}.csv', encoding='utf-8', index=None)

    return


def update_checklist():
    lastest_checklist = pd.read_csv(CSV_DAILY_CHECKLIST, 
                                    encoding='utf-8', 
                                    dtype=CHECKLIST_DTYPE)

    today_checklist = init_checklist()
    today_checklist = iter_checklist(today_checklist)

    not_tracked_list = today_checklist[today_checklist['일봉관리여부'] == False]

    if not_tracked_list.shape[0]:
        save_new_stock_data(not_tracked_list)
    else:
        if lastest_checklist.equals(today_checklist):
            print('어제와 오늘의 today_checklist가 같음.')

    lastest_checklist.to_csv(CSV_LASTEST_CHECKLIST, index=None, encoding='utf-8')
    today_checklist.to_csv(CSV_DAILY_CHECKLIST, index=None, encoding='utf-8')








if __name__ == '__main__':
    kiwoom = Kiwoom()
    kiwoom.CommConnect(block=True)

    state = kiwoom.GetConnectState()
    if state == 0:
        print("미연결")
    elif state == 1:
        print("연결완료")

    update_checklist()

    