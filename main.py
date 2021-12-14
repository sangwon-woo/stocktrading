from technical_analysis.trend_analysis import *
from config.setting import *





if __name__ == '__main__':
    total_kospi_df = pd.read_feather(ARR_KOSPI_TOTAL_DATA)
    total_kosdaq_df = pd.read_feather(ARR_KOSDAQ_TOTAL_DATA)

    print(total_kospi_df.head())
    print(total_kosdaq_df.head())