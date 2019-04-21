#!/bin/python
from flask import Flask, jsonify, request
from waitress import serve
from wtforms import Form, validators, StringField
from app import read_number_plates

app = Flask(__name__)


@app.route('/status')
def status():
    return "alive"


class ReadForm(Form):
    url = StringField('Url to image', [
        validators.URL()
    ])


@app.route('/read')
def read():
    form = ReadForm(request.args)

    if form.validate():
        url = form.url.data
        number_plates, region_names = read_number_plates(url)

        return jsonify({
            'success': True,
            'url': url,
            'number_plates': number_plates,
            'region_names': region_names,
        })

    return jsonify({
        'success': False,
        'errors': form.errors

    })


def create_app():
    return serve(app)
