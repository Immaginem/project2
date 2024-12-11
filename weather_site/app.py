from flask import Flask, request, render_template
from forecast import Forecast
from formuls import Formuls

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        # Получение данных из формы
        start_city = request.form["city1"]
        end_city = request.form["city2"]
        day = int(request.form["days"])
        if day > 5:
            return render_template('err.html',err='Ошибка, слишком много дней')
        # Создание объектов и вычисление данных
        forecast = Forecast(start_city, end_city, 0, day)
        formuls = Formuls(forecast.aggregate_weather_data(), start_city, end_city)
        start_res = formuls.summarize_start_weather()
        end_res = formuls.summarize_end_weather()
        start_weather = forecast.get_start_city_weather()
        end_weather = forecast.get_end_city_weather()

        # Рендеринг страницы с результатами
        return render_template(
            'res_page.html',
            start_city=start_city,
            end_city=end_city,
            start_weather=start_weather,
            end_weather=end_weather,
            end_res=end_res,
            start_res=start_res
        )

    # Рендеринг страницы формы
    return render_template('form_page.html')

if __name__ == '__main__':
    app.run(debug=True)
