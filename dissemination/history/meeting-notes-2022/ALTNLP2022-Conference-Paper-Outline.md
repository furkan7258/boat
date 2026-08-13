# ALTNLP2022 Conference Paper Outline

# Paper Outline

It should be written, due 18.03.2022, Friday.

Issue #15. The corresponding files of the paper are in the repo, [here](https://gitlab.com/furkan.akkurt/web-annotation-tool/-/tree/main/paper/ALTNLP).

## Abstract

## Introduction

Annotation is a crucial part of Natural Language Processing. Manually annotating is an intense activity undertaken by annotators. Listening to their experiences using the first version and other annotation tools gives us ideas to implement on the tool further and make their experiences healthier.

Responses by annotators have been well for the initial application. Much feedback has been received regarding the user's experience. Some parts of the tool have been removed or altered, corresponding to the feedback. The initial feedback or tests done promise much for the future of the tool.

## Related Work

BoAT v1, Desktop version.

Other annotation tools 3rd party or ones maintained by UD.

## Desktop Modifications

Some modifications have been done to the desktop version of the tool, taking into account the users' feedback. Most modifications have to do with screen space considerations.

Categorical labels for columns have been removed from the top of the window to increase the space that can be used by the annotation table. Instead, a textbox is used specify which column to add or remove from the table. Additionally, an autocomplete feature is provided, where a user can write a column's name in the textbox in a shorthand way and the application selects the column if the provided value matches a valid column. For example, writing `depr` is enough to bring the DEPREL column, or hide.

Another autocomplete feature requested by our annotator is used in the table itself where a user can enter a value to a field and the application ensures that the entry is valid by checking the entry against all possible values. For example, writing `s` in the Number column fills the cell with `Single` immediately after entry.

A linear dependency graph from the Python library `spacy` is included instead of the previous UD graph. This is a more compact and informative graph, attested to by our annotator.

Error validation is improved by using the most recent script and data provided by the UD framework.

## Requirements and Design

First tool's requirements and new requirements that have been constructed as a result of and throughout the usage of the initial tool are here. It should be condensed and readable, not enumerated.

BoAT is a keyboard-oriented application. The annotation page includes a dependency graph and an editable table, both of which in sync. Errors are checked and annotations validated according to the UD framework and the language provided.

An annotator is able to search the corpora they are a part of to see other annotations done for that specific sentence or go to a sentence's annotation page to start annotating.

An outsider can use a particular corpus's API to get the annotations to use in their tasks in a systematic way.

## Implementation

Django, Rest Framework, PostgreSQL & Spacy (dependency graph library) are to be used.

## Features

One of the most game-changing features in this version is the ability to cross-check annotations by implementing a network for annotators where they can see the annotations done by other annotators and if they disagree on some parts, they can interact outside the tool. This can be helpful and a learning experience for annotators.

Also one other thing the interannotator agreement allows us is the possibility to see some anomalies in the Turkish part of the UD framework. For example, if a sentence were annotated a way by many annotators but the UD validation script were giving errors for it, this may indicate the UD validation is lacking in this respect of the Turkish language. Some modifications may be done, and there could be a case for a proposal of change.

### API

By using our annotated corpora API, other parties wanting to check out the capabilities of the tool can retrieve our annotated treebanks. Also, some parties wanting to use the treebanks in their computation tasks can easily extract information from our treebanks by using the API.

### Demo

A demo is [on this site](https://www.link.com) where the annotation capabilities of the tool built can be tested.

## Use Cases

Some cases where Busra uses the tool and sees response. For this, at least some of the parts has to be built.

## Discussion

What could be done further?

