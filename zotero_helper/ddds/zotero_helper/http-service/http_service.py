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

SCORE_BOARD_PATH = "dummyscoreboard.json"
with open(SCORE_BOARD_PATH, "r") as json_file:
    SCORE_BOARD = json.load(json_file)


def out_score_board(score_board):
    with open(SCORE_BOARD_PATH, "w") as json_file:
        json.dump(score_board, json_file, indent=4)


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
    # data2print = []
    # status = request.get_json()["request"]["parameters"]
    # for s in status:
    #     data2print.append({f"request_{s}_grammar_entry": status[s]["grammar_entry"]})
    #     data2print.append({f"request_{s}value         ": status[s]["value"]})

    # status = request.get_json()["context"]["facts"]
    # for s in status:
    #     data2print.append({f"facts_{s}_grammar_entry  ": status[s]["grammar_entry"]})
    #     data2print.append({f"facts_{s}value           ": status[s]["value"]})
    # print_data(["action_success_response", *data2print])

    payload = response_template.render()
    response = app.response_class(response=payload, status=200, mimetype='application/json')
    logger.info("Sending successful action response to TDM", response=response)
    return response


# return folder id
# assume that folder names are unique
@app.route("/folder_name", methods=['POST'])
def folder_id():
    payload = request.get_json()
    name = payload["request"]["parameters"]["folder_name"]
    folder_list, folder_name = None, None
    if name:
        folder_name = name["grammar_entry"]
        folder_list = zot.all_collections()
        if folder_list:
            for folder in folder_list:
                if folder["data"]["name"] == folder_name:
                    id_folder = folder["key"]  # folder found
                    break
            else:
                id_folder = "noid"
        else:
            id_folder = "noid"  # no folders in the lib
        # id_folder = ["noid", "id_found"][0]
    else:
        id_folder = 2  # user did not specify folder

    if id_folder == "noid":
        SCORE_BOARD["folder"]["status"] = "notfound"
        out_score_board(SCORE_BOARD)

    id_folder = str(id_folder)
    print_data(["folder_name", folder_list, name, id_folder, folder_name, SCORE_BOARD])
    return query_response(value=id_folder, grammar_entry=id_folder)


def count_records(r_type="record", folder_id=None):
    if r_type == "record":
        if folder_id is None:
            count = zot.count_items()
        else:
            count = zot.collection(folder_id)["meta"]["numItems"]
    else:
        if folder_id is None:
            items = zot.everything(zot.items())
        else:
            items = zot.everything(zot.collection_items(folder_id))

        count = 0
        for item in items:
            count += (item["data"]["itemType"] == r_type)

    print("kkkkkkkkkkk", r_type, folder_id, count)
    return count


# return count + type
@app.route("/items_count_type", methods=['POST'])
def items_num_type():
    payload = request.get_json()
    req_type = payload["request"]["parameters"]["type"]
    req_folder = payload["request"]["parameters"]["folder_id"]["value"]

    item_type = req_type["value"] if req_type else "record"
    folder = req_folder if req_folder != "2" else None

    count_num = count_records(item_type, folder)
    count_unit = item_type
    if item_type != "record":
        count_unit = " ".join(re.findall("[A-Z][^A-Z]*|[a-z]*", item_type)).strip().lower()

    if count_num > 1:
        count_unit += "s"

    count_num_unit = str(count_num) + " " + count_unit
    print_data(["count_type", count_num, count_unit, payload["request"]["parameters"]["folder_id"]])
    return query_response(value="num", grammar_entry=count_num_unit)


# return count only
@app.route("/items_count_only", methods=['POST'])
def items_num():
    payload = request.get_json()
    req_type = payload["request"]["parameters"]["type"]
    req_folder = payload["request"]["parameters"]["folder_id"]["value"]

    item_type = req_type["value"] if req_type else "record"
    folder = req_folder if req_folder != "2" else None

    count_num = count_records(item_type, folder)

    # When to return grammar_entry and when not! This should not be drived by
    # programming requerement! To interact with if/then statement the value
    # should have the number, but if I return None in grammar_entry I got an
    # buildig error.
    # print_data(["count_only", item_type, num])
    return query_response(value=str(count_num), grammar_entry=str(count_num))


@app.route("/check_item_type", methods=['POST'])
def check_type():
    payload = request.get_json()
    item_type = payload["request"]["parameters"]["type"]

    if not item_type:
        r_type = "record"
    else:
        r_type = " ".join(re.findall("[A-Z][^A-Z]*|[a-z]*", item_type["value"]))
        # r_type_g = item_type["grammar_entry"]
    r_type = r_type.strip().lower()
    print_data(["check_item_type", item_type, r_type])
    # When I set the value the response to ReportEmpty when I have a question
    # How many journal article do I have is empty
    return query_response(value="None", grammar_entry=r_type)


@app.route("/folder_fail_response", methods=['POST'])
def folder_fail_response():
    # check fail reason
    reason = "fail"
    if SCORE_BOARD["folder"]["status"] == "notfound":
        reason = "no_folder_found"
        # reset fail reason
        SCORE_BOARD["folder"]["status"] = "None"
        out_score_board(SCORE_BOARD)

    print_data(["folder_fail_response", reason])
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


@app.route("/mydebug", methods=['POST'])
def debug():
    # payload = request.get_json()
    # item_type = payload["request"]["parameters"]["folder_id"]

    # print_data(["debug", item_type])
    return query_response(value=None, grammar_entry="d")


def print_data(data):
    print("\n\n......................\n")
    for d in data:
        pprint(f"{d}")
        print()
    print("......................\n\n")
