import requests as req
import os
from plyer import notification
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

def notifier():
    notification.notify(
        title="Rain Alert!",
        message="It's going to rain today!",
        app_name="Rain Alert",
        timeout=10, 
    )
def main():
    ip=getip()
    LOC=getloc(ip)
    
    city_data=get_weather(LOC,KEY)
    if rain_check(city_data):
        notifier()
    print(LOC)



if __name__=="__main__":
    main()



    