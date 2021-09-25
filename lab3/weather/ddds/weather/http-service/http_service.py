# -*- coding: utf-8 -*-

import json
from os import getenv

from flask import Flask, request
from jinja2 import Environment
import structlog

from logger import configure_stdout_logging
from urllib.request import Request, urlopen


def setup_logger():
    logger = structlog.get_logger(__name__)
    try:
        log_level = getenv("LOG_LEVEL", default="INFO")
        configure_stdout_logging(log_level)
        return logger
    except BaseException:
        logger.exception("exception during logger setup")
        raise


logger = setup_logger()
app = Flask(__name__)
environment = Environment()


def jsonfilter(value):
    return json.dumps(value)


environment.filters["json"] = jsonfilter


def error_response(message):
    response_template = environment.from_string(
        """
    {
      "status": "error",
      "message": {{message|json}},
      "data": {
        "version": "1.0"
      }
    }
    """
    )
    payload = response_template.render(message=message)
    response = app.response_class(response=payload, status=200, mimetype='application/json')
    logger.info("Sending error response to TDM", response=response)
    return response


def query_response(value, grammar_entry):
    response_template = environment.from_string(
        """
    {
      "status": "success",
      "data": {
        "version": "1.1",
        "result": [
          {
            "value": {{value|json}},
            "confidence": 1.0,
            "grammar_entry": {{grammar_entry|json}}
          }
        ]
      }
    }
    """
    )
    payload = response_template.render(value=value, grammar_entry=grammar_entry)
    response = app.response_class(response=payload, status=200, mimetype='application/json')
    logger.info("Sending query response to TDM", response=response)
    return response


def multiple_query_response(results):
    response_template = environment.from_string(
        """
    {
      "status": "success",
      "data": {
        "version": "1.0",
        "result": [
        {% for result in results %}
          {
            "value": {{result.value|json}},
            "confidence": 1.0,
            "grammar_entry": {{result.grammar_entry|json}}
          }{{"," if not loop.last}}
        {% endfor %}
        ]
      }
    }
     """
    )
    payload = response_template.render(results=results)
    response = app.response_class(response=payload, status=200, mimetype='application/json')
    logger.info("Sending multiple query response to TDM", response=response)
    return response


def validator_response(is_valid):
    response_template = environment.from_string(
        """
    {
      "status": "success",
      "data": {
        "version": "1.0",
        "is_valid": {{is_valid|json}}
      }
    }
    """
    )
    payload = response_template.render(is_valid=is_valid)
    response = app.response_class(response=payload, status=200, mimetype='application/json')
    logger.info("Sending validator response to TDM", response=response)
    return response


def get_data(city, country, unit="metric"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&units={unit}&APPID={key}"
    print_data([url])
    request = Request(url)
    response = urlopen(request)
    data = response.read()
    return json.loads(data)


@app.route("/dummy_query_response", methods=['POST'])
def dummy_query_response():
    response_template = environment.from_string(
        """
    {
      "status": "success",
      "data": {
        "version": "1.1",
        "result": [
          {
            "value": "dummy",
            "confidence": 1.0,
            "grammar_entry": null
          }
        ]
      }
    }
     """
    )
    payload = response_template.render()
    response = app.response_class(response=payload, status=200, mimetype='application/json')
    logger.info("Sending dummy query response to TDM", response=response)
    return response


@app.route("/action_success_response", methods=['POST'])
def action_success_response():
    response_template = environment.from_string(
        """
   {
     "status": "success",
     "data": {
       "version": "1.1"
     }
   }
   """
    )
    payload = response_template.render()
    response = app.response_class(response=payload, status=200, mimetype='application/json')
    logger.info("Sending successful action response to TDM", response=response)
    return response


@app.route("/temperature", methods=['POST'])
def temperature():
    payload = request.get_json()
    city = payload["context"]["facts"]["city"]["grammar_entry"]
    country = payload["context"]["facts"]["country"]["grammar_entry"]
    unit = payload["request"]["parameters"]["unit"]
    unit = "metric" if unit is None else unit["value"]
    print_data([country])
    data = get_data(city, country, unit)
    temp = data['main']['temp']
    temp = str(temp)
    return query_response(value=temp, grammar_entry=None)


@app.route("/weather", methods=['POST'])
def weather():
    payload = request.get_json()
    city = payload["context"]["facts"]["city"]["grammar_entry"]
    country = payload["context"]["facts"]["country"]["grammar_entry"]
    data = get_data(city, country)

    weather_ = data['weather'][0]['description']
    weather_ = str(weather_)
    return query_response(value=weather_, grammar_entry=None)


def print_data(data):
    print()
    print("......................")
    print(" --> ", end=" ")
    for d in data:
        print(d, end="  ||  ")
    print("......................")
    print()
