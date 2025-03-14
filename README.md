
# Weather Lambda

Have you ever been caught off-guard by a particually cold day, or perhaps a windy one? Well, I have... and I got tired of replacing frozen cracked water hoses or dragging the empty trash can out of the road because the wind decided to play with it after I forgot (was too lazy) to bring it up the driveway.

The next time you forget to check the weather, this Lambda function has got your back.


To get started, go to [Open Weather Map](https://openweathermap.org/) and get yourself an API key (free)


## Run Locally

Clone the project

```bash
  git clone https://github.com/nasturtevant/weatherLambda
```

Go to the project directory and find the config.ini file. In here you will add your API key, the latitude & longitude of the location you want data for, as well as your high & low temp thresholds and wind speed.

```bash
api_key = <yourkeyhere>
lat = 36.998979651737436
lon = -109.04521077269315
units = imperial # Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit
low_temp = 50
high_temp = 90
wind_speed = 20
```


