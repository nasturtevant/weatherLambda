import requests
import json
import pytz
import time
import boto3
import logging

from datetime import datetime
from datetime import timedelta
from pytz import timezone
from configparser import ConfigParser

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
                


def clean_message(data):
    message = "Low temps incoming: "
    dataList = ""
    for d in data:
        #dataList = "<<<" + dataList + " " + str(d["Temperature"]) + " "
        #dataList = dataList + " " + str(d["Time"]) + ">>>        "
        dataList = dataList + str(d)
    return message + str(dataList)

def get_weather(props):
        
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={props.get('lat')}&lon={props.get('lon')}&appid={props.get('api_key')}&units={props.get('units')}"
    
    try:
        response = requests.get(url)
    except Exception as e:
        logger.error("Error getting weather data: {}".format(e))
        return "Error getting weather data: {}".format(e)
    data = json.loads(response.text)

    temperatureDataDict,windDataDict = load_weather_data(data)

    triggerData = find_weather_data(temperatureDataDict,windDataDict, props.get('wind_speed'), props.get('low_temp'), props.get('high_temp'))

    for item in triggerData:
        print(triggerData[item])


def load_weather_data(data):
    temperatureDataDict = {}
    windDataDict = {}

    for d in data["list"]:
        dt = datetime.fromtimestamp(d["dt"], pytz.timezone('EST'))
        temperature = d["main"]["temp"]
        wind = d["wind"]["gust"]
        stringTime = dt.strftime("%A %m-%d-%Y %H:%M %Z")
        temperatureDataDict[stringTime] = temperature
        windDataDict[stringTime] = wind

    # logger.debug(f"Wind Data: {windDataDict.items()}")
    return temperatureDataDict,windDataDict

def find_weather_data(temperatureDataDict,windDataDict,wind_speed,min,max):
    weatherData = {}

    for time, temp in temperatureDataDict.items():
        if temp < int(min):
            if time in weatherData:
                if "Temp" in weatherData[time]:
                    if weatherData[time]["Temp"] < temp:
                        weatherData[time].update({"Temp": temp})
                else:
                    weatherData[time].update({"Temp": temp})
            else:
                weatherData[time] = {"Temp": temp}
            logger.info(f"Temperature {temp} is below minimum {min} at {time}")
        if temp > int(max):
            if time in weatherData:
                if "Temp" in weatherData[time]:
                    if weatherData[time]["Temp"] > temp:
                        weatherData[time].update({"Temp": temp})
                else:
                    weatherData[time].update({"Temp": temp})
            else:
                weatherData[time] = {"Temp": temp}

    for time, wind in windDataDict.items():
        if wind > int(wind_speed):
            if time in weatherData:
                if "Wind" in weatherData[time]:
                    if weatherData[time]["Wind"] > wind:
                        weatherData[time].update({"Wind": wind})
                else:
                    weatherData[time].update({"Wind": wind})
            else:
                weatherData[time] = {"Wind": wind}

    return weatherData

def publish_to_sns(message):
    sns = boto3.client('sns')
    return sns.publish(
        TopicArn='arn:aws:sns:us-east-1:123456789012:WeatherNotification',
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json'
    )

def lambda_handler(event, context):
    config = ConfigParser()
    config.read('config.ini')
    logger.info(f"Config: {config.sections()}")
    props = config['default']

    # weatherResp = get_weather(props.get('api_key'), props.get('lat'), props.get('lon'), props.get('units'))
    weatherResp = get_weather(props)
    

    # if len(weatherResp) > 0:
    #     resp = clean_message(weatherResp)
    #     return publish_to_sns(resp)
    # else:
    #     return weatherResp