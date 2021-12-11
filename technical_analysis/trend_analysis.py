import time
import pandas as pd
from config.setting import *
import multiprocessing as mp

def get_trend_analysis(df, days):
    
    df = df.sort_values(by=['날짜']).reset_index(drop=True)
    df.reset_index(inplace=True)
    df['index'] += 1
    
    df['평균매매가'] = (df[['시가', '종가']].sum(axis=1) / 2 + df[['시가', '종가', '저가', '고가']].sum(axis=1))/5
    standard_price = df.loc[0, '평균매매가']

    df['변환주가'] = (df['평균매매가'] / standard_price * 10000)
    max_price = df['변환주가'].max()                                                      # P2
    min_price = df['변환주가'].min()                                                      # P3
    xi = df.loc[df['변환주가'] == max_price, 'index'].values[0]
    ni = df.loc[df['변환주가'] == min_price, 'index'].values[0]
    max_index = 1 if df.loc[0, '변환주가'] == max_price else xi                          # L2
    min_index = 1 if df.loc[0, '변환주가'] == min_price else ni                          # M2
    first_price = 10000                                                                  # T2
    last_price = df['변환주가'].values[-1]                                                # T3

    X_of_open_close = (last_price - first_price) / days                                  # T12 = (T3-T2) / N3
    intercept_of_open_close = 10000                                                       # V12

    X_of_high_low = (max_price - min_price) / (max_index - min_index)                     # T16 = (P2-P3) / (L2-M2)
    intercept_of_high_low = max_price - (max_index * X_of_high_low)                       # V16 = P2 - (L2*T16)

    _1 = (1 + X_of_open_close ** 2) ** (1 / 2)                                            # W13
    _2 = (1 + X_of_high_low ** 2) ** (1 / 2)                                              # W17
    _3 = _1 / _2                                                                          # W15
    _4 = first_price - intercept_of_high_low                                              # U23 = T2 - V16
    _5 = X_of_high_low - X_of_open_close                                                  # S23 = T16 - T12
    _6 = _4 / _5                                                                          # T24 = U23 / S23
    _7 = X_of_high_low * _6 + intercept_of_high_low                                       # U24

    X_of_cross_line = (X_of_open_close + (X_of_high_low * _3)) / (1 + _3)                 # T22
    intercept_of_cross_line = _7 - (_6 * X_of_cross_line)                                 # V22 = U24 - (T24*T22)
    Y_of_cross_line = lambda x: X_of_cross_line * x + intercept_of_cross_line



    x_axis_one_scale = (max_price - min_price) / (days -1) # AI10
    x_data_count = days -1 # AI11
    max_min_height = max_price - min_price # AI12
    best_trend_energy = x_data_count * max_min_height / 2 # AI13
    open_close_trend_energy = (last_price - first_price) * x_data_count / 2 # AI14
    high_low_trend_energy = max_min_height * (max_index - min_index) / 2 # AI15
    open_close_trend_energy_pct = open_close_trend_energy / best_trend_energy * 100# AJ14
    high_low_trend_energy_pct = high_low_trend_energy / best_trend_energy * 100# AJ15
    up_trend_power = (open_close_trend_energy_pct + high_low_trend_energy_pct) / 2 # T7


    df['시종에너지'] = open_close_trend_energy / 10000
    df['고저에너지'] = high_low_trend_energy / 10000
    df['에너지소계'] = df['시종에너지'] + df['고저에너지']
    cross_line_gap = (df['변환주가'] - (df['index'].apply(Y_of_cross_line))).abs()
    df['중심선괴리합'] = cross_line_gap.sum()
    df['중심선괴리평균'] = cross_line_gap.mean()
    df['괴리도'] = cross_line_gap.mean() / ((first_price + last_price) / 2) * 100
    df['기간상승/하락률'] = ((last_price / first_price) - 1) *100
    df['상승추세강도'] = up_trend_power
    df['타임스팬'] = days
    
    return df.iloc[-1, [1, 2, 19, 15, 17, 18]]

def get_total_df(market):

    code_list = kospi_code_list_we_have if market == 'kospi' else kosdaq_code_list_we_have
    code_dir = DIR_KOSPI_DAILY if market == 'kospi' else DIR_KOSDAQ_DAILY
    code_cnt = kospi_cnt_we_have if market == 'kospi' else kosdaq_cnt_we_have
    total_df = pd.DataFrame()

    for i, code in enumerate(code_list):
        df = pd.read_csv(code_dir + f'\\{code}.csv', encoding='utf-8', dtype=TRADEDATA_DTYPE)
        total_df = total_df.append(df, ignore_index=True)
        
        print(f'{i+1} / {code_cnt}')
    
    total_df['날짜'] = pd.to_datetime(total_df['날짜'])
    total_df['종목코드'] = total_df['종목코드'].astype('category')
    total_df['종목명'] = total_df['종목명'].astype('category')
    total_df = total_df.sort_values(by=['종목코드', '날짜'], ascending=[True, False]).reset_index(drop=True)

    total_df.to_feather(PWD + f'\\data\\total_{market}_data_{TODAY}.arrx')

    return total_df

def append_trend_analysis(total_df, market):
    
    save_dir = CSV_KOSPI_TREND_ANALYSIS if market == 'kospi' else CSV_KOSDAQ_TREND_ANALYSIS
    
    trend_df = pd.DataFrame()

    for code in total_df['종목코드'].unique():
        print(f'{code} 시작', end=' ')
        code_df = total_df[total_df['종목코드'] == code].reset_index(drop=True)
        max_date = code_df['날짜'].max()
        min_date = code_df['날짜'].min()
        nrows = code_df.shape[0]
        
        return_df = pd.DataFrame()
        
        for days in range(10, 121):
            if nrows < days:
                print(f'총 데이터 수가 {days}일 보다 적음, {code} 분석 종료', end=' ')
                break
                
            temp_df = code_df.loc[:days-1, :]
            if temp_df[temp_df['거래량'] == 0].shape[0]:
                print(f'{days}일 내에 거래량이 없는 종목이라서 {code} 분석 종료', end=' ')
                break
                
            tdf = get_trend_analysis(temp_df, days)
            return_df = return_df.append(tdf)
        trend_df = trend_df.append(return_df, ignore_index=True)
        
        print(f'{code} 완료')

    trend_df.to_csv(save_dir, encoding='utf-8', index=None)

    print(f'{TODAY} 기준 {market} 추세 분석 완료')
    time.sleep(2)

def run_trend_analysis():
    
    total_kospi_df = get_total_df('kospi') if not os.path.isfile(ARR_KOSPI_TOTAL_DATA) else pd.read_feather(ARR_KOSPI_TOTAL_DATA)
    with mp.Pool(os.cpu_count()) as p:
        append_trend_analysis(total_kospi_df, 'kospi')

    total_kosdaq_df = get_total_df('kosdaq') if not os.path.isfile(ARR_KOSDAQ_TOTAL_DATA) else pd.read_feather(ARR_KOSDAQ_TOTAL_DATA)
    append_trend_analysis(total_kosdaq_df, 'kosdaq')
