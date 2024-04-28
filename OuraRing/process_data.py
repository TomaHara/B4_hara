import pandas as pd
from pathlib import Path

def add_username(path):  #フォルダ内のcsvファイルに"user"列を追加
    file_list = Path(path).glob('*.csv')
    for row in file_list:
        df = pd.read_csv(row)
        if 'user' in df.columns:
            pass
        else:
            username = row.stem[-3:]
            df['user'] = username
            df.to_csv(row, index=False)

def combine_all_data(path_from, path_to):  #フォルダ内のcsvファイルを結合
    file_list = Path(path_from).glob('*.csv')
    df_list = []
    for row in file_list:
        df = pd.read_csv(row)
        if df.shape[0] == 0:
            pass
        else:
            df_list.append(pd.read_csv(row))
    combined_df = pd.concat(df_list, ignore_index=True)
    combined_df.to_csv(path_to + r"\all_sleep_data.csv")

def datetime(df): #'bedtime_start'と'bedtime_end'を'%Y-%m-%d %H:%M:%S'の型に合わす
    df['bedtime_start'] = pd.to_datetime(df['bedtime_start'], utc=True).dt.tz_convert('Asia/Tokyo')
    df['bedtime_end'] = pd.to_datetime(df['bedtime_end'], utc=True).dt.tz_convert('Asia/Tokyo')
    df['bedtime_start'] = df['bedtime_start'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df['bedtime_end'] = df['bedtime_end'].dt.strftime('%Y-%m-%d %H:%M:%S')

def select_period(df,start_date,end_date): #指定した期間のデータを抽出(start_date,end_dateはdatetime(%y,%m,%d))
    df['day'] = pd.to_datetime(df['day'])
    filtered_df = df[(df['day']>start_date) & (df['day']<end_date)]
    return filtered_df

if __name__ == "__main__":
    file_list = Path("~~~~~~~~~~~~~~~~~~~~~").glob('*.csv')
    for row in file_list:
        df = pd.read_csv(row)
        datetime(df)
        df.to_csv(row, index=False)
    add_username("~~~~~~~~~~~~~~")
    combine_all_data("~~~~~~~~~~")

