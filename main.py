import requests as req
import os
from plyer import notification
from dotenv import load_dotenv

load_dotenv()

KEY=os.getenv("API_KEY")

def getip():
    res=req.get('https://api.ipify.org')
    return res.text

ip=getip()
def getloc():
    res=req.get(f"http://ip-api.com/json/{ip}")
    data=res.json()
    return data["city"]

LOC=getloc()


def get_weather():
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
    city_data=get_weather()
    if rain_check(city_data):
        notifier()



if __name__=="__main__":
    main()



    