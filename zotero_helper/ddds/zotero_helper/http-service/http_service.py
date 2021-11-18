# -*- coding: utf-8 -*-

import json
from os import getenv
import re

from flask import Flask, request
from jinja2 import Environment
# from copy import deepcopy

import structlog

from logger import configure_stdout_logging
# from urllib.request import Request, urlopen

from pyzotero import zotero
from requests.api import get
from urllib.parse import quote_plus
from settings import api_key, usr_id
from papers_db import citations
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

# naive board may be needed
SCORE_BOARD_PATH = "dummyscoreboard.json"
with open(SCORE_BOARD_PATH, "r") as json_file:
    SCORE_BOARD = json.load(json_file)

# Wekimedia api data, used to get citation data given an article
# identifier.
base_url = "http://en.wikipedia.org/api/rest_v1/data/citation/zotero/"
header = {"accept": "application/json", "charset": "utf-8"}


def word2num(num_str):

    mapping = {
        "zero": "0", "one": "1", "two": "2", "three": "3",
        "four": "4", "five": "5", "six": "6", "seven": "7",
        "eight": "8", "nine": "9", "dot": ".", "v": "v"}
    wrd_list = num_str.split(" ")
    num4wrd = "".join([mapping[x] for x in wrd_list])

    return num4wrd


def format_arxiv_identifier(identifier):
    identifier_num = word2num(identifier)
    return f"http://arxiv.org/abs/{identifier_num}"


def paper_info_zotero(identifier):
    url = base_url + quote_plus(identifier)
    try:
        response = get(url, headers=header, timeout=(1, 3.05))
        data = response.text
        data2print = ["wiki_resp"]
    except Exception:  # to avoid having read time out
        data2print = ["Paper Readtime out"]
        data = []

    print_data(data2print)
    return data


def reformat_authors(authors):
    if len(authors) >= 3:
        return f"{authors[0]} and others"
    if len(authors) == 2:
        return f"{', '.join(authors[:-1])} and {authors[-1]}"

    return authors[0]


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
@app.route("/folder_id", methods=['POST'])
def folder_id():
    print("\n\nhere\n")
    payload = request.get_json()
    name = payload["request"]["parameters"]["folder_name"]
    current_id = SCORE_BOARD["folder"]["current"]

    folder_list, folder_name, folder_type = None, None, None
    if name:
        folder_name = name["grammar_entry"]
        folder_type = name["value"]

        if folder_type == "CurrentFolder":  # user requested current folder
            # return current folder if known by the system else return "0"
            id_folder = current_id if current_id != "None" else "0"
        else:  # user requested other folder
            if folder_type == "LibraryFolder":
                id_folder = "home"
            else:
                folder_list = zot.all_collections()
                if folder_list:
                    for folder in folder_list:
                        if folder["data"]["name"] == folder_name:
                            id_folder = folder["key"]  # requested folder found
                            break
                    else:
                        id_folder = "noid"  # requested folder not found
                else:
                    id_folder = "noid"  # no folders in the lib
    else:
        id_folder = "2"  # user did not specify folder

    if id_folder == "noid":
        SCORE_BOARD["folder"]["status"] = "notfound"
        out_score_board(SCORE_BOARD)

    print_data(["folder_id", id_folder, folder_type])
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
    print_data(["count_type", count_num, payload["request"]["parameters"]["folder_id"], count_unit, count_num_unit])
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
    print_data(["count_only", item_type, count_num])
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
    return query_response(value="checktype", grammar_entry=r_type)


@app.route("/folder_fail_response", methods=['POST'])
def folder_fail_response():
    # check fail reason
    # reason = "fail"
    if SCORE_BOARD["folder"]["status"] == "notfound":
        # reason = "no_folder_found"
        # reset fail reason
        SCORE_BOARD["folder"]["status"] = "None"
        out_score_board(SCORE_BOARD)

    # print_data(["folder_fail_response", reason])
    return action_success_response()


# return identifier url
@app.route("/identifier_url", methods=['POST'])
def identifier_url():
    payload = request.get_json()
    identifier = payload["request"]["parameters"]["item_identifier"]
    identifier = format_arxiv_identifier(identifier["grammar_entry"])

    return query_response(value="arxiv", grammar_entry=identifier)


# return citation info
# Combine both /identifier_url & /cite_info_api
# get citation info in zotero format using api. Too slow for TDM.
@app.route("/cite_info_api", methods=['POST'])
def cite_info_api():
    payload = request.get_json()
    identifier = payload["request"]["parameters"]["item_identifier_url"]
    cite_info = paper_info_zotero(identifier["grammar_entry"])

    # print_data(["cite_info", identifier, cite_info])

    return query_response(value="None", grammar_entry=cite_info)


# return citation info
# Combine both /identifier_url & /cite_info
# load citation info from db
@app.route("/cite_info", methods=['POST'])
def get_cite_info():
    payload = request.get_json()
    identifier = payload["request"]["parameters"]["item_identifier_url"]
    cite_ = json.dumps(citations[quote_plus(identifier["grammar_entry"])])
    print_data(["cite_info", identifier, cite_])

    return query_response(value="cite", grammar_entry=str(cite_))


# create folder
@app.route("/create_folder", methods=['POST'])
def create_folder():
    payload = request.get_json()
    folder = payload["request"]["parameters"]["folder_name"]["grammar_entry"]

    _status = zot.create_collections([{"name": folder}])  # noqa: F841

    print_data(["create_folder", _status])
    return action_success_response()


# return title
@app.route("/title", methods=['POST'])
def title():
    payload = request.get_json()
    my_cite_info = payload["request"]["parameters"]["cite_info"]["grammar_entry"]
    my_title = json.loads(my_cite_info)[0]["title"]

    print_data(["title", type(my_title), my_cite_info])

    return query_response(value="tilte", grammar_entry=my_title)


# rfolder status
@app.route("/folder_status", methods=['POST'])
def folder_status():
    # payload = request.get_json()
    print_data(["folder_status"])

    return query_response(value="ncreated", grammar_entry="ncreated")


# return authors formated
@app.route("/authors", methods=['POST'])
def authors():
    payload = request.get_json()
    cite_info = payload["request"]["parameters"]["cite_info"]["grammar_entry"]
    authors_nm = json.loads(cite_info)[0]["creators"]
    authors = reformat_authors([" ".join([nm["firstName"], nm["lastName"]]) for nm in authors_nm])

    # print_data(["authors", authors])

    return query_response(value="None", grammar_entry=authors)


# create item
@app.route("/create_item", methods=['POST'])
def create_item():
    payload = request.get_json()
    # data2print = []
    # status = payload["request"]["parameters"]
    # for s in status:
    #     data2print.append({f"request_{s}_grammar_entry": status[s]["grammar_entry"]})
    #     data2print.append({f"request_{s}_value        ": status[s]["value"]})

    # status = payload["context"]["facts"]
    # for s in status:
    #     data2print.append({f"facts_{s}_grammar_entry  ": status[s]["grammar_entry"]})
    #     data2print.append({f"facts_{s}_value          ": status[s]["value"]})
    # print_data(["create_item", *data2print])
    item = payload["context"]["facts"]["cite_info"]["grammar_entry"]
    dist = payload["context"]["facts"]["folder_id_dist"]["value"]
    zotero_dict = json.loads(item)
    item_type = zotero_dict[0]["itemType"]
    if dist == "noid":
        folder_name = payload["context"]["facts"]["folder_name"]["grammar_entry"]
        folder_list = zot.all_collections()
        for folder in folder_list:
            if folder["data"]["name"] == folder_name:
                id_folder = folder["key"]  # requested folder found
                break
        item_temp = zot.item_template(item_type)
        for k in item_temp:
            if k in zotero_dict[0]:
                item_temp[k] = zotero_dict[0][k]
            item_temp["collections"] = [id_folder]
        print(item_temp)
        _feedback = zot.create_items([item_temp])  # noqa: F841

    elif dist == "home":
        _feedback = zot.create_items(zotero_dict)  # noqa: F841

    else:
        item_temp = zot.item_template(item_type)
        for k in item_temp:
            if k in zotero_dict[0]:
                item_temp[k] = zotero_dict[0][k]
            item_temp["collections"] = [dist]

        _feedback = zot.create_items([item_temp])  # noqa: F841
        # _feedback = zot.addto_collection(dist, item_temp)  # noqa: F841

    if "folder" in payload["context"]["facts"]:
        f = payload["context"]["facts"]["folder"]["value"]
    else:
        f = None
    print_data(["add", _feedback, f])
    return action_success_response()


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
