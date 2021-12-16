# Report

**Table of content**

- [1. Introduction](#1-introduction)
- [2. API](#2-api)
  - [2.1. Pyzotero](#21-pyzotero)
  - [2.2. Wikimedia REST API](#22-wikimedia-rest-api)
- [3. Data collection](#3-data-collection)
  - [3.1. Scenario](#31-scenario)
    - [3.1.1. Introduction](#311-introduction)
    - [3.1.2. Add items manually](#312-add-items-manually)
    - [3.1.3. Add items using arXiv identifier](#313-add-items-using-arxiv-identifier)
    - [3.1.4. Query number of items](#314-query-number-of-items)
  - [3.2. Collected material](#32-collected-material)
    - [3.2.1. Add items manually](#321-add-items-manually)
    - [3.2.2. Add items using arXiv identifier](#322-add-items-using-arxiv-identifier)
    - [3.2.3. Query number of items](#323-query-number-of-items)
  - [3.3. Distillation](#33-distillation)
    - [3.3.1. Introduction](#331-introduction)
    - [3.3.2. Add items manually](#332-add-items-manually)
    - [3.3.3. Add items using arXiv identifier](#333-add-items-using-arxiv-identifier)
    - [3.3.4. Query number of items](#334-query-number-of-items)
    - [3.3.5. Analysis](#335-analysis)
- [4. Implementation](#4-implementation)
  - [4.1. Add items manually](#41-add-items-manually)
  - [4.2. Add items using arXiv identifier](#42-add-items-using-arxiv-identifier)
  - [4.3. Item Add Menue based](#43-item-add-menue-based)
  - [4.4. Query number of items](#44-query-number-of-items)
- [5. Sample dialogues handled](#5-sample-dialogues-handled)
  - [5.1. Change topic from manully add to count](#51-change-topic-from-manully-add-to-count)
  - [5.2. Add by identifier to nonexisting folder](#52-add-by-identifier-to-nonexisting-folder)
  - [5.3. Count](#53-count)
- [6. Discussion](#6-discussion)
  - [6.1. Bugs](#61-bugs)
  - [6.2. Read Time out](#62-read-time-out)
  - [6.3. Sub actions](#63-sub-actions)
  - [6.4. Limitation with TDM Queries](#64-limitation-with-tdm-queries)
  - [6.5. Building of Custamizable Different Domains](#65-building-of-custamizable-different-domains)
  - [6.6. Documentaion](#66-documentaion)
- [7. Future work](#7-future-work)
- [8. Code](#8-code)
- [9. Refrences](#9-refrences)

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

#### 3.1.1. Introduction

As discussed in [section 3](#3-data-collection), the data collection will be
through role play. As [Pyzotero](#21-pyzotero) is the main API, I have set up
the dialogues scenario based on the methods provided and the data required by
the API. The planned secnario will as follows:

#### 3.1.2. Add items manually

The user initiates the required task by expressing their intent to add an item
manually, i.e., by specifying the information for each item field, such as item
type, title, authors, etc. Because there are many fields (for example, a
journal article has 23 fields), in my project, the user will specify only four
fields: item type, title, authors, and folder. The specified by the user folder
may not exist in the database. If this is the case, the program should offer to
create a new folder for the user and add the item afterward.

#### 3.1.3. Add items using arXiv identifier

The user initiates the required task by expressing their intent to add an item
by specifing the arXiv identifier and destination folder. The specified by the
user folder may not exist in the database. If this is the case, the program
should offer to create a new folder for the user and add the item afterward.

#### 3.1.4. Query number of items

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
> S> Good good [mmm] What are the authors' names?
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
>
> S> Clear. Do you want to add A Study on Dialogue Reward Prediction for
>    Open-Ended Conversational Agents under reviews folder?
>
> U> yes
>
> S> I successfully added your item. Do you want anything else?
>
> U> No, thank you

#### 3.2.2. Add items using arXiv identifier

> S> Wellcome to the Zotero helper. What would you like to achieve today?
>
> U> I want to add 1812.00350v1
>
> S> Good. [aaa] Please wait while retrieving information from the internet.\
> S> I have found the requested paper. [aaah] Please select [PAUSE] a destination folder.
>
> U> No specific folder [PAUSE] Just put it under my library.
>
> S> Ok. Do you want to add [PAUSE] A Study on Dialogue Reward Prediction for
>    Open-Ended Conversational Agents under your library?
>
> U> yes
>
> S> I successfully added your item. Do you want anything else?
>
> U> No, thank you

#### 3.2.3. Query number of items

> S> Wellcome to the Zotero helper. What would you like to achieve today?
>
> U> how many items do you have under the reviews folder?
>
> S> Ok. One moment please. You have three items under reviews folder.
>
> S> Do you want anything else?
>
> U> No, thank you

### 3.3. Distillation

#### 3.3.1. Introduction

For each `USER-SYSTEM` turns, I will provide a short description about what change. Also,
generaly speaking, if the system turn has a hesitation or it is syntactically uncorrect it will be
ﬁxed.

#### 3.3.2. Add items manually

**FUNCTIONALITY:** Setting up a custom `<greeting>` is not straightforward in
TDM. Thus I changed the custom greeting to the default TDM greeting: `What
would you like to do?`

> ~~S> Wellcome to the Zotero helper. What would you like to achieve today?~~ \
>   S> What would you like to do?
>
> U> I want to add an item with the title [aaah PAUSE aaa] A Study on Dialogue
>    Reward Prediction for Open-Ended Conversational Agents.

**RELEVANCE:** Remove unnecessary confirmation

> S> ~~Ok, good [mmm].~~What is the item type?
>
> U> journal article

**RELEVANCE:** Remove unnecessary confirmation

> S> ~~Good good [mmm]~~ What are the authors' names?
>
> U> Heriberto Cuayáhuitl, Seonghan Ryu, Donghyeon Lee, and Jihie Kim

**FUNCTIONALITY:** I removed this turn; the system will assume that the user's
formate is `First Name Last Name`. I introduce this removal to simplify the
implementation of my project. Please see [section 6.
Discussion](#6-discussion).

> ~~S> [mmm] ok, I assume that these names are in the first name followed
>    by last name format~~
>
> ~~U> Exactly~~

**RELEVANCE:** Remove unnecessary confirmation

> S> ~~Ok, ~~Where do you want to add your journal article?
>
> U> Put it under reviews.

No change

> S> Clear. Do you want to add A Study on Dialogue Reward Prediction for
>    Open-Ended Conversational Agents under reviews folder?
>
> U> yes

**FUNCTIONALITY:** TDM will handle questions asked after finishing a task or
query using its default utterances `Returning to ...` or `what do What would
you like to do?`

> S> I successfully added your item. ~~Do you want anything else?~~
>
> ~~U> No, thank you~~

#### 3.3.3. Add items using arXiv identifier

**FUNCTIONALITY:** Setting up a custom `<greeting>` is not straightforward in
TDM. Thus I changed the custom greeting to the default TDM greeting: `What
would you like to do?`

> ~~S> Wellcome to the Zotero helper. What would you like to achieve today?~~ \
>   S> What would you like to do?
>
> U> I want to add 1812.00350v1

**RELEVANCE:** Remove unnecessary confirmation

> S> ~~Good. [aaa]~~ Please wait while retrieving information from the internet.\
> S> I have found the requested paper. ~~[aaah]~~ Please select ~~[PAUSE]~~ a destination folder.
>
> U> No specific folder [PAUSE] Just put it under my library.
>
> S> ~~Ok.~~ Do you want to add ~~[PAUSE]~~ A Study on Dialogue Reward Prediction for
>    Open-Ended Conversational Agents under your library?
>
> U> yes

**FUNCTIONALITY:** TDM will handle questions asked after finishing a task or
query using its default utterances `Returning to ...` or `what do What would
you like to do?`

> S> I successfully added your item. ~~Do you want anything else?~~
>
> ~~U> No, thank you~~

#### 3.3.4. Query number of items

**FUNCTIONALITY:** Setting up a custom `<greeting>` is not straightforward in
TDM. Thus I changed the custom greeting to the default TDM greeting: `What
would you like to do?`

> ~~S> Wellcome to the Zotero helper. What would you like to achieve today?~~ \
>   S> What would you like to do?
>
> U> how many items do you have under the reviews folder?

**RELEVANCE:** Remove unnecessary confirmation

> S> ~~Ok.~~ One moment please. You have three items under reviews folder.

**FUNCTIONALITY:** TDM will handle questions asked after finishing a task or
query using its default utterances `Returning to ...` or `what do What would
you like to do?`
> ~~S> Do you want anything else?~~
>
> ~~U> No, thank you~~

#### 3.3.5. Analysis

Because the participants try to imitate a software-- not a human-- during the
role-play, the dialogues after distillation look very similar to the original
conversation.

## 4. Implementation

### 4.1. Add items manually

The user can add items manually by initiating the `add_manually` action
(`<goaltype="perform" action="add_manually">`). The associatted action in the
service interface is `AddItem`. The user should provide the system
with the required information to create an item in Zotero. Each piece of
information has a respective predicate. The system can recognize the following:

1. item type `<predicate name="typetwo" sort="record_type"/>`: Type of the item
   to be added. The system can recognize the following:
   - journal article type: `<individual name="journalArticle">`
   - Webpage type: `<individual name="webpage">`
   - Conference Paper type: `<individual name="conferencePaper">`

2. item title: `<predicate name="title" sort="item_title_info"/>`.

3. Authors' names: The system can recognize up to three authors in formate of
   `<First Name> <Last Name>`. A total of six predicates are used; three has
   sort of `<sort name="first_name" dynamic="true"/>` for the authors first
   name the other three are of sort of `<sort name="last_name" dynamic="true"/>`

4. Destination folder `<predicate name="folder_name" sort="folder_nm_str"/>`:
   The name of the folder to which the user wants to add the item.

The system asks about the predicates stated above if the user does not provide
information about them. Also, the system set other predicates to be used in
dialogue logic as follows:

1. `<predicate name="folder_id_dist" sort="folder_id_str"/>`: to determine
   whether the folder specified by the user exists; if not create a new folder
   with the same name. This predicate is set by
   `<invoke_service_query predicate="folder_id_dist" type="wh_question"/>`.
   If the predicate has a value of:
   - `noid`, then the folder name provided by the user is not found; create a
     new folder
   - `0`, **NOT IMPLEMENTED**: There is an option that the user says "use the
     current folder" so the system can use the folder name that is supposed to
     be provided in a previous stage. If the value is `0`, then the system does
     not know the current value for the predicate `folder_id_dist`
   - Otherwise, the value is the ID `folder_id` of the folder specified by the
     user.

2. `<predicate name="next_author" sort="authors_info"/>`: to determine whether
   the user wants to add more authors information. This predicate is set by
   `<invoke_service_query predicate="next_author" type="wh_question"/>`

I used another predicate for the item title
`<predicate name="item_title" sort="item_info"/>` to solve a problem that I
faced. For ore information refer to [Section 6 Discussion](#6-discussion)
for more information.

### 4.2. Add items using arXiv identifier

The user can add items by providing arXiv identifier by initiating the
`add_by_identfier` action (`<goaltype="perform" action="add_by_identfier">`).
The associatted action in the service interface is `AddItem`. The user should
provide the system with the required information to create an item in Zotero.
Each piece of information has a respective predicate.  The system can recognize
the following:

1. arXiv identifier `<predicate name="item_identifier" sort="item_info"/>`

2. Destination folder `<predicate name="folder_name" sort="folder_nm_str"/>`:
   The name of the folder to which the user wants to add the item.

The system asks about the predicates stated above if the user does not provide
information about them. When the system knows the identifier, it queries the
citation information for the provided identifier using
`<invoke_service_query predicate="cite_info" type="wh_question"/>`. It also,
set the predicate's value `<predicate name="item_title" sort="item_info"/>`
with the item title to use it in the action's `AddItem` report and preconfirm.
The logic of the dialogue related to the destination folder is the same as
discussed above.

### 4.3. Item Add Menue based

The user can go to the add item menu by initiating the `add_item` action. The
Systems will ask the user if they want to add an item manually or by providing
the identifier.

### 4.4. Query number of items

The user can call for a query to count the number of items in the whole
database or under a specific folder;
`<goal type="resolve" question_type="wh_question" predicate="count">`
the logic is as follows:

1. IF the user does not provide the item type, it is assumed the user wants to
   query about all items, regardless of their type. The respective predicate is
   `<predicate name="type" sort="record_type"/>`

2. If the user does not provide a folder name, it is assumed the user wants to
   query the whole database. The respective predicate is
   `<predicate name="type" sort="folder_name"/>`

I used other predicates like `folder_id`, `count_type`, etc. To workaround some
issues that I have faced. For more information refer to
[section 6 Discussion](#6-discussion) for more information.

## 5. Sample dialogues handled

### 5.1. Change topic from manully add to count

```text
S> What would you like to do?
U> add a journal article titled Goal Embedded Dual Hierarchical Model for Task Oriented
Dialogue Generation by Xianling Lan
S> What is the second author's first name?
U> that is it
S> Select a distination folder?
U> how many items do you have under Task Oriented
S> You have 2 records
U>
S> Returning to add an item manually. Select a distination folder?
U> Task oriented
S> Do you want to add Goal Embedded Dual Hierarchical Model for Task Oriented Dialogue
Generation to Task oriented
U> yes
S> Succssefully added Goal Embedded Dual Hierarchical Model for Task Oriented Dialogue
Generation
```

### 5.2. Add by identifier to nonexisting folder

```text
S> What would you like to do?
U> add one nine zero seven dot zero zero six eight four v one to my DM folder
S> Do you want to create DM?
U> yes
S> Succssefully created DM
U>
S> Do you want to add *
U> yes
S> Succssefully added *
```

### 5.3. Count

```text
S> What would you like to do?
U> how many articles do you have under NLU
S> You do not have any journal articles
```

## 6. Discussion

### 6.1. Bugs

text1

### 6.2. Read Time out

text

### 6.3. Sub actions

text

### 6.4. Limitation with TDM Queries

text

### 6.5. Building of Custamizable Different Domains

(focusing on the capabilities of your app in terms of the dialogues it can handle, and problems you have encountered; feature requests and pointing out limitations of the TDM system are very welcome!)

### 6.6. Documentaion

Wrong written things
Broken links
Issue with default
Compelete Example for some vague things

## 7. Future work

(that could improve the system)

## 8. Code

text

## 9. Refrences

<a id="1">[1]</a>
Hügel, S. (2019). Pyzotero (Version 1.3.15) [Computer software].
https://doi.org/10.5281/zenodo.2917290

<a id="2">[2]</a>
Wikimedia REST API. (2021, October 16). MediaWiki, . Retrieved 14:13, December
9, 2021 from
https://www.mediawiki.org/w/index.php?title=Wikimedia_REST_API&oldid=4874352.

<a id="3">[3]</a>
Fraser, N. M., & Gilbert, G. N. (1991). Simulating speech systems. Computer Speech & Language, 5(1), 81–99. https://doi.org/10.1016/0885-2308(91)90019-M