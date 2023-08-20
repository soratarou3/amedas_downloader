# -*- coding: utf-8 -*-

CHAR_UNDERSCORE: str = '_'
CHAR_HYPHEN: str = '-'
CHAR_COMMA: str = ','

DATA_TYPE_DAILY: str = 'd'
DATA_TYPE_HOUR: str = 'h'
DATA_TYPE_10MIN: str = '10'

DATA_TYPE_DAILY_URL: str = 'daily'
DATA_TYPE_HOUR_URL: str = 'hourly'
DATA_TYPE_10MIN_URL: str = '10min'

STATION_TYPE_S1: str = 's1'
STATION_TYPE_A1: str = 'a1'

STATIONDATA_DAT_PATH: str = './src/stationdata.dat'
OUTPUT_DIR_PATH: str = './outputs'

EXTENSION_CSV = '.csv'

ENCODE_UTF8 = 'utf-8'

HEADER_DAILY_S1: str = 'year,month,day,average site pressure,average sea level pressure,total precipitation,max precipitation 1hour,max precipitation 10min,average temperature,max temperature,min temperature,average humidity,min humidity,average wind speed,max sustained wind speed,max sustained wind direction,max instantaneous wind speed,max instantaneous wind direction,daylight hours,total snowfall,max snowfall ,daytime weather,night weather\n'
HEADER_DAILY_A1: str = 'year,month,day,total precipitation,max precipitation 1hour,max precipitation 10min,average temperature,max temperature,min temperature,average humidity,min humidity,average wind speed,max sustained wind speed,max sustained wind direction,max instantaneous wind speed,max instantaneous wind direction,most wind direction,daylight hours,total snowfall,max snowfall\n'
HEADER_HOUR_S1: str = 'year,month,day,hour,site pressure,sea level pressure,precipitation,temperature,dew-point temperature,vapor pressure,humidity,wind speed,wind direction,daylight hours,global solar radiation,snowfall,snow coverage,weather,cloud amount,visibility\n'
HEADER_HOUR_A1: str = 'year,month,day,hour,precipitation,temperature,dew‐point temperature,vapor pressure,humidity,average wind speed,average wind direction,daylight hours,nowfall,snow coverage\n'
HEADER_10MIN_S1: str = 'year,month,day,time,site pressure,sea level pressure,precipitation,temperature,humidity,average wind speed,average wind direction,max instantaneous wind speed,max instantaneous wind direction,daylight hours\n'
HEADER_10MIN_A1: str = 'year,month,day,time,precipitation,temperature,humidity,average wind speed,average wind direction,max instantaneous wind speed,max instantaneous wind direction,daylight hours\n'

URL_DOMAIN: str = 'https://www.data.jma.go.jp/obd/stats/etrn/view/'
URL_PARTS_PHP: str = '.php?'
URL_PARTS_PREC_BLOCK: str = 'prec_no={0}&block_no={1}'
URL_PARTS_DATE: str = '&year={0}&month={1}&day={2}&view='

HTML_TAG_TR: str = 'tr'
HTML_TAG_A: str = 'a'
HTML_TAG_TD: str = 'td'
HTML_TAG_IMG: str = 'img'