# Report

- [1. Introduction](#1-introduction)
- [2. API](#2-api)
  - [2.1. Pyzotero](#21-pyzotero)
  - [2.2. Wikimedia REST API](#22-wikimedia-rest-api)
- [3. Data collection](#3-data-collection)
  - [3.1. Scenario](#31-scenario)
    - [3.1.1. Add items manually](#311-add-items-manually)
    - [3.1.2. Add items using arXiv identifier](#312-add-items-using-arxiv-identifier)
    - [3.1.3. Query number of items](#313-query-number-of-items)
  - [3.2. Collected material](#32-collected-material)
    - [3.2.1. Add items manually](#321-add-items-manually)
    - [3.2.2. Add items using arXiv identifier](#322-add-items-using-arxiv-identifier)
    - [3.2.3. Query number of items](#323-query-number-of-items)
  - [3.3. Distillation](#33-distillation)
- [4. Implementation](#4-implementation)
- [5. Sample dialogues handled](#5-sample-dialogues-handled)
- [6. Discussion](#6-discussion)
- [7. Future work](#7-future-work)
- [8. Code](#8-code)
- [9. collected dialogues, distilled dialogues](#9-collected-dialogues-distilled-dialogues)
- [10. Refrences](#10-refrences)

---

## 1. Introduction

`Zotero Helper` enables the user to interface with `Zotero` reference management
through a dialogue system. `Zotero` is a free reference management software that
helps users organize their research sources. In this project, the user can add
items either by arXiv identifier or by providing the item information like
title, item type, authors, etc. The user can also get the number of items in
the reference manager.

## 2. API

Two API are used:
[Pyzotero](https://github.com/urschrei/pyzotero/tree/v1.4.26#readme) [[1]](#1)
and [Wikimedia
](https://en.wikipedia.org/api/rest_v1/#/Citation/getCitation) [[2]](#2).

### 2.1. Pyzotero

It is a python wrapper for [Zotero Web API
v3](https://pyzotero.readthedocs.io/en/latest/#). This python package enables
users to add, delete, update and make queries about their reference management.

**Note**: The API needs a `key` and a `usr_id`. They are stored in
`zotero_helper/ddds/zotero_helper/http-service/settings.py` and imported in
`zotero_helper/ddds/zotero_helper/http-service/http_service.py`. The
`setting.py` is submitted separately via canvas.

### 2.2. Wikimedia REST API

A public API returns citation data by querying an article's identifier such as
DOI, ISBN, PMCID, arXiv, or PMID in the URL-encoded format. arXiv identifiers
are used in this project.

**Note**: the API is relatively slow for the TDM, so to avoid read time out
error, a dummy database is used that is stored under
`zotero_helper/ddds/zotero_helper/http-service/papers_db.py` and imported in
`zotero_helper/ddds/zotero_helper/http-service/http_service.py`. to use
Wikimedia API change the endpoint of `<query name="cite_info">` to
`cite_info_api`.

## 3. Data collection

The project idea is to interface with reference management software. Because
the project idea is to interact with a program, I think the best way to build a
dialogues corpus is to use a Wizard of Oz [[3]](#3). However, it is hard to
implement such a methodology in this project. I will collect the data by
transcribing several dialogues between two human participants; one plays the
software role.

### 3.1. Scenario

As discussed in [section 3](#3-data-collection), the data collection will be
through role play. As [Pyzotero](#21-pyzotero) is the main API, I have set up
the dialogues scenario based on the methods provided and the data required by
the API. The planned secnario will as follows:

#### 3.1.1. Add items manually

The user initiates the required task by expressing their intent to add an item
manually, i.e., by specifying the information for each item field, such as item
type, title, authors, etc. Because there are many fields (for example, a
journal article has 23 fields), in my project, the user will specify only four
fields: item type, title, authors, and folder. The specified by the user folder
may not exist in the database. If this is the case, the program should offer to
create a new folder for the user and add the item afterward.

#### 3.1.2. Add items using arXiv identifier

The user initiates the required task by expressing their intent to add an item
by specifing the arXiv identifier and destination folder. The specified by the
user folder may not exist in the database. If this is the case, the program
should offer to create a new folder for the user and add the item afterward.

#### 3.1.3. Query number of items

The user initiates the required task by requesting the system to count the
number of items. The user can specify a specific folder or item type or both of
them.

### 3.2. Collected material

#### 3.2.1. Add items manually

> S> Wellcome to the Zotero helper. What would you like to achieve today?
>
> U> I want to add an item with the title [aaah PAUSE aaa] A Study on Dialogue
>    Reward Prediction for Open-Ended Conversational Agents.
>
> S> Ok, good [mmm]. What is the item type?
>
> U> journal article
>
> S> Good food [mmm] What are the authors' names?
>
> U> Heriberto Cuayáhuitl, Seonghan Ryu, Donghyeon Lee, and Jihie Kim
>
> S> [mmm] ok, I assume that these names are in the first name followed
>    by last name format
>
> U> Exactly
>
> S> Ok, where do you want to add your journal article?
>
> U> Put it under reviews.
> S> Clear. Do you want to add A Study on Dialogue Reward Prediction for
>    Open-Ended Conversational Agents under reviews folder?
>
> U> yes
>
> S> I successfully added your item. Do you want anything else?
>
> U> No, thank you

#### 3.2.2. Add items using arXiv identifier

```text
S> Wellcome to the Zotero helper. What would you like to achieve today?
U> I want to add 1812.00350v1
S> Good. [aaa] Please wait while retrieving information from the internet.
S> I have found the requested paper. [aaah] Please select [PAUSE] a destination folder.
U> No specific folder [PAUSE] Just put it under my library.
S> Ok. Do you want to add [PAUSE] A Study on Dialogue Reward Prediction for
   Open-Ended Conversational Agents under your library?
U> yes
S> I successfully added your item. Do you want anything else?
U> No, thank you
```

#### 3.2.3. Query number of items

```text
S> Wellcome to the Zotero helper. What would you like to achieve today?
U> how many items do you have under the reviews folder?
S> Ok. One moment please. You have three items under reviews folder.
S> Do you want anything else?
U> No, thank you
```

### 3.3. Distillation

text

## 4. Implementation

text

## 5. Sample dialogues handled

text

## 6. Discussion

(focusing on the capabilities of your app in terms of the dialogues it can handle, and problems you have encountered; feature requests and pointing out limitations of the TDM system are very welcome!)

## 7. Future work

(that could improve the system)

## 8. Code

text

## 9. collected dialogues, distilled dialogues

text

## 10. Refrences

<a id="1">[1]</a>
Hügel, S. (2019). Pyzotero (Version 1.3.15) [Computer software].
https://doi.org/10.5281/zenodo.2917290

<a id="2">[2]</a>
Wikimedia REST API. (2021, October 16). MediaWiki, . Retrieved 14:13, December
9, 2021 from
https://www.mediawiki.org/w/index.php?title=Wikimedia_REST_API&oldid=4874352.

<a id="3">[3]</a>
Fraser, N. M., & Gilbert, G. N. (1991). Simulating speech systems. Computer Speech & Language, 5(1), 81–99. https://doi.org/10.1016/0885-2308(91)90019-M