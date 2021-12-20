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
  - [6.3. Limitation with TDM Queries](#63-limitation-with-tdm-queries)
  - [6.4. Building of Custamizable Different Domains](#64-building-of-custamizable-different-domains)
  - [6.5. Documentaion](#65-documentaion)
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

1. <a id="b">**Folder logic impelemtation:**</a>
   `<predicate name="folder_id_dist" sort="folder_id_str"/>`: to determine
   whether the folder specified by the user exists; if not create a new folder
   with the same name. This predicate is set by
   `<invoke_service_query predicate="folder_id_dist" type="wh_question"/>`.
   If the predicate has a value of:
   - `noid`, then the folder name provided by the user is not found; create a
     new folder
   - `0`, **NOT IMPLEMENTED**: There is an option that the user says <a id="c">*"use the
     current folder"*</a> so the system can use the folder name that is supposed to
     be provided in a previous stage. If the value is `0`, then the system does
     not know the current value for the predicate `folder_id_dist`
   - Otherwise, the value is the ID "`folder_id`" of the folder specified by the
     user.\
     See below for logic flowchart

     ![Folder Logic](https://github.com/zarzouram/DialogueSystems_LT2319/blob/main/zotero_helper/images/Add%20Item%20Logic.drawio.svg)

2. <a id="a">**Author logic implemetation:**</a>
   `<predicate name="next_author" sort="authors_info"/>`: to determine whether
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
   The name of the folder to which the user wants to add the item. The dialoge
   logic is the same as disscussed above in [Add items manually](#b)

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

**Providing Authors name Incrementally**

Below at line 12. the system asks about the first name of the third author. If
I did not provide the information in a timely matter, the system, instead of
asking `So, What is the third author's first name?` it goes for the next
question, "line 14," and it goes for infinite loop repeating the question
`What is the third author's last name?`.

This bug happen when the system asking for the second authors also. It does not
happen with the irst question.

```text
01  S> What would you like to do?
02  U> add a journal article titled Comprehensive Study How the Context Information
03  of Different Granularity Affects Dialogue State Tracking to reviews
04  S> What is the first author's first name?
05  U> Puhai
06  S> What is the first author's last name?
07  U> Yang
08  S> What is the second author's first name?
09  U> Heyan
10  S> What is the second author's last name?
11  U> Huang
12  S> What is the third author's first name?
13  U>
14  S> What is the third author's last name?
15  U> Xian-Ling
16  S> What is the third author's last name?
```

Below is the code impelemtation for the authors part, for more disscussion about
logic impelementation go to [Author logic implemetation](#a):

```xml
<findout type="wh_question" predicate="first_first_name"/>
<findout type="wh_question" predicate="first_last_name"/>
<raise type="wh_question" predicate="second_first_name"/>
<invoke_service_query predicate="next_author" type="wh_question"/>
<if>
  <condition>
    <proposition predicate="next_author" value="next"/>
  </condition>
  <then>
    <forget predicate="next_author"/>
    <findout type="wh_question" predicate="second_last_name"/>
    <raise type="wh_question" predicate="third_first_name"/>
    <invoke_service_query predicate="next_author" type="wh_question"/>
    <if>
      <condition>
        <proposition predicate="next_author" value="next"/>
      </condition>
      <then>
        <findout type="wh_question" predicate="third_last_name"/>
      </then>
    </if>
  </then>
</if>
```

**Wrong return after a preconform negation**

At line 10 below, after the user refuses to add an item it seems that the
system restarts the goal to perform `add_by_identfier` action.

```text
01  S> What would you like to do?
02  U> add one nine zero nine dot zero nine four eight four v one
03  S> Select a distination folder?
04  U> how many items do you have under NLU
05  S> You do not have any records
06  U>
07  S> Returning to add an item by identfier. Select a distination folder?
08  U> NLU
09  S> Do you want to add Generative Dialog Policy for Task-oriented Dialog Systems to NLU?
10  U> no
11  S> What identifier?
```

Below is the code impelemtation for the forder part. You can find the code
[here](https://github.com/zarzouram/DialogueSystems_LT2319/blob/c3ed8dbcfb0cbeced3e198fa33caed6c1fe66664/zotero_helper/ddds/zotero_helper/zotero_helper/domain.xml#L55-L116).For
more discussion about the dialogue logic go to [Section
4.2](#42-add-items-using-arxiv-identifier).

**Wrong Repeatetion of "AddItem" action"**

In actions `add_by_identfier`, we have mainly two paths. See [Folder logic
impelemtation](#b) and the code below:
  1. path 1: Add the item to a folder, not in the system. Thus, we create the
     folder first, then add the item.
  2. path 2: Add an item in an existing folder.

The system seems to stop after the execution of an `invoke_service_action`. No
further queries or action is executed after these points. See the red mark (1)
in the flowchart [here](#b). For this reason, I have created a `<postplan>` so
that the system will add the item after creating the missing folder (path 1).
The if block in the `<postplan>` should prevent the `AddItem` action's double
execution if the system is coming from path 2. Unfortunately, the if block does
not work, i.e., the condition is not checked, and the system executes the code
within the <then> block in all conditions. Also, if I remove the `ADDItem`
action from path-2 (so the system executes the `AddItem` action only once,
i.e., via the `<postplan>`), the system goes into an infinite loop.

If my conclusion is correct, it is preferable to be able to execute multiple
actions. It could be the case that the system needs to perform sub-actions to
complete the main action.


```xml
<plan>
  ....
  <!-- find destination folder -->
  <findout type="wh_question" predicate="folder_name"/>
  <invoke_service_query predicate="folder_id_dist" type="wh_question"/>
  <if>
    <condition>
      <!-- requested folder not found create folder -->
      <proposition predicate="folder_id_dist" value="noid"/>
    </condition>
    <then>
      <invoke_service_query predicate="folder" type="wh_question"/>
      <invoke_service_action name="CreateFolder" preconfirm="interrogative"
      postconfirm="true"/>
      <!-- No code is excuted beyond this point even after if block-->
    </then>
    <else>
      <if>
        <condition>
          <!-- current folder is not known by the system ask for the folder
          **not implemented**-->
          <proposition predicate="folder_id_dist" value="0"/>
        </condition>
        <then>
          <invoke_service_action name="Dummy" postconfirm="false"/>
        </then>
        <else>
          <invoke_service_query predicate="folder" type="wh_question"/>
          <invoke_service_action name="AddItem"
          preconfirm="interrogative" postconfirm="true"/>
          <!-- No code is excuted beyond this point even after if block-->
        </else>
      </if>
    </else>
  </if>
</plan>
<postplan>
<if>
  <condition>
  <!-- This if block does not work -->
    <proposition predicate="folder" value="created"/>
  </condition>
  <then>
    <forget predicate="folder_id_dist"/>
    <invoke_service_query predicate="folder_id_dist" type="wh_question"/>
    <invoke_service_action name="AddItem" preconfirm="interrogative" postconfirm="true"/>
  </then>
  <!-- <else>
    <invoke_service_action name="Dummy" postconfirm="false"/>
  </else> -->
</if>
</postplan>
```

### 6.2. Read Time out

As discussed in [Section 2.2. Wikimedia REST API](#22-wikimedia-rest-api), the
API is too slow for the TDM. Having a customizable time-out timer could be a
good solution.

Also, for some reason, when I ran a test for
[`interaction_tests_eng.txt`](ddds/zotero_helper/zotero_helper/test/interaction_tests_eng.txt),
I got a couple of run time errors for Zotero API; test 15 and test 16 most of
the time. In contrast, it seems that the individual test does not return such
an error. That is why I wrote
[run_individual_test.sh](./run_individual_test.sh) that loop through all tests
in the test file and individually test them. The bash script expects the test's
title to start with a two digits number.

### 6.3. Limitation with TDM Queries

TDM query cannot return multiple values, i.e. set different predicates. In our
case when the system knows an item identifier, three predicates value should be
updated. Note that for full version application at least 23 predicates need to
be updated. To overcome this issue, I used an individual query service for each
predicate to set its value. See further discussion [here](#d).

### 6.4. Building of Custamizable Different Domains

ِ[[4]](#4) discusses the benefits of the separation of domain-speciﬁc knowledge
from general dialogue capabilities. While working on my project, I found that
the separation idea could be extended, as shown below.

**Lingistic domain**
The system's utterance may contain a `Numeral + Noun` structure. The `Noun`
could be plurals or singular depending on the `Numeral`. In my implementation,
to have correct syntactic utterances, I have to have three separate predicates:
the `Numeral`, the `Noun`, and `Numeral+Noun`. Based on the value of the
`Numeral` predicate, I change the form of the `Noun` predicate and combine them
in the third predicate `Numeral+Noun`, to include them in the system
utterances.

Include such capabilities in a separate domain or the general dialogue
capabilities domain will reduce the load on the app developer. Other
considerations could be the indefinite articles, plurals, singular verbs, etc.
Also, it is possible to switch between languages with minimum changing.

<a id="d">**Dialogue Implications Domain**</a>

As discussed in [Section 6.3 Limitation with TDM
Queries](#63-limitation-with-tdm-queries), The system may change multiple
predicates depending on information received from the user. It is possible to
have a separate domain where the developer defines the rules that manage the
changes in predicates. This domain could be implemented as an extension to the
`ontology` part.

**Common Sense or Common Knowledge Domain**

Some functions are common knowledge like:

  - adding an item: the added item is new and does not exist. If it exists, ask
    for the correct information. I do not check for such a condition to
    simplify my implementation.
  - some user-provided information must be unique, like citation key and folder
    name.
  - searching for something under a folder; the folder must exist; otherwise
    asks for the correct information
  - user-provided information should be consistent; for example, the authors
    for a cerian title must be correct. Most probably, the user is wrong with
    the authors, provide them with the right authors for confirmation or wait
    for another instruction from the user like correcting the title.

There are many others rules that the user unintentionally considers when
dealing with a database manager. These rules could be categorized depending on
the field type and the task being performed, i.e., query about cite key and
create a new citation key. The few rules stated above can complicate the
implementation, especially using markup language like XML.

### 6.5. Documentaion

Issues that I faced during dealing with the documentation are listed here:

  - Under the Service Interface/Children/Parameters, there is an attribute
    called
    [Default](https://docs.talkamatic.se/dialog-domain-description-definition/service_interface/children/parameters/#default-attribute).
    However, the system does not accept this attribute and gives a "not allowed
    here" error.

  - the difinition of Invoke Service Action is written wrong it should be
    `<invoke_service_action name="alpha">` (with underscore) instead of
    `<invoke-service-action name="alpha">`. Here is the
    [link](https://docs.talkamatic.se/dialog-domain-description-definition/domain/children/invoke_service_action/).

  - Broken links:
    - `<forget>`, under the Children list in the Domain->Plan page. Here is the [link](https://docs.talkamatic.se/dialog-domain-description-definition/domain/children/forget).

    - `<jumpto>`, at the same place above. Here is the [link](https://docs.talkamatic.se/dialog-domain-description-definition/domain/children/jumpto).

  - The last two items are missing in the same list stated above

## 7. Future work

- A useful feature could be adding notes to items using google assistance or Siri.

- Extend the project to have other functions like searching for items using any fields.

- Build a multimodal menu and sun menu, including help function.

- Add other features like find similar papers using additional API like
  [Connected Paper](https://www.connectedpapers.com).

## 8. Code

Code can be found [here](./ddds/zotero_helper).

## 9. Refrences

<a id="1">[1]</a>
Hügel, S. (2019). Pyzotero (Version 1.3.15) [Computer software].
<https://doi.org/10.5281/zenodo.2917290>

<a id="2">[2]</a>
Wikimedia REST API. (2021, October 16). MediaWiki, . Retrieved 14:13, December
9, 2021 from
<https://www.mediawiki.org/w/index.php?title=Wikimedia_REST_API&oldid=4874352>.

<a id="3">[3]</a>
Fraser, N. M., & Gilbert, G. N. (1991). Simulating speech systems. Computer
Speech & Language, 5(1), 81–99. <https://doi.org/10.1016/0885-2308(91)90019-M>

<a id="4">[4]</a>
Larsson, S., & Berman, A. (2016). Domain-specific and General Syntax and Semantics in the Talkamatic Dialogue Manager. Empirical Issues in Syntax and Semantics, 11, 91–110.
