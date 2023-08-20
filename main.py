# -*- coding: utf-8 -*-

import os
import sys
import logging
import datetime
import requests
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta

import const
from station import Station


def main():
    dtype: str = set_data_type()

    date: tuple = set_date(dtype)
    start_date: datetime = date[0]
    end_date: datetime = date[1]

    station_list: Station = set_station()

    if not os.path.isdir(const.OUTPUT_DIR_PATH):
        os.mkdir(const.OUTPUT_DIR_PATH)
    os.chdir(const.OUTPUT_DIR_PATH)

    for station_data in station_list:
        output_filename: str = create_output_file(station_data, start_date, end_date, dtype)
        date: datetime = start_date
        while date <= end_date:
            if dtype == const.DATA_TYPE_DAILY:
                print('Parsing: ' + station_data.station_name_en + ' at ' + str(date.year) + '-' + str(date.month), end=' ... ')
            else:
                print('Parsing: ' + station_data.station_name_en + ' at ' + str(date), end=' ... ')
            parse_html(dtype, station_data, date, output_filename)
            print('Finish!')
            if dtype == const.DATA_TYPE_DAILY:
                date += relativedelta(months=1)
            else:
                date += datetime.timedelta(days=1)
    
    os.chdir('..')


def set_data_type():
    """取得するデータの種類（日毎、1時間値、10分値）を取得
    
    Returns
    ------
    dtype : str
        データの種類を示す文字列（'d' or 'h' or '10'）
    """
    print('取得したいデータの種類を入力してください。（日毎 : d, 1時間値 : h, 10分値 : 10）')
    dtype: str = str(input('Input : '))
    if (dtype != const.DATA_TYPE_DAILY and dtype != const.DATA_TYPE_HOUR and dtype != const.DATA_TYPE_10MIN):
        print('データの種類の入力に誤りがあります。')
        sys.exit()
    return dtype


def set_date(dtype: str):
    """データを取得する期間を取得
    
    Parameters
    ------
    dtype : str
        データの種類を示す文字列
    
    Returns
    ------
    start_date : datetime
        取得する期間の開始日
    end_date : datetime
        取得する期間の終了日
    """
    try:
        if dtype == const.DATA_TYPE_DAILY:
            print('開始月を入力してください。（yyyy-mm）')
            input_date: str = str(input('Input : '))
            start_date: datetime = datetime.date(int(input_date.split('-')[0]), \
                int(input_date.split('-')[1]), \
                1)

            print('終了月を入力してください。（yyyy-mm）')
            input_date: str = str(input('Input : '))
            end_date: datetime = datetime.date(int(input_date.split('-')[0]), \
                int(input_date.split('-')[1]), \
                1)
        else:
            print('開始日を入力してください。（yyyy-mm-dd）')
            input_date: str = str(input('Input : '))
            start_date: datetime = datetime.date(int(input_date.split('-')[0]), \
                int(input_date.split('-')[1]), \
                int(input_date.split('-')[2]))

            print('終了日を入力してください。（yyyy-mm-dd）')
            input_date: str = str(input('Input : '))
            end_date: datetime = datetime.date(int(input_date.split('-')[0]), \
                int(input_date.split('-')[1]), \
                int(input_date.split('-')[2]))
        
        if (int(start_date.year) < 1961 or int(end_date.year) < 1961):
            print('1961年以降でなければいけません。')
            sys.exit()
        
        return start_date, end_date
        
    except ValueError:
        print('入力された日付を確認してください。')
        sys.exit()


def set_station():
    """アメダス地点を設定
    
    Returns
    ------
    station_list : list[Station]
        Stationクラスのオブジェクト（アメダス地点の情報）のリスト
    """
    with open(const.STATIONDATA_DAT_PATH, encoding=const.ENCODE_UTF8) as f:
        station_info: list[str] = f.readlines()
    station_info = [line.strip() for line in station_info]
    station_list: list[Station] = []
    print('地点名を入力してください。（prefecture_point）')
    stations: list[str] = list(map(str,input('Input : ').split()))
    for station_name in stations:
        selected_station_info: str = [line for line in station_info if station_name in line][0]
        station_type: str = selected_station_info.split('\t')[2]
        prec_no: str = selected_station_info.split('\t')[3]
        block_no: str = selected_station_info.split('\t')[4]
        station_data = Station(station_name, station_type, prec_no, block_no)
        station_list.append(station_data)
    return station_list


def create_output_file(station_data: Station, start_date: datetime, end_date: datetime, dtype: str):
    """出力するファイルの生成
    
    Parameters
    ------
    station_data : Station
        Stationクラスのオブジェクト（アメダス地点の情報）のリスト
    start_date : datetime
        取得する期間の開始日
    end_date : datetime
        取得する期間の終了日
    dtype : str
        データの種類を示す文字列（'d' or 'h' or '10'）

    Returns
    ------
    filename : str
        出力するファイル名
    """
    if dtype == const.DATA_TYPE_DAILY:
        filename: str = station_data.station_name_en + const.CHAR_UNDERSCORE + str(start_date.year) + (str(start_date.month) if start_date.month > 9 else '0' + str(start_date.month)) + \
            const.CHAR_HYPHEN + str(end_date.year) + (str(end_date.month) if end_date.month > 9 else '0' + str(end_date.month)) + const.CHAR_UNDERSCORE + dtype + const.EXTENSION_CSV
    else:
        filename: str = station_data.station_name_en + const.CHAR_UNDERSCORE + str(start_date.year) + (str(start_date.month) if start_date.month > 9 else '0' + str(start_date.month)) + (str(start_date.day) if start_date.day > 9 else '0' + str(start_date.day)) + \
            const.CHAR_HYPHEN + str(end_date.year) + (str(end_date.month) if end_date.month > 9 else '0' + str(end_date.month)) + (str(end_date.day) if end_date.day > 9 else '0' + str(end_date.day)) + const.CHAR_UNDERSCORE + dtype + const.EXTENSION_CSV
    if os.path.isfile(filename):
        os.remove(filename)
    header: str = None
    if dtype == const.DATA_TYPE_DAILY:
        if station_data.station_type == const.STATION_TYPE_S1:
            header = const.HEADER_DAILY_S1
        else:
            header = const.HEADER_DAILY_A1
    elif dtype == const.DATA_TYPE_HOUR:
        if station_data.station_type == const.STATION_TYPE_S1:
            header = const.HEADER_HOUR_S1
        else:
            header = const.HEADER_HOUR_A1
    else:
        if station_data.station_type == const.STATION_TYPE_S1:
            header = const.HEADER_10MIN_S1
        else:
            header = const.HEADER_10MIN_A1
    with open(filename, 'a', encoding=const.ENCODE_UTF8) as f:
        f.writelines(header)
    return filename


def parse_html(dtype: str, station_data: Station, date: datetime, output_filename: str):
    """観測データが含まれているHTMLファイルを取得・パース・CSVファイルに書き出す
    
    Parameters
    ------
    dtype : str
        データの種類を示す文字列（'d' or 'h' or '10'）
    station_data : Station
        Stationクラスのオブジェクト（アメダス地点の情報）のリスト
    date : datetime
        取得する対象日
    output_filename : str
        観測データを書き込むファイル名
    """
    dtype_url: str = None
    if dtype == const.DATA_TYPE_DAILY:
        dtype_url = const.DATA_TYPE_DAILY_URL
    elif dtype == const.DATA_TYPE_HOUR:
        dtype_url = const.DATA_TYPE_HOUR_URL
    else:
        dtype_url = const.DATA_TYPE_10MIN_URL
    
    url: str = const.URL_DOMAIN + dtype_url + const.CHAR_UNDERSCORE + station_data.station_type + const.URL_PARTS_PHP + \
        const.URL_PARTS_PREC_BLOCK.format(station_data.station_prec_no, station_data.station_block_no) + \
        const.URL_PARTS_DATE.format(str(date.year), str(date.month), str(date.day))

    try:
        res = requests.get(url, timeout=(3.0, 30.0))
    except requests.exceptions.Timeout as e:
        if dtype == const.DATA_TYPE_DAILY:
            print(str(date.year) + '年' + str(date.month) + '月のHTMLファイルの取得でタイムアウトが発生しました。')
            logger.error(e)
        else:
            print(str(date.year) + '年' + str(date.month) + '月' + str(date.day) + '日のHTMLファイルの取得でタイムアウトが発生しました。')
            logger.error(e)

    soup = BeautifulSoup(res.content, 'html.parser')
    rows = soup.find_all(const.HTML_TAG_TR, class_='mtx', style='text-align:right;')
    for row in rows:
        line: str = ''
        if (dtype == const.DATA_TYPE_DAILY):
            line = line + str(date.year) + const.CHAR_COMMA + str(date.month) + const.CHAR_COMMA + str(row.find(const.HTML_TAG_A).contents[0])
        else:
            line = line + str(date.year) + const.CHAR_COMMA + str(date.month) + const.CHAR_COMMA + str(date.day) + const.CHAR_COMMA + \
                str(row.find(const.HTML_TAG_TD, style='white-space:nowrap').contents[0])
        datas = row.find_all(const.HTML_TAG_TD, class_ = 'data_0_0')
        for data in datas:
            if (data.find(const.HTML_TAG_IMG) != None):
                line = line + const.CHAR_COMMA + str(data.find(const.HTML_TAG_IMG).get('alt'))
            else:
                line = line + const.CHAR_COMMA + str(data.contents[0] if len(data) > 0 else '')
        with open(output_filename, 'a', encoding=const.ENCODE_UTF8) as f:
            f.writelines(line + '\n')
        # print(line)


if __name__ == '__main__':
    try:
        logger = logging.getLogger('amedas_downloader')
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('amedas_downloader.log')
        logger.addHandler(handler)
        fmt = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(fmt)

        main()
    
    except KeyboardInterrupt:
        print('\nCtrl + Cコマンドなどでプログラムが終了しました。')
    
    except Exception as e:
        print('予期せぬエラーが発生しました。')
        logger.error(e)