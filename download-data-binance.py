import sys
import os
import requests
import pandas as pd
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pytz

logfile = open("log.txt", "a")

def create_folder(folder_name):
    try:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f"Created folder: {folder_name}")
        else:
            print(f"Folder already exists: {folder_name}")
    except Exception as e:
        print(f"Error creating folder '{folder_name}': {str(e)}")

def getTransaction(symbol, from_id, folder_name, end_date):
    api_key = 'gNOSJuPCNQ8LTYGmauQtBa2EyujjPsnHRrpVfmQcGkZzi02GOPndqHgGGSLeREhr'
    batch_size = 1000  # Set a larger batch size
    curId = from_id
    received_transactions = 0

    create_folder(folder_name)

    file_name = f"{folder_name}/transactions.csv"

    if os.path.isfile(file_name):
        existing_data = pd.read_csv(file_name)

        if 'time' in existing_data.columns:
            max_timestamp = existing_data.iloc[-1]["time"]
            curId = int(existing_data.iloc[-1]["id"]) + 1

            if (max_timestamp // 1000) >= end_date:
                print(f"The data for {symbol} is already up-to-date.")
        openfile = open(file_name, 'a')
    else:
        openfile = open(file_name, 'w')
        openfile.write("id,price,qty,quoteQty,time,isBuyerMaker,isBestMatch\n")

    end_date = datetime.utcfromtimestamp(end_date // 1000).replace(tzinfo=pytz.timezone('America/Chicago'))

    while True:
        print("Getting from id =", curId)
        url = 'https://api.binance.us/api/v3/historicalTrades'
        params = {
            'symbol': symbol,
            'fromId': curId,
            'limit': batch_size
        }
        headers = {
            'X-MBX-APIKEY': api_key
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            if not data:
                print("exiting getTransaction(): not data")
                break

            df = pd.DataFrame(data, columns=['id', 'price', 'qty', 'quoteQty', 'time', 'isBuyerMaker', 'isBestMatch'])

            df.to_csv(openfile, mode='a', header=False, index=False)

            curId = df.iloc[-1]["id"] + 1
            received_transactions += len(df)

            latest_transaction = df.iloc[-1]["time"]
            if datetime.utcfromtimestamp(latest_transaction // 1000).replace(tzinfo=pytz.timezone('America/Chicago')) >= end_date:
                print("exiting getTransaction(): time exceeded ", latest_transaction, end_date)
                break

        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 429:
                print('Too Many Requests. Sleeping for 15 seconds...')
                time.sleep(15)
            else:
                raise

        except Exception as e:
            print('An error occurred:', str(e))
            time.sleep(15)  # Sleep for 15 seconds after encountering an error

    openfile.close()
    print(f'Finished reading {received_transactions} trades for {symbol}')

def candlesamplePlotter(symbol, end_date):
    try:
        file_name = f"{symbol}/transactions.csv"
        data = pd.read_csv(file_name)

        if 'time' in data.columns:
            data['time'] = pd.to_datetime(data['time'], unit='ms')

            periods = ['s', 'Min', 'h', 'D', 'W', 'ME', 'YE']
            #periods = ['S', 'T', 'H', 'D', 'W', 'M', 'A']
            for period in periods:
                ohlc_data = data.groupby(pd.Grouper(key='time', freq=period)).agg({'price': ['first', 'last', 'max', 'min'], 'qty': 'sum'}).reset_index()
                ohlc_data.columns = ['timestamp', 'open', 'close', 'high', 'low', 'volume']

                file_path = f"{symbol}/candlesticks-{period}.csv"
                ohlc_data.to_csv(file_path, index=False, date_format='%s', na_rep='NaN')

                ohlc_data['range'] = ohlc_data['high'] - ohlc_data['low']
                no_profit_count = (ohlc_data['range'] == 0).sum()
                maximum_profit = ohlc_data['range'].sum()
                logfile.write(symbol + " " + period + " " + str(maximum_profit) + " " + str(no_profit_count)+"\n")

                if period == 'h' or period == 'D' or period == 'W' or period == 'ME' or period == 'YE' :
                    ohlc_data.set_index('timestamp', inplace=True)
                    df = ohlc_data
                    myTitle = f"{symbol} Candle Stick Graph (Monthly)"

                    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05)

                    fig.add_trace(go.Candlestick(x=df.index,
                                                 open=df['open'],
                                                 high=df['high'],
                                                 low=df['low'],
                                                 close=df['close'],
                                                 name='candlestick'),
                                  row=1, col=1)

                    fig.add_trace(go.Bar(x=df.index,
                                         y=df['volume'],
                                         name='Volume'),
                                  row=2, col=1)

                    fig.update_layout(title=myTitle,
                                      xaxis=dict(title='Date', rangeslider=dict(visible=True), type='date'),
                                      yaxis=dict(title='Price'),
                                      showlegend=False)

                    fig.write_html(f"{symbol}/candlesticks-{period}-plot.html")

        else:
            print("Error: 'time' column not found in the DataFrame.")
    except FileNotFoundError:
        print(f"Error: '{file_name}' file not found.")

def getHistoricalData():
    #symbols = [
    #    '1INCHUSDT',
    #    'AAVEUSDT',
    #    'ACHUSDT',
    #    'ADAUSDT',
    #    'ALGOUSDT'
    #]
    
    symbols = [
    #downloaded fine
    '1INCHUSDT', 'AAVEUSDT', 'ACHUSDT', 'ADAUSDT', 'ALGOUSDT', 'ALICEUSDT', 'ALPINEUSDT', 'ANKRUSDT', 'ANTUSDT', 'APEUSDT', 'API3USDT', 'APTUSDT', 'ARBUSDT', 'ASTRUSDT', 'ATOMUSDT', 'AUDIOUSDT', 'AVAXUSDT', 'AXLUSDT', 'AXSUSDT', 'BALUSDT', 'BANDUSDT', 'BATUSDT', 'BCHUSDT', 'BICOUSDT', 'BLURUSDT', 'BNBUSDT', 'BNTUSDT', 'BONDUSDT', 'BOSONUSDT', 'BTCUSDT', 'BTRSTUSDT', 'CELOUSDT', 'CELRUSDT', 'CHZUSDT', 'CLVUSDT', 'COMPUSDT', 'COTIUSDT', 'CRVUSDT', 'CTSIUSDT', 'DAIUSDT', 'DARUSDT', 'DASHUSDT', 'DGBUSDT','DIAUSDT', 'DOGEUSDT', 'DOTUSDT', 'EGLDUSDT', 'ENJUSDT', 'ENSUSDT', 'EOSUSDT', 'ETCUSDT', 'ETHUSDT', 'FETUSDT', 'FILUSDT', 'FLOKIUSDT', 'FLOWUSDT', 'FLUXUSDT', 'FORTHUSDT', 'FTMUSDT', 'GALUSDT', 'GALAUSDT', 'GLMUSDT', 'GRTUSDT', 'GTCUSDT', 'HBARUSDT', 'ICPUSDT', 'ICXUSDT', 'ILVUSDT', 'IMXUSDT', 'IOSTUSDT', 'IOTAUSDT', 'JAMUSDT', 'KAVAUSDT', 'KDAUSDT', 'KNCUSDT', 'KSMUSDT', 
    #failed to download: requests.exceptions.HTTPError: 400 Client Error: Bad Request for url: https://api.binance.us/api/v3/historicalTrades?symbol=LAZIUSDT&fromId=0&limit=1000
    #'LAZIUSDT', 
    'LDOUSDT', 'LINKUSDT', 'LOKAUSDT','LOOMUSDT', 'LPTUSDT', 'LRCUSDT', 'LSKUSDT', 'LTCUSDT', 'LTOUSDT', 'MANAUSDT', 'MASKUSDT', 'MATICUSDT', 'MKRUSDT', 'MXCUSDT', 'NEARUSDT', 'NEOUSDT', 'NMRUSDT', 'OCEANUSDT', 'OGNUSDT', 'OMGUSDT', 'ONEUSDT', 'ONTUSDT', 'OPUSDT', 'OXTUSDT', 'PAXGUSDT', 'POLYXUSDT', 'PONDUSDT', 'PORTOUSDT', 'PROMUSDT', 'QNTUSDT', 'QTUMUSDT', 'RADUSDT', 'RAREUSDT', 'REEFUSDT', 'RENUSDT', 'REQUSDT', 'RLCUSDT', 'RNDRUSDT', 'ROSEUSDT', 'RVNUSDT', 'SANDUSDT', 'SANTOSUSDT', 'SHIBUSDT','SKLUSDT', 'SLPUSDT', 'SNXUSDT', 'SOLUSDT', 'STGUSDT', 'STORJUSDT', 'SUSHIUSDT', 'SYSUSDT', 'TUSDT', 'THETAUSDT', 'TLMUSDT', 'TRACUSDT', 'TUSDUSDT', 'UNIUSDT', 'USDCUSDT', 'VETUSDT', 'VITEUSDT', 'VOXELUSDT', 'VTHOUSDT', 'WAVESUSDT', 'WAXPUSDT', 'XECUSDT', 'XLMUSDT', 'XNOUSDT', 'XRPUSDT', 'XTZUSDT', 'YFIUSDT', 'ZECUSDT', 'ZENUSDT', 'ZILUSDT', 'ZRXUSDT'
    ]
    
    from_id = 0

    end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    end_date = int(end_date.timestamp() * 1000)

    for symbol in symbols:
        print(f"Working on symbol: {symbol}")
        folder_name = symbol
        create_folder(folder_name)
        getTransaction(symbol, from_id, folder_name, end_date)
        candlesamplePlotter(symbol, end_date)

def main(argv):
    while True:
        print("getHistoricalData()...")
        getHistoricalData()
        current_datetime = datetime.now()
        next_midnight = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        sleep_time = (next_midnight - current_datetime).total_seconds()

        logfile.close()

if __name__ == '__main__':
    main(sys.argv[1:])
