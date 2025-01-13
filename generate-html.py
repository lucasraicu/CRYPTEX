def generate_html_table(data):
    table_html = "<table>\n<tr>\n<th>Coin</th>\n<th>Year</th>\n<th>Month</th>\n<th>Week</th>\n<th>Day</th>\n<th>Hour</th>\n<th>Minute</th>\n<th>Second</th>\n<th>All Transactions</th>\n</tr>\n"
    
    for row in data:
        table_html += "<tr>\n"
        for item in row:
            if item.startswith("<a"):
                table_html += f"<td>{item}</td>\n"
            else:
                table_html += f"<td>{item}</td>\n"
        table_html += "</tr>\n"
    
    table_html += "</table>"
    return table_html


# Example data with variable names as a list
coin_names = [
    '1INCHUSDT', 'AAVEUSDT', 'ACHUSDT', 'ADAUSDT', 'ALGOUSDT', 'ALICEUSDT', 'ALPINEUSDT', 'ANKRUSDT', 'ANTUSDT', 'APEUSDT', 'API3USDT', 'APTUSDT', 'ARBUSDT', 'ASTRUSDT', 'ATOMUSDT', 'AUDIOUSDT', 'AVAXUSDT', 'AXLUSDT', 'AXSUSDT', 'BALUSDT', 'BANDUSDT', 'BATUSDT', 'BCHUSDT', 'BICOUSDT', 'BLURUSDT', 'BNBUSDT', 'BNTUSDT', 'BONDUSDT', 'BOSONUSDT', 'BTCUSDT', 'BTRSTUSDT', 'CELOUSDT', 'CELRUSDT', 'CHZUSDT', 'CLVUSDT', 'COMPUSDT', 'COTIUSDT', 'CRVUSDT', 'CTSIUSDT', 'DAIUSDT', 'DARUSDT', 'DASHUSDT', 'DGBUSDT','DIAUSDT', 'DOGEUSDT', 'DOTUSDT', 'EGLDUSDT', 'ENJUSDT', 'ENSUSDT', 'EOSUSDT', 'ETCUSDT', 'ETHUSDT', 'FETUSDT', 'FILUSDT', 'FLOKIUSDT', 'FLOWUSDT', 'FLUXUSDT', 'FORTHUSDT', 'FTMUSDT', 'GALUSDT', 'GALAUSDT', 'GLMUSDT', 'GRTUSDT', 'GTCUSDT', 'HBARUSDT', 'ICPUSDT', 'ICXUSDT', 'ILVUSDT', 'IMXUSDT', 'IOSTUSDT', 'IOTAUSDT', 'JAMUSDT', 'KAVAUSDT', 'KDAUSDT', 'KNCUSDT', 'KSMUSDT', 'LAZIUSDT', 'LDOUSDT', 'LINKUSDT', 'LOKAUSDT','LOOMUSDT', 'LPTUSDT', 'LRCUSDT', 'LSKUSDT', 'LTCUSDT', 'LTOUSDT', 'MANAUSDT', 'MASKUSDT', 'MATICUSDT', 'MKRUSDT', 'MXCUSDT', 'NEARUSDT', 'NEOUSDT', 'NMRUSDT', 'OCEANUSDT', 'OGNUSDT', 'OMGUSDT', 'ONEUSDT', 'ONTUSDT', 'OPUSDT', 'OXTUSDT', 'PAXGUSDT', 'POLYXUSDT', 'PONDUSDT', 'PORTOUSDT', 'PROMUSDT', 'QNTUSDT', 'QTUMUSDT', 'RADUSDT', 'RAREUSDT', 'REEFUSDT', 'RENUSDT', 'REQUSDT', 'RLCUSDT', 'RNDRUSDT', 'ROSEUSDT', 'RVNUSDT', 'SANDUSDT', 'SANTOSUSDT', 'SHIBUSDT','SKLUSDT', 'SLPUSDT', 'SNXUSDT', 'SOLUSDT', 'STGUSDT', 'STORJUSDT', 'SUSHIUSDT', 'SYSUSDT', 'TUSDT', 'THETAUSDT', 'TLMUSDT', 'TRACUSDT', 'TUSDUSDT', 'UNIUSDT', 'USDCUSDT', 'VETUSDT', 'VITEUSDT', 'VOXELUSDT', 'VTHOUSDT', 'WAVESUSDT', 'WAXPUSDT', 'XECUSDT', 'XLMUSDT', 'XNOUSDT', 'XRPUSDT', 'XTZUSDT', 'YFIUSDT', 'ZECUSDT', 'ZENUSDT', 'ZILUSDT', 'ZRXUSDT'
    ]

data = []
for coin_name in coin_names:
    data.append([coin_name, f'<a href="{coin_name}/candlesticks-YE.csv">CSV</a>, <a href="{coin_name}/candlesticks-YE-plot.html">Plot</a>', f'<a href="{coin_name}/candlesticks-ME.csv">CSV</a>, <a href="{coin_name}/candlesticks-ME-plot.html">Plot</a>', f'<a href="{coin_name}/candlesticks-W.csv">CSV</a>, <a href="{coin_name}/candlesticks-W-plot.html">Plot</a>', f'<a href="{coin_name}/candlesticks-D.csv">CSV</a>, <a href="{coin_name}/candlesticks-D-plot.html">Plot</a>', f'<a href="{coin_name}/candlesticks-h.csv">CSV</a>, <a href="{coin_name}/candlesticks-h-plot.html">Plot</a>', f'<a href="{coin_name}/candlesticks-Min.csv">CSV</a>', f'<a href="{coin_name}/candlesticks-s.csv">CSV</a>', f'<a href="{coin_name}/transactions.csv">CSV</a>'])

# Generate HTML table
html_table = generate_html_table(data)

print(html_table)
