# Report

- [1. Introduction](#1-introduction)
- [2. API](#2-api)
  - [2.1. Pyzotero](#21-pyzotero)
  - [2.2. Wikimedia REST API](#22-wikimedia-rest-api)
- [3. Data collection](#3-data-collection)
  - [3.1. Scenario](#31-scenario)
  - [3.2. Collected material: overview, some examples](#32-collected-material-overview-some-examples)
  - [3.3. Distillation and analysis results](#33-distillation-and-analysis-results)
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

text

### 3.1. Scenario

text

### 3.2. Collected material: overview, some examples

text

### 3.3. Distillation and analysis results

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
Wikimedia REST API. (2021, October 16). MediaWiki, . Retrieved 14:13, December 9, 2021 from https://www.mediawiki.org/w/index.php?title=Wikimedia_REST_API&oldid=4874352.