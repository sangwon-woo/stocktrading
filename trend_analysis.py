'''
이 스크립트의 목적은 코스피, 코스닥 전체 종목의 추세 분석을 돌려보는 것이다.
추세 분석은 고문님의 알고리즘을 따른다.
근데 문제는 타임프레임을 정하는 것이다. 
나한테는 아직 단기, 중기, 장기를 가르는 기준이 없다.
타임프레임이 3개면 될까?
아니면 더 해야할까. 
그래도 적어도 3개월 이상을 볼까?
아니면 1개월부터 볼까. 잘 모르겠다. 
요즘 시장은 2주
'''

import pandas as pd
from setting import *

def get_no_volume_list(days):
    no_volume_list = []
    for code in kosdaq_code_list_we_have:
        df = pd.read_csv(DIR_KOSDAQ_DAILY + f'\\{code}.csv', dtype=TRADEDATA_DTYPE, encoding='utf-8', parse_dates=['날짜'])
        tdf = df.loc[:days-1, :]
        zero_volume_days = tdf[tdf['거래량'] == 0].shape[0]
        if zero_volume_days:
            no_volume_list.append(code)

    return no_volume_list

def trend_analysis(timespan, code):
    nrows = timespan
    if code in kospi_code_list_we_have:
        
        df = pd.read_csv(DIR_KOSPI_DAILY + f'\\{code}.csv', 
                         encoding='utf-8', 
                         dtype=TRADEDATA_DTYPE, 
                         parse_dates=['날짜'])
    else:
        df = pd.read_csv(DIR_KOSDAQ_DAILY + f'\\{code}.csv', 
                         encoding='utf-8', 
                         dtype=TRADEDATA_DTYPE, 
                         parse_dates=['날짜'])
    if df.shape[0] < nrows:
        return None
    
    if not df.loc[0, '거래량']:
        return None
    
    df = df.iloc[:nrows-1, :]
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

    X_of_open_close = (last_price - first_price) / nrows                                  # T12 = (T3-T2) / N3
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



    x_axis_one_scale = (max_price - min_price) / (nrows -1) # AI10
    x_data_count = nrows -1 # AI11
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
    
    return df.iloc[-1, [1, 2, 15, 17, 18]]

def run_trend_analysis():
    total_df = pd.DataFrame()
    for days in range(10, 121):
        no_volume_list = get_no_volume_list(days)
        tdf = pd.DataFrame()
        for code in kosdaq_code_list_we_have:
            if code in no_volume_list: continue
            tdf = tdf.append(trend_analysis(days, code))
        total_df = total_df.append(tdf)
        print(f'{days} 완료')

    total_df.to_csv(CSV_TODAY_TREND_ANALYSIS, encoding='utf-8', index=None)