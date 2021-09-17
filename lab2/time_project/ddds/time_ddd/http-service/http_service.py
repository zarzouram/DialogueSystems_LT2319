# -*- coding: utf-8 -*-

import json

from flask import Flask, request
from jinja2 import Environment

app = Flask(__name__)
environment = Environment()


def jsonfilter(value):
    return json.dumps(value)


environment.filters["json"] = jsonfilter

with open('./clock.json', "r") as json_file:
    CLOCK = json.load(json_file)

CLOCK["current_time"]["time_hour"] = 0
CLOCK["current_time"]["time_minute"] = 0
CLOCK["current_alarm"]["alarm_hour"] = 0
CLOCK["current_alarm"]["alarm_minute"] = 0
CLOCK["current_alarm"]["alarm_on"] = False
with open('./clock.json', "w") as json_file:
    json.dump(CLOCK, json_file)


def error_response(message):
    response_template = environment.from_string("""
    {
      "status": "error",
      "message": {{message|json}},
      "data": {
        "version": "1.0"
      }
    }
    """)
    payload = response_template.render(message=message)
    response = app.response_class(response=payload,
                                  status=200,
                                  mimetype='application/json')
    return response


def query_response(value, grammar_entry):
    response_template = environment.from_string("""
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
    """)
    payload = response_template.render(value=value,
                                       grammar_entry=grammar_entry)
    response = app.response_class(response=payload,
                                  status=200,
                                  mimetype='application/json')
    return response


def multiple_query_response(results):
    response_template = environment.from_string("""
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
     """)
    payload = response_template.render(results=results)
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/dummy_query_response", methods=['POST'])
def dummy_query_response():
    response_template = environment.from_string("""
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
     """)
    payload = response_template.render()
    response = app.response_class(response=payload,
                                  status=200,
                                  mimetype='application/json')
    return response


@app.route("/action_success_response", methods=['POST'])
def action_success_response():
    response_template = environment.from_string("""
   {
     "status": "success",
     "data": {
       "version": "1.1"
     }
   }
   """)
    payload = response_template.render()
    response = app.response_class(response=payload,
                                  status=200,
                                  mimetype='application/json')
    return response


@app.route("/set_time", methods=['POST'])
def set_time():
    payload = request.get_json()
    hour_to_set = payload["context"]["facts"]["hour_to_set"]["value"]
    minute_to_set = payload["context"]["facts"]["minute_to_set"]["value"]
    CLOCK["current_time"]["time_hour"] = hour_to_set
    CLOCK["current_time"]["time_minute"] = minute_to_set
    print(CLOCK)
    with open('./clock.json', "w") as json_file:
        json.dump(CLOCK, json_file)
    return action_success_response()


@app.route("/set_alarm", methods=['POST'])
def set_alarm():
    payload = request.get_json()
    selected_alarm_time = payload["context"]["facts"]["selected_alarm_time"]["value"]
    if selected_alarm_time == "eight":
        CLOCK["current_alarm"]["alarm_hour"] = 8
        CLOCK["current_alarm"]["alarm_minute"] = 0
        CLOCK["current_alarm"]["alarm_on"] = True
    elif selected_alarm_time == "eight_thirty":
        CLOCK["current_alarm"]["alarm_hour"] = 8
        CLOCK["current_alarm"]["alarm_minute"] = 30
        CLOCK["current_alarm"]["alarm_on"] = True
    elif selected_alarm_time == "nine":
        CLOCK["current_alarm"]["alarm_hour"] = 9
        CLOCK["current_alarm"]["alarm_minute"] = 0
        CLOCK["current_alarm"]["alarm_on"] = True
    elif selected_alarm_time == "off":
        CLOCK["current_alarm"]["alarm_hour"] = 0
        CLOCK["current_alarm"]["alarm_minute"] = 0
        CLOCK["current_alarm"]["alarm_on"] = False
    with open('./clock.json', "w") as json_file:
        json.dump(CLOCK, json_file)
    return action_success_response()


@app.route("/current_time", methods=['POST'])
def current_time():
    time_hour = CLOCK["current_time"]["time_hour"]
    time_minute = CLOCK["current_time"]["time_minute"]
    time = f'{time_hour}:{time_minute}'
    return query_response(value=time, grammar_entry=None)


@app.route("/current_alarm", methods=['POST'])
def current_alarm():
    if CLOCK["current_alarm"]["alarm_on"] is False:
        alarm_time = "alarm_off"
        return query_response(value=alarm_time, grammar_entry=None)
    else:
        alarm_time = f"{CLOCK['current_alarm']['alarm_hour']}:{CLOCK['current_alarm']['alarm_minute']}"
        if alarm_time == "8:00":
            alarm = "eight"
        elif alarm_time == "8:30":
            alarm = "eight_thirty"
        elif alarm_time == "9:00":
            alarm = "nine"
        else:
            alarm = "alarm_off"
        return query_response(value=alarm, grammar_entry=None)


@app.route("/selected_alarm_time", methods=['POST'])
def selected_alarm_time():
    options = [{
            "value": "eight",
            "confidence": 1.0,
            "grammar_entry": "08:00"
          }, {
            "value": "eight_thirty",
            "confidence": 1.0,
            "grammar_entry": "08:30"
          }, {
            "value": "nine",
            "confidence": 1.0,
            "grammar_entry": "09:00"
          }]
    return multiple_query_response(options)
