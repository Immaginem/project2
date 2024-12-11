import requests

class Forecast:
    def __init__(self, starting_city, ending_city, day_start, day_end):
        self.api = 'JK2fkykcucX7HIE0GGyAN48zxRLVmjeA'
        self.weather = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/'
        self.city = 'http://dataservice.accuweather.com/locations/v1/cities/search'
        self.start = starting_city
        self.end = ending_city
        self.day_start = day_start - 1
        self.day_end = day_end - 1
        self.data = {}

    def fetch_city_key(self, city_name):
        response = requests.get(
            self.city,
            params={'apikey': self.api, 'q': city_name}
        ).json()
        return response[0]['Key']

    def fetch_city_forecast(self, city_name):
        city_key = self.fetch_city_key(city_name)
        response = requests.get(
            f"{self.weather}{city_key}",
            params={'apikey': self.api, 'details': True}
        )
        return response.json()

    def process_forecast_data(self, info, city_name):
        min_temp = round((info['Temperature']['Minimum']['Value'] - 32) * (5 / 9), 1)
        max_temp = round((info['Temperature']['Maximum']['Value'] - 32) * (5 / 9), 1)
        humidity = info['Day']['RelativeHumidity']['Average']
        wind_speed = round(info['Day']['Wind']['Speed']['Value'] * 1.6, 0)
        rain_prob = info['Day']['RainProbability']
        snow_prob = info['Day']['SnowProbability']

        self.data[city_name] = {
            'temperature_min': min_temp,
            'temperature_max': max_temp,
            'average_humidity': humidity,
            'wind_speed_kmh': wind_speed,
            'rain_chance': rain_prob,
            'snow_chance': snow_prob
        }

    def load_start_city_data(self):
        forecast = self.fetch_city_forecast(self.start)
        self.process_forecast_data(forecast['DailyForecasts'][self.day_start], self.start)
        return self.data

    def load_end_city_data(self):
        forecast = self.fetch_city_forecast(self.end)
        self.process_forecast_data(forecast['DailyForecasts'][self.day_end], self.end)
        return self.data

    def aggregate_weather_data(self):
        self.load_start_city_data()
        self.load_end_city_data()
        return self.data

    def compose_weather_summary(self, city_name):
        data = self.data[city_name]
        prob_rain = data['rain_chance']
        prob_snow = data['snow_chance']
        prob_message = f"Вероятность дождя: {prob_rain}%" if prob_rain > prob_snow else f"Вероятность снега: {prob_snow}%"

        return (
            f"Минимальная температура: {data['temperature_min']}°C, "
            f"Максимальная температура: {data['temperature_max']}°C, {prob_message}, "
            f"Влажность: {data['average_humidity']}%, Скорость ветра: {data['wind_speed_kmh']} км/ч"
        )

    def get_start_city_weather(self):
        return self.compose_weather_summary(self.start)

    def get_end_city_weather(self):
        return self.compose_weather_summary(self.end)
