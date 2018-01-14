import requests
import sys

def check_tickle():
    url = "https://kyfw.12306.cn/otn/leftTicket/queryZ"
    params = {
        "leftTicketDTO.train_date":"2018-02-10",
        "leftTicketDTO.from_station":"SZQ",
        "leftTicketDTO.to_station":"TJH",
        "purpose_codes":"ADULT",
    }
    headers ={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/63.0.3239.108 Safari/537.36",
    }

    r = requests.get(url, params=params, headers=headers)

    print(r.text)

def allll():
    print(sys._getframe().f_code.co_name)
    abcdef = "ooo"
    print(locals().get(abcdef))

allll()