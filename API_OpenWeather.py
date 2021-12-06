# SI 206 Final Project
# OpenWeather API
# Ryan Horlick


# api.openweathermap.org/data/2.5/forecast/daily?q={city name}&cnt={cnt}&appid={API key}

# api.openweathermap.org/data/2.5/forecast/daily?q={city name},{state code}&cnt={cnt}&appid={API key}

import requests
import json





Api_key = "26b0ce95b59c0362ddbde7102cb97c68"
city_name = "alabama"
cnt = "1"
url = "https://api.openweathermap.org/data/2.5/forecast/daily?q={" + city_name + "}&cnt={" + cnt + "}&appid={" + Api_key + "}"

response = requests.get(url)
data = json.loads(response.text)
print(data)