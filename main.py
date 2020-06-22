#!/usr/bin/env python3
import urllib.request
import json
import datetime
import sys
import schedule
import time
import setting

token = setting.token

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

def gen_timetable(dt, weekday="default"):
    if weekday == "default":
        weekday = dt.weekday()
    if weekday >  4:
        print("今日はお休みです！")
        exit(0)

    today_timetable = timetable[daysofweek[weekday]]
    return today_timetable



def send_now_class():
    schedule.every().day.at("08:40").do(sendstarttime, 1)
    schedule.every().day.at("09:35").do(sendstarttime, 2)
    schedule.every().day.at("10:30").do(sendstarttime, 3)
    schedule.every().day.at("11:25").do(sendstarttime, 4)
    schedule.every().day.at("12:50").do(sendstarttime, 5)
    schedule.every().day.at("13:45").do(sendstarttime, 6)
    schedule.every().day.at("14:20").do(sendstarttime, 7)
    
    
def sendstarttime(lesson_number):
    dt = datetime.datetime.now()
    today_timetable = gen_timetable(dt)

    if not len(today_timetable) < lesson_number and lesson_number != 1:
        if today_timetable[lesson_number - 2] == today_timetable[lesson_number - 1]:
            print("Same as last time.")
            exit(0)
        
    data = json.dumps({
             "messages":[
                  {
                       "type":"text",
                        "text":str(lesson_number) + "限: " + today_timetable[lesson_number - 1] + "の授業の時間です."
                  }
            ]
    })
    sendlinemessage(data, token)



def main():
    schedule.every().day.at("08:40").do(sendstarttime, 1)
    schedule.every().day.at("09:35").do(sendstarttime, 2)
    schedule.every().day.at("10:30").do(sendstarttime, 3)
    schedule.every().day.at("11:25").do(sendstarttime, 4)
    schedule.every().day.at("12:50").do(sendstarttime, 5)
    schedule.every().day.at("13:45").do(sendstarttime, 6)
    schedule.every().day.at("14:30").do(sendstarttime, 7)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
    exit(0)

if __name__ == "__main__":
    main()
