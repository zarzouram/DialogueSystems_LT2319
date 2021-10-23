# -*- coding: utf-8 -*-

import json
from os import getenv
import re

from flask import Flask, request
from jinja2 import Environment
import structlog

from logger import configure_stdout_logging
# from urllib.request import Request, urlopen

from pyzotero import zotero
from settings import api_key, usr_id
from pprint import pprint


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
zot = zotero.Zotero(usr_id, 'user', api_key)


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


# return count + type
@app.route("/items_count_type", methods=['POST'])
def items_num_type():
    payload = request.get_json()
    item_type = payload["request"]["parameters"]["type"]
    print_data(item_type)

    if not item_type:
        num = zot.count_items()
        r_type = "records" if num > 1 else "record"
    else:
        num = 0
        items = zot.everything(zot.items())
        r_type = " ".join(re.findall("[A-Z][^A-Z]*|[a-z]*", item_type["value"]))
        r_type = r_type.strip().lower()
        print_data(r_type)
        for item in items:
            num += (item['data']['itemType'] == item_type["value"])
        if num > 1:
            r_type += "s"

    num = str(num) + " " + r_type
    print_data(num)
    return query_response(value=None, grammar_entry=num)


@app.route("/check_item_type", methods=['POST'])
def check_type():
    payload = request.get_json()
    item_type = payload["request"]["parameters"]["type"]
    print_data(item_type)

    if not item_type:
        r_type = "records"
    else:
        r_type = " ".join(re.findall("[A-Z][^A-Z]*|[a-z]*", item_type["value"]))
        # r_type_g = item_type["grammar_entry"]

    # When I ser the value the response to ReportEmpty when I have a question
    # How many journal article do I have is empty
    return query_response(value=None, grammar_entry=r_type)


# return count only
@app.route("/items_count_only", methods=['POST'])
def items_num():
    payload = request.get_json()
    item_type = payload["request"]["parameters"]["type"]
    print_data(item_type)

    if not item_type:
        num = zot.count_items()
    else:
        num = 0
        items = zot.everything(zot.items())
        for item in items:
            num += (item['data']['itemType'] == item_type["value"])

    # When to return grammar_entry and when not! This should not be drived by
    # programming requerement! To interact with if/then statement the value
    # should have the number, but if I return None in grammar_entry I got an
    # buildig error.
    print_data(num)
    return query_response(value=str(num), grammar_entry=str(num))


def print_data(data):
    print("\n\n......................")
    if isinstance(data, list):
        for d in data:
            print(f"--> {d}")
    elif isinstance(data, dict):
        print("-->", end="")
        pprint(data, indent=2)
    else:
        print(f"--> {data}")
    print("......................\n\n")
