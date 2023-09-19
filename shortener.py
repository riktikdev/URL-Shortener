# Импортирование стандартных библиотек
import string
import random
import json

# Импортирование Flask
from flask import Flask, render_template, redirect, url_for, request

# Импортирование Validator's
import validators

app = Flask(__name__)
shortened_urls = {}


# Функция создания короткой ссылки
def create_short_url(length=9):
    chars = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(chars) for _ in range(length))
    return short_url


@app.route('/',methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']

        # Проверка на валидность ссылки
        if not validators.url(long_url):
            return 'Вы ввели недопустимый URL адрес', 400

        short_url = create_short_url()

        while short_url in shortened_urls:
            short_url = create_short_url()

        shortened_urls[short_url] = long_url

        with open('saved_urls.json', 'w') as file:
            json.dump(shortened_urls, file)

        return f'Ваш сокращенный URL адрес: {request.url_root}{short_url}'
    return render_template('index.html')


@app.route('/<short_url>')
def redirect_url(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return render_template('error.html', message='Запрашиваемый URL адрес не найден'), 404


@app.errorhandler(400)
def bad_request_error(error):
    return render_template('error.html', message='Недопустимый URL адрес'), 400


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', message='Запрашиваемый URL адрес не найден'), 404


if __name__ == '__main__':
    try:
        with open('saved_urls.json', 'r') as file:
            shortened_urls = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        shortened_urls = {}

    app.run(host='0.0.0.0', port=5000, debug=True)
