#!/usr/bin/env python3
from main import *

def  send_today_timetable():
    dt = datetime.datetime.now()
    today_timetable = gen_timetable(dt)
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

        today_data.append("  " + str(i + 1) + "   限: " + today_timetable[i])
    data = json.dumps({
             "messages":[
                  {
                       "type":"text",
                        "text": daysofweek[dt.weekday()] + "曜日\n" + ','.join(today_data).replace(',', '\n') +  ""
                  }
            ]
    })
    sendlinemessage(data, token)

send_today_timetable()