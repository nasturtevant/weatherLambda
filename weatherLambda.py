import requests




def callWeatherAPI():
    # Enter your API key here
    api_key = ""
 
    # base_url variable to store url
    base_url = "http://pro.openweathermap.org/data/2.5/forecast/hourly?"


    lat = ''
    lon = ''


    complete_url = "{}lat={}&lon={}&appid={}".format(base_url,lat,lon,api_key)
 
    # get method of requests module
    # return response object
    response = requests.get(complete_url)
 
    # json method of response object
    # convert json format data into
    # python format data
    return response.json()

def publish_to_sns(message):
    sns = boto3.client('sns')	
    return sns.publish(
          TopicArn='arn:aws:sns:us-east-1:000000000000:topicName',
          Message=json.dumps({'default': json.dumps(message)}),
          MessageStructure='json'
    )    
    
#def lambda_handler(event, context):
    # TODO implement
#    weatherData = callWeatherAPI()
  
print(callWeatherAPI())
