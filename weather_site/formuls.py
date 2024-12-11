class Formuls: #НАЗВАНИЕ КЛАССА + ФУНКЦИЙ И РЕТЕРНЫ
    def __init__(self, data, start, end):
        self.data = data
        self.start = start
        self.end = end

    def is_temperature_optimal(self, place):
        min_temp = self.data[place]["temperature_min"]
        max_temp = self.data[place]["temperature_max"]
        return 12 < min_temp < 27 and max_temp < 27

    def is_humidity_within_range(self, place):
        humidity = self.data[place]['average_humidity']
        return 27 < humidity < 69

    def analyze_wind_conditions(self, place):
        wind_speed = self.data[place]['wind_speed_kmh']
        if wind_speed > 69:
            return f'Небезопасно, в {place} штормовый ветер'
        return wind_speed < 27

    def are_precipitation_chances_low(self, place):
        snow_prob = self.data[place]['snow_chance']
        rain_prob = self.data[place]['rain_chance']
        return max(snow_prob, rain_prob) < 69

    def evaluate_weather_conditions(self, place):
        temp = self.is_temperature_optimal(place)
        humidity = self.is_humidity_within_range(place)
        wind = self.analyze_wind_conditions(place)
        if not isinstance(wind, bool):
            return wind
        prob = self.are_precipitation_chances_low(place)
        if not temp or not prob:
            return 'Неблагоприятная погода'
        elif not humidity or not wind:
            return 'Удовлетворительная погода'
        else:
            return 'Отличная погода'

    def summarize_start_weather(self):
        return self.evaluate_weather_conditions(self.start)

    def summarize_end_weather(self):
        result = self.evaluate_weather_conditions(self.end)
        if result == 'Неблагоприятная погода':
            return 'Погода в месте назначения крайне неблагоприятная. Поездку стоит отложить.'
        elif result == 'Удовлетворительная погода':
            return 'Погода допустима, но не идеальна. Рекомендуем тщательно обдумать поездку.'
        else:
            return 'Погода в месте назначения отличная! Удачной поездки!'
