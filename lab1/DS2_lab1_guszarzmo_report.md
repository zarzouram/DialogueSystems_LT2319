# Lab 1 Report

Mohamed Zarzoura

<br >

- [Project idea](#project-idea)
- [Dialouge 1 Distilling process](#dialouge-1-distilling-process)
  - [D1 Transcription](#d1-transcription)
  - [D1 Distilled](#d1-distilled)
  - [D1 Annotated](#d1-annotated)
- [Dialouge 2 Distilling process](#dialouge-2-distilling-process)
  - [D2 Transcription](#d2-transcription)
  - [D2 Distilled](#d2-distilled)
  - [D2 Annotated](#d2-annotated)

--- --- ---

## Project idea

The project idea is to have a system that interfaces with a reference manager
like Zotero. The System has a limitation that it is cannot retrieve data
from the paper itself as it is limited to the information shown in the
database.

<br >

## Dialouge 1 Distilling process

### D1 Transcription

The scenario is as follows: the user search for a keyword, but the system
cannot find the paper. The then, ask the system to list all the papers under a
particular folder. As they would expect, there is an item with the wrong
title, and they fix it.

  > **U.** Hello / search for a keyword /pause/ human annotated dataset
  >
  > **S.** Hello / searching / cannot find your request
  >
  > **U.** Strange / what items do you have under r /pause/ datasets folder
  >
  > **S.** I have conference paper wizard of Wikipedia /pause/ knowledge      \
  > **S.** powered conversational agents / journal article introducing man    \
  > **S.** tls a novel multi domain information seeking dialogues dataset /   \
  > **S.** a journal article dia two / a web page
  >
  > **U.** just one moment
  >
  > **S.** /pause/ yes
  >
  > **U.** let me check /pause/ ok so the dia 2 item / can you change the     \
  > **U.** title to human annotated dialogues dataset for natural             \
  > **U.** conversational  agents
  >
  > **S.** Ok dia two title changed to human annotated dialogues dataset for  \
  > **S.** natural conversational agents / do you want to change anything else
  >
  > **U.** Yes [change theee] / what is the document type again
  >
  > **S.** journal article
  >
  > **U.** ok ok [so] aah keep it /m [so can you tell] [how how] so do you    \
  > **U.** have authors how many authers do you have
  >
  > **S.** I have /pause/ four authors
  >
  > **U.** okey /pause/ good thank you

<br >

### D1 Distilled

  Below each USER-SYSTEM turns, I will provide a short description about what
  change. Also, generaly speaking, if the system turn has a hesitation or it is
  syntactically uncorrect it will be fixed.

  > **U.** Hello / search for a keyword /pause/ human annotated dataset
  >
  > **S.** Hello / let me check / Sorry I cannot find a paper that have a keyword \
  > **S.** human annotated dataset

  TURN-KEEPING: Let me check* and \
  CONFIRMATION: Repeat the keyword

  > **U.** Strange / what items do you have under r /pause/ datasets folder
  >
  > **S.** Under the dataset I have /pause/ wizard of Wikipedia knowledge     \
  > **S.** powered conversational agents /pause/ introducing man tls a novel  \
  > **S.** domain information seeking dialogues dataset /pause/ dia two       \
  > **S.** /pause/ IREM_TITLE                                           \

  Not sure how the system will behave when listing several papers. But I think
  it should go by titles only one by one with some pause between. No need to
  state the document type. Because the system will not state the document type
  the utterance *a web page* is replace by *IREM_TITLE*. It is assumed that the
  system will continue listing the items under the required folder.

  > **U.** just one moment
  >
  > **S.** yes

  Nothing changed. It is compatible with TURN-TAKING(1).

  > **U.** let me check /pause/
  >
  > **S.** Ok
  >
  > **U.** ok so the dia 2 item / can you change the title to human annotated  \
  > **U.** dialogues dataset for natural conversational agents
  >
  > **S.** Ok dia two title is changed to human annotated dialogues dataset    \
  > **S.** for natural conversational agents / do you want to change anything else

  I added a feedback from the system when the user took a time to check the
  paper. TURN-TAKING(3)
  I added *do you want to change anything else* which may contradict with
  QUANTITY(2) but I think it is needed to finish the conversation instead of
  waiting for the user's next question.

  > **U.** Yes [change theee] what is the document type
  >
  > **S.** journal article

  I removed the last word "*again*" from the user utterances. It was said because
  the system brought it up in the prevouis conversation. Currently it does not
  make sense.

  > **U.** ok ok [so aah] keep it / [so can you tell] [how how so] do you have \
  > **U.** authors how many authers do you have
  >
  > **S.** I have four authors

   Nothing changed

  > **U.** okey / good thank you
  >
  > **S.** do you need anything else
  >
  > **U.** No thank you

I added *do you need anything else?*. Such question would be ask after every
request that have been fullfilled by the system.

<br >

### D1 Annotated

```xml
  > U. <greet>Hello</greet>/
  >    <request:find>search for a <field>keyword</field> /pause/
  >       <keyword>human annotated dataset</keyword></<request>

  > S. <greet>Hello</greet>/
  >    <turn_keep>let me check</turn_keep> /
  >    <fail:find>Sorry I cannot find a </item_type>paper</item_type> that
  >       have a keyword<keyword>human annotated dataset</keyword></fail>

  > U. <feedback: ne>Strange</feedback> /
  >    <request:list_papers_folder>what items do you have under r
  >        /pause/ <folder>datasets</folder>folder</request>

  > S. <ans:list_papers_folder>Under the dataset I have /pause/
  >      <list_papers>
  >         <paper:title>wizard of Wikipedia knowledge powered conversational
  >            agents</paper>
  >         <pause>/pause/</pause>
  >         <paper:title>introducing man tls a novel domain information
  >            seeking dialoguesdataset</paper>
  >         <pause>/pause/</pause>
  >         <paper:title>dia two</paper>
  >         <pause>/pause/</pause>
  >         <paper:title>IREM_TITLE</paper>
  >      </list_papers>
  >    </ans>                                           \

  > U. <user_intercept>just one moment</user_intercept>

  > S. <feedback:pos>yes</feedback>

  > U. <kepp_turn>let me check</kepp_turn><pause>/pause/</pause>

  > S. <feedback:pos>Ok</feedback>

  > U. <request:change>ok so <change:from>the dia 2</change>
  >       item / can you change <field>the title</field> to
  >       <change:to>human annotated dialogues dataset for natural
  >       conversational agents</change></request>

  > S. <ans: change>Ok <change:from>dia two's</change>
  >       <field>>title</field>> is changed to
  >       <change:to>human annotated dialogues dataset for natural
  >       conversational agents</change></ans>
  >    <ask:goal>do you want to change anything else</ask>

  > U. <request:query>Yes [change theee] what is <field>the document
  >       type</field></request>

  > S. <ans:query>journal article</ans>

  > U. <confirmation>ok ok [so aah]</confirmation>
  >    <request:keep>keep it</request> /
  >    <request:count>[so can you tell] [how how so] do you have
  >       authors how many <field>authers</field> do you
  >       have</request>

  > S. <ans:count>I have <count>four</count> <field>authors</field>
  >       </ans>

  > U. <feedback:pos>okey / good thank you</feedback>

  > S. <ask:goal>do you need anything else</ask>

  > U. <feedback:neg>No thank you</feedback>
```

<br >

## Dialouge 2 Distilling process

### D2 Transcription

Sometimes the user likes a paper and wants to search for other papers for the
same authors. The user does not remember the full title but knows the keyword.
After finding the paper, they ask for other papers that have the same authors.
To limit the dialogue length, the user will ask about a thesis for the first
author.

  > **U.** Hello / aah please find the paper that have the key word compositionality
  >
  > **S.** Just a moment / let me check / aah yes I found two papers the first   \
  > **S.** one  is compositionality decomposed how do neural networks generalise \
  > **S.** / the second one is on the realization of compositionality in neural  \
  > **S.** networks both are journal articles
  >
  > **U.** What is the name of the first author of the first paper
  >
  > **S.** aah Hupkes [Hupkes] Dieuwke
  >
  > **U.** OK / so we have any thesis for the same author
  >
  > **S.** Yes / we have thesis titled hierarchy and interpretability in neural  \
  > **S.** models of language processing
  >
  > **U.** Yes OK thank you
  >
  > **S.** do you need anything else
  >
  > **U.** thank you

<br >

### D2 Distilled

  Below each USER-SYSTEM turns, I will provide a short description about what
  change. Also, generaly speaking, if the system turn has a hesitation or it is
  syntactically uncorrect it will be fixed.

  > **U.** Hello / aah please find the paper that have the key word compositionality
  >
  > **S.** Just a moment let me check / yes I found two papers the first one   \
  > **S.** is compositionality decomposed how do neural networks generalise    \
  > **S.** the second one is on the realizationof compositionality in neural   \
  > **S.** networks

  Remove *both are journal articles*, RELEVANCE/QUANTITY(1) the system
  presentS the required info only

  > **U.** What is the name of the first author of the first paper
  >
  > **S.** The author name is Hupkes Dieuwke

  CONFORMATION the system uses echo, implicit or explicit feedback.

  > **U.** OK / so we have any thesis for the same author
  >
  > **S.** Yes / we have a thesis titled hierarchy and interpretability in  \
  > **S.** neural models of language processing

  Nothing changed.

  > **U.** Yes OK thank you
  >
  > **S.** do you need anything else
  >
  > **U.** thank you

  Nothing changed.

<br >

### D2 Annotated

```xml
  > U. <greet>Hello</greet> / <request:find>aah please find <item_type>the
  >       paper</item> that have the <field>keyword</field>
  >       <keyword>compositionality</keyword><keyword>

  > S. <turn_keep>Just a moment let me check</turn_keep> / <ans:find>yes
  >       I found <count>two</count> <item_type>papers</item_type>
  >       <list_papers>
  >         <paper:title>the first one is compositionality decomposed how
  >            do neural networks generalise</paper>
  >         <pause>/pause/</pause>
  >         <paper:title>the second one is on the realizationof
  >            compositionality in neural  networks</paper>
  >         <pause>/pause/</pause>
  >         <paper:title>dia two</paper>
  >         <pause>/pause/</pause>
  >         <paper:title>IREM_TITLE</paper>
  >      </list_papers>
  >    </ans>

  > U. <request:query>What is <field>the name of the
  >       <list_pos>first</list_pos> <field>author</field> of the
  >       <list_pos>first</list_pos> <item>paper</item></request>

  > S. <ans>The <fields>author name</field> is Hupkes Dieuwke</ans>

  > U. <request:find>OK / so we have any <item>thesis</item> for
  >       the same <field>author</field></request>

  > S. <ans>Yes / we have a <item>thesis</item> <field:title>titled
  >       hierarchy and interpretability in neural models of language
  >       processing</field></ans>

  > U. <feedback:pos>Yes OK thank you</feedback>

  > S. <ask:goal>do you need anything else</ask>

  > U. <feedback:neg>thank you</neg>
```
