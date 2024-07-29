import requests as req
import os
import pywhatkit as pykt
# from plyer import notification
from dotenv import load_dotenv

load_dotenv()

KEY=os.getenv("API_KEY")

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



def get_weather(LOC,KEY):
    res=req.get(f"http://api.openweathermap.org/data/2.5/forecast?q={LOC}&appid={KEY}")
    data=res.json()
    return data

def rain_check(data):
    for forecast_data in data["list"]:
        weather_description = forecast_data["weather"][0]["description"]
        if "rain" in weather_description.lower():
            return True
    return False

def notifier(number,message,hour,minute):
    pykt.sendwhatmsg(number,message,hour,minute)
    
def main():
    ip=getip()
    LOC=getloc(ip)
    
    city_data=get_weather(LOC,KEY)
    print("Please enter the  hour and minute in 24 hour format E.g. 13:30 for 1:30 PM")
    number=input("Enter the number:")
    message=input("Enter the message:")
    hour=int(input("Enter the hour:"))
    minute=int(input("Enter the minute:"))
    
    if rain_check(city_data):
        notifier(
            number,
            message+". It's going to rain today at "+LOC+" in few hours",
            hour,
            minute
        )
    



if __name__=="__main__":
    main()



    