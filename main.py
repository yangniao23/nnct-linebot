#!/usr/bin/env python3
import urllib.request
import json
import datetime

token = '0irVpDIYgnm1pYvhJxTdVIfp1P3xhnyhPIHimbmAy69VzhVTapfuX8QLjiPTH7Rhtw9qXnN3WLf89CWyz3SZcFyHb6cHYRiohY/gcKaQJZJp4j8NVeRPosEzrxZ8ltMQ3LbvqXo4hc2V6xCrUEFwFQdB04t89/1O/w1cDnyilFU='

daysofweek = ["月", "火", "水", "木", "金", "土", "日"]

timetable = {
    "月": ["英語IA", "英語IA", "化学", "国語", "英語IB", "英語IB", "課題数学"],
    "火": ["基礎数A", "基礎数A", "化学", "化学", "専門教科", "専門教科", "専門教科", "専門教科"],
    "水":  ["国語", "国語", "基礎数A", "基礎数A", "生命環境基礎", "生命環境基礎", "音楽/美術"],
    "木": ["保健体育", "保健体育", "世界史", "世界史", "英語IC", "英語多読",  "特活"],
    "金": ["現代社会", "現代社会", "基礎数A", "基礎数A", "専門教科", "専門教科"]
}
def sendlinemessage(data, token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
    }
    
    response = urllib.request.Request('https://api.line.me/v2/bot/message/broadcast', data=data.encode(), method='POST', headers=headers)

    try:
        with urllib.request.urlopen(response) as response:
            body = json.loads(response.read())
            headers = response.getheaders()
            status = response.getcode()

            print(headers)
            print(status)
            print(body)

    except urllib.error.URLError as e:
         print(e.reason)


def  send_timetable():
    dt = datetime.datetime.now()
    if dt.weekday() >  4:
        print("今日はお休みです！")
        return 0

    today_timetable = timetable[daysofweek[dt.weekday()]]
    today_data = []

    for i in range(len(today_timetable)):
        try:
            if today_timetable[i] == today_timetable[i+3]: 
                today_data.append(str(i+1) + "~" + str(i+4) + "限: " + today_timetable[i])
                break
        except IndexError:
            pass

        if not len(today_timetable) == i + 1:
            if today_timetable[i] == today_timetable[i+1]:      
                today_data.append(str(i + 1) + "~" + str(i+2) + "限: " + today_timetable[i])
                continue
            elif today_timetable[i - 1] == today_timetable[i]:
                continue

        elif today_timetable[i - 1] == today_timetable[i]:
            if len(today_timetable) == i + 1:
                break
            continue

        today_data.append(" " + str(i + 1) + " 限: " + today_timetable[i])
    data = json.dumps({
             "messages":[
                  {
                       "type":"text",
                        "text": daysofweek[dt.weekday()] + "曜日\n" + ','.join(today_data).replace(',', '\n') +  ""
                  }
            ]
    })
    sendlinemessage(data, token)

send_timetable()