import requests
user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) " \
        "Chrome/44.0.2403.157 Safari/537.36 "
headers = {"User-Agent": user_agent,
            "Connection": "keep-alive"}
for stationID in range(3959, 10000):
    url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID="\
        +str(stationID)+"&timeframe=3&submit=Download+Data"
    r = requests.get(url, headers=headers)
    # open打开excel文件，报存为后缀为xls的文件
    file = "./data/"+ str(stationID) + ".csv"
    fp = open(file, "wb")
    fp.write(r.content)
    fp.close()



