import requests as req
import os
import pywhatkit as pykt
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# KEY=os.getenv("API_KEY")

def getip():
    res=req.get('https://api.ipify.org')
    return res.text


def getloc(ip):
    res = req.get(f"https://ipinfo.io/{ip}/json")
    data = res.json()
    if "city" in data:
        return data["city"]
    else:
        return "Unknown"



def get_weather(LOC):
    res=req.get(f"https://wttr.in/{LOC}?format=j1")
    data=res.json()
    return data

# def rain_check(data):
#     for forecast_data in data["list"]:
#         weather_description = forecast_data["weather"][0]["description"]
#         if "rain" in weather_description.lower():
#             return True
#     return False

def rain_check(data):
    for forecast in data["weather"]:
        for hourly in forecast["hourly"]:
            weather_description = hourly["weatherDesc"][0]["value"]
            if "rain" in weather_description.lower():
                return True
    return False

def notifier(number,message,hour,minute):
    pykt.sendwhatmsg(number,message,hour,minute)
    
def main():
    ip=getip()
    LOC=getloc(ip)
    
    city_data=get_weather(LOC)
    print("Please enter the  hour and minute in 24 hour format E.g. 13:30 for 1:30 PM")
    number=input("Enter the number:")
    message=input("Enter the message:")
    hour=int(input("Enter the hour:"))
    minute=int(input("Enter the minute:"))
    
    if rain_check(city_data):
        time=datetime.now()
        check_time=time.replace(hour=hour,minute=minute,second=0, microsecond=0)
        if(check_time-time).total_seconds()<=120:
            notifier(
                number,
                message+". It's going to rain today at "+LOC+" in few hours",
                hour,
                minute
            )
        else:
            notifier(
                number,
                message+". It's not going to rain today at "+LOC,
                hour,
                minute
            )
    print((check_time-time).total_seconds())



if __name__=="__main__":
    main()



    