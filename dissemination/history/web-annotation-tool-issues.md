# web-annotation-tool — issues

Exported from GitLab `furkan5204/web-annotation-tool`. 140 issues.

54 open, 86 closed.

---

## ✅ #1 — Requirement Elicitation Meeting with Busra

*closed* · opened 2022-02-21 · labels: requirements

A meeting with Busra will be held on 24 Feb 2022 @ 14:00 (estimated time 1 hr). The goal is to observe the annotation process and identify the main pain points. 

This goal is to document and prioritize the main features to prepare the requirements specification. 

- [x] Prepare elicitation questions
- [x] Inspect real-time annotation by Busra (easy sentences, difficult sentences)
- [x] Select some **key reference examples** to be used in further discussions and reports
- [x] Document elicitation meeting notes and put on Wiki (under Requirements heading)

The elicitation notes taken by @uskudarli   with a meeting with @iambusra are [here](https://gitlab.com/nlpgroup1/dttddip/-/wikis/web-anno-tool)

## ✅ #2 — Create Initial Labels for Issues

*closed* · opened 2022-02-21 · labels: documentation

New labels need to be created for use in issue creation. Initial general labels would suffice for now. Later more may be added.

## ✅ #3 — Create Initial Wiki Pages for Navigation

*closed* · opened 2022-02-21 · labels: documentation

The [home page](https://gitlab.com/furkan.akkurt/web-annotation-tool/-/wikis/home) & [sidebar](https://gitlab.com/furkan.akkurt/web-annotation-tool/-/wikis/_sidebar) on Wiki were created and initialized by @furkan.akkurt. [Requirements](https://gitlab.com/furkan.akkurt/web-annotation-tool/-/wikis/Software-Requirements-Specification-(SRS)) & [Communication Plan](https://gitlab.com/furkan.akkurt/web-annotation-tool/-/wikis/Communication-Plan) pages were created but need to be filled after [the meeting](https://gitlab.com/furkan.akkurt/web-annotation-tool/-/issues/1) on 22 Feb 4 PM.

## ✅ #4 — Prepare Requirements Specification

*closed* · opened 2022-02-21 · labels: documentation

Requirements should be specified on the page for [SRS](https://gitlab.com/furkan.akkurt/web-annotation-tool/-/wikis/Software-Requirements-Specification-(SRS)) after [the meeting](https://gitlab.com/furkan.akkurt/web-annotation-tool/-/issues/1). The hard deadline for the requirements to be specified is Mar 4, 2022.

## ✅ #5 — Upload fork of the original desktop GUI application of BoAT

*closed* · opened 2022-02-28 · labels: documentation, gui

A fork of the [original application](https://github.com/boun-tabi/BoAT) should be uploaded to the repository.

## ✅ #6 — Document the new GUI fork & its usage

*closed* · opened 2022-02-28 · labels: documentation, gui

The [fork](https://gitlab.com/furkan.akkurt/web-annotation-tool/-/tree/main/src_fork) should be documented and explained as to its usage. A PDF file similar to the [_User Manual_](https://github.com/boun-tabi/BoAT/blob/master/UserManual.pdf) on the original repository may be prepared and uploaded.

## ✅ #7 — Create a glossary in SRS

*closed* · opened 2022-03-03 · labels: documentation

A glossary should be added to the [SRS](https://gitlab.com/furkan.akkurt/web-annotation-tool/-/wikis/Software-Requirements-Specification-(SRS)) describing all the terms related to the tool. Ideally, it should be ready before the SRS deadline, 4 March.

## ✅ #8 — Create barebones of annotation web page using JS

*closed* · opened 2022-03-03 · labels: design, javascript

The barebones of the main web page should be started to be written using JavaScript.

## ✅ #9 — Do SRS Final Iteration

*closed* · opened 2022-03-04 · labels: documentation, requirements

Discussed during [the meeting](https://gitlab.com/furkan.akkurt/web-annotation-tool/-/wikis/04.03.2022-15:00-Meeting-Notes), the final iteration will consist of reorganization of requirements and change of wording for specificity. Redundant requirements in different sections of the document should be minimized.

## ✅ #10 — Create known milestones

*closed* · opened 2022-03-04 · labels: documentation

Milestones that are known to have fixed dates can be documented, as discussed [here](https://gitlab.com/furkan.akkurt/web-annotation-tool/-/wikis/04.03.2022-15:00-Meeting-Notes).

## ✅ #11 — Prepare mockup images for the validation meeting

*closed* · opened 2022-03-04 · labels: design, documentation, requirements

Some mockup images of how the tool would look like should be prepared ahead of the validation meeting with @iambusra. The meeting is not set up yet but known to be soon.

## ✅ #12 — Schedule validation meeting

*closed* · opened 2022-03-06 · labels: design, documentation, requirements

A requirements validation meeting is to be scheduled where attendees are @furkan.akkurt, @uskudarli & @iambusra. Some images to convey how the tool would look like should be shown to the annotator.

## ✅ #13 — Add paper outline and template for ALTNLP2022

*closed* · opened 2022-03-11 · labels: documentation

[ALTNLP2022](https://conferences.famnit.upr.si/event/24/) template documents for the paper regarding this project should be uploaded to this repository under a new folder `Papers`.

- [x] Create a new folder under repo
- [x] Download and build paper in accordance with ALTNLP 2022 guidelines
- [x] Push to repo

## ✅ #14 — Start a Django project

*closed* · opened 2022-03-11 · labels: django, implementation

A Django project with initial configurations are to be started. The decisions are subject to change.

## ✅ #15 — Prepare Outline of ALTNLP2022 Paper

*closed* · opened 2022-03-13 · labels: altnlp2022, documentation, implementation, requirements

An outline of the ALTNLP2022 paper should be prepared. The due date is 3/18/2022.

## ✅ #16 — Add different sections for Desktop and Web version of BoAT to ALTNLP paper outline

*closed* · opened 2022-03-19 · labels: altnlp2022, documentation

Different sections for the desktop and the web version of the tool BoAT are to be included in the outline of the ALTNLP2022 paper. Then the outline is to be integrated into the main `tex` file for the paper.

## ✅ #17 — Merge branch for converting word variables to dictionaries for redundancy removal

*closed* · opened 2022-03-19 · labels: gui, implementation

A branch was created for converting word variables to dictionaries to remove redundancy and possibly improve performance in the desktop app's folder. After tests, it should be merged to `main`.

## ✅ #18 — Implement annotation model save after upload

*closed* · opened 2022-03-19 · labels: django, implementation

After uploading a `conllu` file, the annotated parts should be saved to an annotation object by the user. This decision can be changed after discussing with Busra.

## ✅ #19 — Research css frameworks for annotation table

*closed* · opened 2022-03-19 · labels: design, implementation

Table and button designs by CSS should be researched and discussed with the team before implementing for the annotation table.

## ✅ #20 — Find how to get errors from validate.py for both desktop and web versions

*closed* · opened 2022-03-20 · labels: gui, implementation

A way to get errors for a specific sentence should be found for both the desktop and the web versions of BoAT. Currently, the desktop version gets the errors by running the `validate.py` script for a conllu file that's created on the fly for a sentence and then run as a command on the shell to get the output.

## ✅ #21 — Fill 25 March meeting notes

*closed* · opened 2022-03-25 · labels: documentation

The meeting notes taken during the meeting on 25 March 3 PM should be documented in the related wiki page.

## 🔲 #22 — Find common API use cases

*opened* · opened 2022-04-03 · labels: documentation

Common API use cases are to be documented to be used in creating functions. The tool may be used alone via API calls.

## 🔲 #23 — Create new API functions for posting data

*opened* · opened 2022-04-03 · labels: API, feature, high-priority, implementation, improvement

New API functions are needed if the tool is to be used alone via API. Posting annotations, uploading files, etc. are possible uses. First common API use cases are to be documented, #22.

## ✅ #24 — Create test cases to be performed on UI

*closed* · opened 2022-04-03 · labels: documentation

The tool is to be tested out on the UI side. Test cases to perform by potential users are to be documented.

## ✅ #25 — Start dockerization of the tool

*closed* · opened 2022-04-03 · labels: implementation

Initial preparations for the eventual dockerization of the tool should be started. The tool may be divided into two, API & UI sides. 2 deployments are to be done.

## ✅ #26 — Start Project Midterm Progress Report

*closed* · opened 2022-04-04 · labels: documentation, report

The Project Midterm Progress Report should be started. LaTeX is to be used. Due 28 Apr.

## ✅ #27 — Confirm if ALTNLP Abstract is needed beforehand

*closed* · opened 2022-04-08 · labels: altnlp2022

ALTNLP Conference should be emailed for confirmation.

## ✅ #28 — Left align FEATS column in annotate view

*closed* · opened 2022-04-08 · labels: design, implementation, javascript

The column FEATS should be left aligned for ease of reading in the annotate view, currently at `annotate/<treebank_title>/<sentence_order>`

## ✅ #29 — Replace undo, redo icons with standard ones

*closed* · opened 2022-04-08 · labels: design, implementation, javascript

The icons used in the annotate view should be changed with more standard forms, like in the picture [here](https://www.google.com/url?sa=i&url=http%3A%2F%2Fsimpleicon.com%2Fundo-6.html&psig=AOvVaw0w-notnIJMu4RQ1U_fi8q-&ust=1649515366404000&source=images&cd=vfe&ved=0CAoQjRxqFwoTCOjOzd7ZhPcCFQAAAAAdAAAAABAD).

## ✅ #30 — Create visible outer border for index table in annotate view

*closed* · opened 2022-04-08 · labels: design, implementation, javascript

The index table needs a visible outer border (with minimal width possible) for ease of reading in the annotation view.

## 🔲 #31 — Fix header column of word line table

*opened* · opened 2022-04-08 · labels: design, implementation, javascript

The header column of the word line table in annotation view needs to be fixed, just like the index table above it.

## ✅ #32 — Put graph button at bottom

*closed* · opened 2022-04-08 · labels: design, implementation, javascript

The select and button for graph selection in the annotation view should be moved below the actual graph where the action takes place. The error button and its card can be treated the same.

## 🔲 #33 — Fix index table not sticking to top when scrolled to bottom of page

*opened* · opened 2022-04-08 · labels: bug, design, implementation, javascript, requirements

The index table does not stick to top when the annotation page is scrolled till the bottom of the page. This needs to be fixed.
Possible checks: This error happened when the error card and the graph were both hidden. Maybe if one of them is shown, this may not happen. Then the solution can be adding a <br> at bottom, which seems not to exist when both are hidden.

## ✅ #34 — Establish one list for graph selection in annotate.js

*closed* · opened 2022-04-08

One global graph list should be established in `annotate.js`. One place for redundancy removal would be helpful and not error-prone. The graph select would use it.

## ✅ #35 — Add cell autocomplete in annotation view

*closed* · opened 2022-04-08 · labels: implementation, javascript

In the annotation view, the cells, where it applies, should use autocomplete, like how it was implemented into the desktop application.

## ✅ #36 — Start abstract of ALTNLP Paper

*closed* · opened 2022-04-10 · labels: altnlp2022

The abstract of the ALTNLP2022 Paper should be started.

## ✅ #37 — Finish ALTNLP paper

*closed* · opened 2022-04-14 · labels: altnlp2022

The paper should be finished before the due date of 24 Apr & submitted.

## ✅ #38 — Make outer border prettier, rounder for index table in annotate view

*closed* · opened 2022-04-15 · labels: design

The border generated for the issue #30 should be made rounder.

## ✅ #39 — Fill discussion notes for meeting on 4/15

*closed* · opened 2022-04-15 · labels: documentation, meetings

The meeting notes for the meeting on 4/15 should be filled, according to the notes taken during the meeting. The notes are [here](https://gitlab.com/furkan.akkurt/web-annotation-tool/-/wikis/15.04.2022-15:00-Meeting-Notes).

## ✅ #40 — Make underscore center aligned in FEATS column

*closed* · opened 2022-04-15 · labels: design, implementation, javascript

The left alignment implemented for the issue #28 had an undesired result for the empty FEATS fields in the annotation view. The empty fields should be center-aligned.

## ✅ #41 — Make status button more compact in annotate view

*closed* · opened 2022-04-15 · labels: design, implementation

Button for changing the status of an annotation should be more compact and not make the button group atop have higher height than it would have without the status. The button has 2 lines currently for `Not finished`, etc.

## ✅ #42 — Change annotation status labels

*closed* · opened 2022-04-15 · labels: design, implementation

The labels in the annotate view for annotation status are currently `Not finished`, `Half finished`, etc. Not finished should be `Incomplete` instead. The others can be changed as seen fit.

## ✅ #43 — Change conllu.js dependency graph border from red

*closed* · opened 2022-04-15 · labels: design, implementation

The `conllu.js` dependency graph currently has red color as border. It should be changed to another color; for example, blue. It is the same color with the error card, which is not desirable.

## ✅ #44 — Make error card border green when no error exists

*closed* · opened 2022-04-15 · labels: design, implementation

When no error exists for an annotation, the validation script returns something like ```*** PASSED. ***```. When this happens the borders can be made green (for success).

## ✅ #45 — Check if UD lists are same with lists gotten from Busra

*closed* · opened 2022-04-15 · labels: UD

Busra had sent me lists for autocompletion of certain fields in the annotation table. Check if they are the same with the UD validation script. May need to speak to Busra.

## 🔲 #46 — Fix bugs in error card related to synchronization and HTML chars

*opened* · opened 2022-04-15 · labels: bug

The synchronization when fields in the annotation table are changed seems faulty. HTML chars appear in some cases. Fix this.

## 🔲 #47 — Create unit tests for backend

*opened* · opened 2022-04-15 · labels: requirements, test

Unit tests are to be written for backend (frontend also needs them but it's secondary).

An example: When annotation is saved, is the data saved to database correct? Check with a completed annotation.

## 🔲 #48 — Add annotation timer to annotation view

*opened* · opened 2022-04-15 · labels: design, implementation, javascript

A timer for starting, pausing and stopping annotations would be nice.

2 examples of usage:
- By using this timer, statistics can be calculated for a user. They could be shown in their profile.
- Annotations done for the current session can be shown in the annotation view, next to the timer. This may motivate the annotator. This may be optional.

## ✅ #49 — Fix problem of getting different list representations in annotate view, different browsers and times

*closed* · opened 2022-04-20 · labels: bug

The tool was tried on Firefox and the list for `current_columns` in the annotate view seems to have a bug. The list sent by Django to frontend needs to be split agnostic to the browser. This causes the annotation table to be faulty. Needs a fix!

## 🔲 #50 — Make it less error-prone when lemma splitting by disabling input for the split lemma

*opened* · opened 2022-04-22 · labels: implementation

When a lemma is split, 2 more lemmas are generated. The first lemma of 3 lemmas that results from this should have no input, other than ID, FORM, LEMMA and MISC fields. Input should be disabled accordingly.

## ✅ #51 — Create visible outer border for annotation table in annotate view

*closed* · opened 2022-04-22 · labels: implementation

A similar border to the one implemented for the issue #30 should be implemented for the annotation table as well. Rather than using built-in CSS techniques, bootstrap is desirable for this.

## ✅ #52 — Left-align annotation table in annotation view

*closed* · opened 2022-04-22 · labels: design

The table for annotation in the annotation view has centered text for almost all fields. FEATS have been changed to be left-aligned. During the meeting on 4/22, changing all columns to be left-aligned was agreed to be more easily legible and understandable. Actually, centering is done explicitly, removing it will solve this. Revert please.

## ✅ #53 — Detail mouse-based interaction in ALTNLP paper

*closed* · opened 2022-04-25 · labels: altnlp2022

Specific nature of mouse interaction should be detailed. Make it more clear as to why it disrupts flow.

## 🔲 #54 — Add guideline to BoAT v2

*opened* · opened 2022-04-25 · labels: dissemination, documentation, implementation

A user manual and guidelines should be prepared for the main tool in this repository, BoAT v2.

## ✅ #55 — Make it clear keyboard only usage has GUI as well in ALTNLP

*closed* · opened 2022-04-25 · labels: altnlp2022

In the paper, check if the stress on keyboard-oriented approach is over-the-top and if it insinuates there's no GUI, change it accordingly.

## ✅ #56 — Describe annotation process better in use-case in ALTNLP

*closed* · opened 2022-04-25 · labels: altnlp2022

Annotation process section can be normalized and what is typical in annotations (regarding lemma counts, splitting, etc.) can be mentioned.

## ✅ #57 — Document 22.04.2022 15:00 Meeting Discussion and Result

*closed* · opened 2022-04-29 · labels: documentation, meetings

The meeting on 22.04.2022 15:00 should be documented [here](https://gitlab.com/furkan.akkurt/web-annotation-tool/-/wikis/22.04.2022-15:00-Meeting-Notes).

## ✅ #58 — Figure  in Implementation section of ALTNLP is not easy to read

*closed* · opened 2022-04-30 · labels: altnlp2022, pr:medium

The example in Figure in implementation section is a good example. But, it is not easy to read. 
In contrast with the font of the article everything is tiny, the graph is also not readable. 

We should consider how to make it more readable.

## ✅ #59 — Reduce the size of the ALTNLP paper to fit 8 pages

*closed* · opened 2022-04-30 · labels: altnlp2022, narrative

The paper is in draft form.

But, it is getting close to the deadline. So, need to make a plan for reducing the size. 

Ideas:
- [x] Features of implementation can be described in a more condensed manner
- [ ] Although the feature format looks good, if need be they can be written as straight text. 
- [ ] Main contributions are good to outline, but they can also be written in the straight text if necessary. Last option. 
- [ ] Suzan can do a lot of general condensing of English. 2 pages ?? Getting more difficult.

## ✅ #60 — Submit ALTNLP paper

*closed* · opened 2022-04-30 · labels: altnlp2022

Submit no later than 2 May night.

[Submission link](https://easychair.org/conferences/?conf=altnlp2022)

- Check paper is 8 pages
- Pdf will be submitted.

Authors:
- Furkan  (Corresponding, if you want you can put me also, I think they allow more than one)
- Busra
- Suzan

After submission:

- [x] Preserve the version that has been submitted. It is easy for Git since all we have to do is tag it with a version.
- [x] Keep the PDF version you submitted. Store it with a timestamp (i.e. ALTNLP2022_Original_Submission_2022-05-02.pdf and load it to our repo. I think it makes sense to duplicate the whole folder. 


We keep the version so that in the future when we need to refer to it (for revision or to prepare another manuscript) we have the exact version associated with it. Revision are most common and it is important to be able to manage the process.

## ✅ #61 — Essential points to emphasize in ALTNLP paper -- from differentiation and annotator benefit perspective

*closed* · opened 2022-04-30 · labels: altnlp2022

- [ ] Its support for collaboration! Currently, **annotated datasets are very large, requiring multiple annotators**. Support for the following is very significant.
    - simultaneous annotators
    - interaction among annotators to share information about annotations 
    - comment on other annotations (We do not have this, this is a good feature to add to BoAT v2.0.
    - to be able to see how others have annotated
- [ ] The differences in annotation process for analytical vs agglutinative language
    - quantity of annotations (there simply are many more annotations)
    - nature of annotations (the way in which annotations are created is not suitable for drag and drop) [After show and tell we should be able to refine it]
- [ ] Insufficient support for annotations leads to information loss (not being able to assert some information, or that it is so difficult to do so with the tool the annotator tends not to do it).
- [ ] Speed up is remarkable
- [ ] Annotator convenience is greatly improved

## ✅ #62 — Concepts to clarify about annotation of Aggluniative Languages

*closed* · opened 2022-04-30 · labels: Clarification, altnlp2022

Note: we started talking about this with the example: **okuldakilerle**

First, understand them better. Urgently: To understand its impact on the annotation process. 

- [ ] splitting lemmas
- [ ] stacking morphemes
- [ ] syncretism  ( -ki) 
- [ ] refinement (of annotations I think)
- [ ] typology 
- [ ] In analytical languages lemmas and morphemes tend to be the same - is this true?
- [ ] Analytical languages do not have derivations and inflections. Thus feature addition is not an issue. But, they are very common for agglutinative languages, which is why a mechanism that supports a flow state is so important. Do not want to force an annotator to shift between drag and drop and keyboard interactions

## ✅ #63 — Document 29.04.2022 15:00 Meeting Discussion and Result

*closed* · opened 2022-05-01 · labels: documentation

The meeting on 29.04.2022 15:00 should be documented [here](https://gitlab.com/furkan.akkurt/web-annotation-tool/-/wikis/29.04.2022-15:00-Meeting-Notes).

## 🔲 #64 — Dockerfile should run makemigrations and migrate before running the server

*opened* · opened 2022-05-04 · labels: docker

Django image will either need to include migrations (which is not wanted) or should run `python3 manage.py makemigrations && python3 manage.py migrate` before running the server with `python3 manage.py runserver`.

## 🔲 #65 — Research and incorporate logger into the Django app

*opened* · opened 2022-05-04 · labels: bug, django, low-priority

A logger would be nice to have in the app in the development side. What's gone wrong can be seen afterwards.

## 🔲 #66 — Add feature to leave comments for someone else's annotation

*opened* · opened 2022-05-04 · labels: feature, implementation

An annotator should be able to leave comments on another annotator's annotation.

## 🔲 #67 — Improve file upload by making upload to the database transparent with respect to file size

*opened* · opened 2022-05-04 · labels: django, implementation, improvement

Currently, a `conllu` file upload takes time to process because before returning a success response, the app tries to process every sentence and add the entire parsed file to the database. The file should be checked for correct format (which is done already) and then we should return a success response. The server should then parse and upload afterwards. Django FileField should be used for this.

## 🔲 #68 — Autocomplete change/reduce for invalid entries

*opened* · opened 2022-05-04 · labels: feature, low-priority

Currently, in the annotation view, there is the autocomplete feature for which the possible entries are computed from the entry to the cell only. A nice-to-have feature would be to process the errors from the `UD` validation script and further filter the autocomplete entry list by not presenting invalid entries. This is low priority atm.

## ✅ #69 — Create new APIs for posting

*closed* · opened 2022-05-04 · labels: API, feature, implementation, improvement

Firstly, new API use cases should be determined, uses for the UI part as well as 3rd party usage outside the UI.
DRF built-in API's should be researched, they will mostly suffice us.
One use case is posting the annotation with an Ajax post to the server. Currently, Django handles it.

## 🔲 #70 — Design collaboration, create use case mockups

*opened* · opened 2022-05-04 · labels: design

Collaboration use cases should be determined and use cases should be created as mock-ups.

Two use cases:
- leaving comments for another's annotation
- referring to another's annotation to maintain consistency within treebank

## 🔲 #71 — Assign roles to annotators for better work division

*opened* · opened 2022-05-09 · labels: feature, implementation, improvement, low-priority

Role assignment can be implemented for annotators to have different roles; for instance, some annotators annotating, another one going over annotations and analyzing consistency among them.

Low priority at the moment.

## ✅ #72 — Document 10.05.2022 10:00 Meeting Discussion and Result with Busra

*closed* · opened 2022-05-11 · labels: documentation, meetings

The meeting on 10.05.2022 10:00 should be documented [here](https://gitlab.com/furkan.akkurt/web-annotation-tool/-/wikis/10.05.2022-10:00-Meeting-Notes).

## ✅ #73 — Create a work list of actions requested by reviewers of ALTNLP2022 paper

*closed* · opened 2022-05-18 · labels: altnlp2022, documentation

The paper has been accepted for the camera-ready version (May 30). A list of actions should be documented after carefully reading them.

## ✅ #74 — Create BoAT v1 section in paper

*closed* · opened 2022-05-18 · labels: altnlp2022, docker, high-priority

A section just related to BoAT v1 should be written, based on the reviews for the camera-ready version (May 30).

## ✅ #75 — Get feedback on BoAT v2 for camera-ready version of ALTNLP2022

*closed* · opened 2022-05-18 · labels: altnlp2022, docker, documentation

Feedback should be gotten from @iambusra after installing a Docker environment of the tool for the paper's camera-ready version (30 May).

## ✅ #76 — Document 5-20 meeting with uskudarli

*closed* · opened 2022-05-20 · labels: documentation

The said meeting should be documented in the wiki.

## ✅ #77 — Change keyboard shortcut to change cells in annotation view

*closed* · opened 2022-05-21 · labels: implementation

Going from one cell to an adjacent cell is done with ctrl + arrow up, down, right, left on Windows but on Mac it requires ctrl+alt+arrow unexpectedly. The shortcut should be changed. The way of moving through the table may be changed also, more similar to Excel type of style or VI (pressing a button to go in insertion mode).

## 🔲 #78 — Prevent new line in word line table's cells of annotation view

*opened* · opened 2022-05-21 · labels: implementation

Entering a new line for a cell should be disallowed.

## 🔲 #79 — Reversing a lemma split should remove residual lines in annotation view

*opened* · opened 2022-05-21 · labels: implementation

For instance, if a lemma was split previously so we have IDs 4-5, 4 and 5 in the table. Removing the row with ID 5 should remove 4-5 also.

## 🔲 #80 — Extend undo operation to include row adding, removing

*opened* · opened 2022-05-21 · labels: implementation

Undo operation should add or remove rows if they were the last operation. It reverts only cell edits currently.

## 🔲 #81 — add ability to change order of columns of word line table in annotation view

*opened* · opened 2022-05-21 · labels: feature, implementation

The word line table's columns should be reordered on request, be it keyboard or mouse.

## 🔲 #82 — Change autocomplete result order in word line table of annotation view

*opened* · opened 2022-05-21 · labels: feature, implementation

The autocomplete results should be changed to make them more user-friendly. For instance, entering N does not bring up Nom at the top. The results should take into account initials of the actual values in ordering.

## 🔲 #83 — Add ability to delete treebanks

*opened* · opened 2022-05-21 · labels: feature, implementation

User should be able to move treebanks to trash. Admin can delete them permanently.

## ✅ #84 — moving to a cell should remove underscore in word line table of annotation view

*closed* · opened 2022-05-21 · labels: implementation

Focusing on a cell in the table should immediately remove `_` underscore if the cell's value is `_`. Focusing to another from the current cell should bring back the underscore.

## 🔲 #85 — add ability to associate existing annotations with a user in a conllu file while uploading it

*opened* · opened 2022-05-21 · labels: implementation

User should be able to associate existing annotations of a conllu file with a user. Currently, a dummy user is used not to lose annotations existing in a conllu file (otherwise annotations would be created for the uploading user at the instant of upload).

## 🔲 #86 — make buttons atop more compact in annotation view

*opened* · opened 2022-05-21 · labels: feature, implementation

1 - input text for `Go to sentence` is too big.
2 - status changes move other buttons/elements, shouldn't happen.

## 🔲 #87 — add shortcut for changing status of annotation in annotation view

*opened* · opened 2022-05-21 · labels: feature, implementation

A keyboard shortcut would be handy for changing the status of an annotation (new, draft, finished).

## 🔲 #88 — fix delay of errors from validation script in annotation view

*opened* · opened 2022-05-21 · labels: bug, implementation

Errors from the UD validation script are shown delayed by 1 edit. A change in the table should immediately update the error card also, not 1 edit later.

## ✅ #89 — think and ask about xpos tag autocomplete in word line table of annotation view

*closed* · opened 2022-05-21 · labels: UD, feature, implementation

XPOS tags are not part of the UD framework. Currently, the tool has a list of XPOS tags used in our BOUN framework to list entries and present autocomplete entries for the annotator. This is a very specific list. Should think and ask to Busra about it. May remove it, or allow users to enter an XPOS list for a treebank (better).

## 🔲 #90 — Fix autocomplete feature changing actual entry to another in word line table of annotation view

*opened* · opened 2022-05-21 · labels: bug, implementation

For instance, entering `conj` to DEPREL tag and moving below with arrows changes the entry to the first entry on the autocomplete list. This is unintended, should be fixed.

## 🔲 #91 — Add language to the treebank model and use UD lists for feats, pos tags after web scraping them

*opened* · opened 2022-05-21 · labels: feature, implementation

A treebank should have a language associated. This allows many things:
- Autocomplete should be served from the lists on the UD website based on the language of the treebank, see [1](https://universaldependencies.org/u/feat/index.html) [2](https://universaldependencies.org/u/pos/index.html) [3](https://universaldependencies.org/ext-feat-index.html) [4](https://universaldependencies.org/ext-dep-index.html).
- Errors from the UD validation script require a language. Without a language, it should be called with 'ud' which is the universal tag. Language specification would hone in on the errors.

## 🔲 #92 — add dark mode based on system

*opened* · opened 2022-05-21 · labels: feature, implementation, low-priority

Dark mode of views should be added based on operating system's theme.

## 🔲 #93 — add ability to set rules for treebanks for autocomplete or new tags

*opened* · opened 2022-05-21 · labels: feature, implementation

User should be able to assign rules on a treebank basis. These rules can be assigning lists for a specific tag (e.g. XPOS) or assigning combinations that are certain to exist together in an if-and-only-if logic. For instance, in our framework, when a FORM tag is `.` and the UPOS tag is `PUNCT`, XPOS tag is definitely `Stop`. It should be possible to implement these kinds of rules for specific treebanks and automate these edits when only one possibility exists.

In line with this, ability to mass-edit should be added. Editing en masse based on some specific rule would be very convenient. For instance, change every UPOS tag to `NOUN` where the lemma is `Başak` and UPOS tag is `PROPN`.

## ✅ #94 — change absolute url paths to relative paths in entire app

*closed* · opened 2022-05-21 · labels: implementation

Some paths in the app's code use absolute paths. These should be made relative so that we can deploy the tool in any root path.

## 🔲 #95 — implement inter-annotator agreement mechanism

*opened* · opened 2022-05-21 · labels: feature, high-priority, implementation

An agreement computation mechanism should be implemented. This mechanism can have:
- selecting sentences to include in calculation,
- selecting which features to include in calculation.

## ✅ #96 — Show full names for annotations instead of usernames

*closed* · opened 2022-05-21 · labels: implementation

For instance, in the search view, users associated with annotations should be shown with full names instead of usernames.

## ✅ #97 — Ask question about `allowing to remove only necessary rows` in annotation table

*closed* · opened 2022-05-27 · labels: feature, implementation, improvement

Is it enough to remove only split-lemma rows that have `-` in their IDs? Does this cover all cases of `removing rows`? Ask this to @iambusra

## ✅ #98 — Prepare ALTNLP conference presentation draft by 5/30

*closed* · opened 2022-05-27 · labels: altnlp2022

The conference presentation's draft should be ready by 5/30. Eventual conference is on 5/7-8.

## ✅ #99 — Add BoAT v1 screenshot to appendix of ALTNLP camera-ready

*closed* · opened 2022-05-27 · labels: altnlp2022

A screenshot of BoAT v1 (the initial version, not improved recently) may be included in appendix.

## 🔲 #100 — Round inter-annotator agreement score

*opened* · opened 2022-06-14 · labels: fix

Currently, inter-annotator agreement score is left as it is after calculations. It should be rounded after analyzing the calculations to remove insignificant digits.

## 🔲 #101 — Schedule lessons learned meeting after Spring 2022 semester end

*opened* · opened 2022-06-20 · labels: high-priority, meetings

Schedule a _lessons learned_ meeting to evaluate what went right, what went wrong regarding the project, soon.

## 🔲 #102 — Gather all deliverables after Spring 2022 semester end

*opened* · opened 2022-06-20 · labels: documentation

All the deliverables produced during the semester Spring 2022 (Web tool, ALTNLP paper, project reports, requirements, etc.) should be gathered.

## 🔲 #103 — Disseminate tool after Spring 2022 semester end

*opened* · opened 2022-06-20 · labels: documentation

The tool should be publicized to test it and possibly use it in real treebanks, and also get further feedback.

User manual should be created for the current tool to make it accessible to new users.  
The linguistics department should be contacted. Furkan should present the tool to them and find opportunities of testing the tool.  
Uzbek researchers from ALTNLP2022 conference should be contacted and we should see if the tool can be used for their (future) Uzbek treebank work.

## ✅ #104 — Document 10 June Meeting

*closed* · opened 2022-06-24 · labels: documentation, meetings

The meeting [here](https://gitlab.com/furkanakkurt5204/web-annotation-tool/-/wikis/6.10.2022-3-PM-Meeting-Notes) should be documented, if it has happened.

## ✅ #105 — Document 17 June Meeting

*closed* · opened 2022-06-24 · labels: documentation, meetings

The meeting [here](https://gitlab.com/furkanakkurt5204/web-annotation-tool/-/wikis/6.17.2022-3-PM-Meeting-Notes) should be documented.

## ✅ #106 — Document 24 June Meeting

*closed* · opened 2022-06-24 · labels: documentation, meetings

The meeting [here](https://gitlab.com/furkanakkurt5204/web-annotation-tool/-/wikis/6.24.2022-3-PM-Meeting-Notes) should be documented, after it has happened.

## ✅ #107 — Refine test cases according to notes from meetings with Ms Uskudarli

*closed* · opened 2022-06-24 · labels: documentation, high-priority, meetings, test

There have been many meetings, during which the test cases were talked about. The test cases should be refined and made more specific, the notes in mind.

## 🔲 #108 — Meet Büşra for testing and scheduling events

*opened* · opened 2022-06-24 · labels: documentation, high-priority, meetings, test

Todo's for Furkan:
- [x] Meet Büşra this Sunday morning (6/26/2022).
    - [x] Test 10 sentences (speed-wise) to compare BoAT v1 and v2 & document. The dataset should be ready by then.
    - [ ] Try to schedule: An event for testing with multiple annotators (may be two sessions, one for individual testing of annotation, another for a single deployment (collaborative))
    - [ ] Try to schedule: a meeting where Furkan explains and disseminates the tool (may present the poster) to teachers (Balkız, Metin ve başka hocalar) & students from the Department of Linguistics of Boğaziçi University. Feasibility of its usage for an endangered language's (e.g. Laz) treebank creation to be discussed.

## 🔲 #109 — Change names of files of the repo

*opened* · opened 2022-06-24 · labels: documentation

Many names of the files in the repo are context-dependent. Names like `Poster.pdf` should be changed as to reflect what they are files of, by just their names. `Poster.pdf` can be changed to `BoAT-CMPE492-Senior-Project-Poster.pdf`.

## 🔲 #110 — Add indicator for when a sentence is edited but not saved

*opened* · opened 2022-06-24 · labels: feature, implementation, improvement

Add an indicator that shows an annotation of a sentence has been edited in the annotation page, but not saved yet; just like text editors.

## 🔲 #111 — Learn unit tests and explain

*opened* · opened 2022-06-24 · labels: test

Should learn what a unit test is and explain to Ms Uskudarli.

## 🔲 #112 — Add ability to proceed from last session

*opened* · opened 2022-06-24 · labels: feature, improvement

Add ability to proceed from the last session's sentence last annotated, as mentioned in the [meeting](https://gitlab.com/furkanakkurt5204/web-annotation-tool/-/wikis/6.19.2022-11-AM-Meeting-Notes).

## 🔲 #113 — Add ability to import annotations

*opened* · opened 2022-06-24 · labels: feature, implementation, improvement

Add ability to import annotations for a certain user, as mentioned in the [meeting](https://gitlab.com/furkanakkurt5204/web-annotation-tool/-/wikis/6.19.2022-11-AM-Meeting-Notes).

## 🔲 #114 — Improve glossary in wiki

*opened* · opened 2022-06-25 · labels: dissemination, documentation

The [glossary page](https://gitlab.com/furkanakkurt5204/web-annotation-tool/-/wikis/Glossary) should be improved and extended to include many more technical and linguistic aspects of the annotation tool _BoAT_.

## ✅ #115 — Registering to the system, test case

*closed* · opened 2022-06-25 · labels: test

In this test case, an annotator should be able to register to the system from scratch, entering their username, first name, last name, email address and password.

## ✅ #116 — Logging in to the system as the registered user, test case

*closed* · opened 2022-06-25 · labels: test

In this test case, an annotator is expected to log in to the system with the credentials of the registration in #115.

## ✅ #117 — Uploading a file, test case

*closed* · opened 2022-06-25 · labels: test

In this test case, an annotator is expected to upload a `conllu` file to the system.

## ✅ #118 — Going to a sentence, test case

*closed* · opened 2022-06-25 · labels: test

In this test case, an annotator is expected to go to a sentence's annotation page.

## ✅ #119 — Annotating a sentence, test case

*closed* · opened 2022-06-25 · labels: test

In this test case, an annotator is expected to annotate several sentences.  
This case is split into subcases:
- Simple
- Complex
- Splitting a *form*

## ✅ #120 — See own annotations, test case

*closed* · opened 2022-06-25 · labels: test

In this test case, an annotator is expected to check their own annotations and filter by their statuses.

## ✅ #121 — Search annotations based on criteria chosen, test case

*closed* · opened 2022-06-25 · labels: test

In this test case, an annotator is expected to search annotations of a treebank. Some criteria should be determined for them to do this search.

## ✅ #122 — Exporting a treebank, test case

*closed* · opened 2022-06-25 · labels: test

In this test case, an annotator is expected to export a treebank, in the _UD_ format. The treebank name should be determined.

## ✅ #123 — Creating a treebank, test case

*closed* · opened 2022-06-25 · labels: test

In this test case, an annotator is expected to create a treebank by providing a unique name for it.

## ✅ #124 — Showing a column, test case

*closed* · opened 2022-06-25 · labels: test

In this test case, an annotator is expected to show a hidden column in the annotation page. Some hidden columns are expected to be shown on request to conveniently annotate the tags of those columns.

## ✅ #125 — Saving an annotation, test case

*closed* · opened 2022-06-25 · labels: test

In this test case, an annotator is expected to save an annotation of a sentence.

## ✅ #126 — Specify username and passwords in test case for registration & log in

*closed* · opened 2022-06-26 · labels: test

In the test cases of registration and log in, usernames and passwords are left to the annotator currently. They should be specified since in local deployments for every annotator, everyone can have the same credentials. For collaborative cases, credentials should be given separately but still specified.

## 🔲 #127 — Create collaborative test cases

*opened* · opened 2022-06-26 · labels: test

Collaborative test cases should be created.

## 🔲 #128 — Fill checklist of things we want to test during the user acceptance tests

*opened* · opened 2022-06-26 · labels: test

The checklist should be filled and matched with the cases that test those things, [link](https://gitlab.com/furkanakkurt5204/web-annotation-tool/-/wikis/User-Acceptance-Tests).

## 🔲 #129 — Combine treebank pages into a dropdown in navbar and condense

*opened* · opened 2022-06-27 · labels: implementation, improvement

There are many pages related to treebanks in general. These pages can be made into a dropdown: Create, View, Compute.

## 🔲 #130 — Remove graph select's apply button, like status

*opened* · opened 2022-06-27 · labels: implementation, improvement

The apply button (`tick`) should be removed, just like the status dropdown.

## 🔲 #131 — Add stripes to annotation table

*opened* · opened 2022-06-27 · labels: implementation, improvement, visualization

The annotation table can be striped, like other tables (e.g. search results) for better visualization.

## 🔲 #132 — Add color to cells of annotation table

*opened* · opened 2022-06-27 · labels: implementation, improvement, visualization

Cells of different tags in the annotation table can be colored, like the GitHub `conllu` file example below, taken from [here](https://github.com/UniversalDependencies/UD_Turkish-Atis/blob/master/tr_atis-ud-test.conllu):
![image](/uploads/15c09697a6550897840563d88de10866/image.png)
Another kind of colorization may be nicer; where, for example, `UPOS` & `XPOS` colored same (categorization).

## 🔲 #133 — Change reset icon in annotation page

*opened* · opened 2022-06-27 · labels: implementation, improvement, visualization

Reset icon does not look representative of its action. It should be changed for the better.

## 🔲 #134 — Add statistics to annotator profile

*opened* · opened 2022-06-27 · labels: implementation, improvement, visualization

Annotator profile page is empty currently. There should be statistics added there, like how many annotations done (recently / all time); visualization of statistics is important (charts, etc.). A profile page may be added as well.

## 🔲 #135 — Discuss automation of annotation status

*opened* · opened 2022-06-27 · labels: annotation, improvement

Annotation status is currently set by annotators manually. Automation of it should be discussed w/ Büşra & Ms Uskudarli.

## 🔲 #136 — Add shortcuts (Enter) for entering an input

*opened* · opened 2022-07-18 · labels: improvement

Entering inputs require applying the input by a button, a shortcut of `Enter` can be supplied. This is a feedback from a non-linguist that participated in the recent testing.

## 🔲 #137 — Show sentence orders in a treebank in viewing treebanks page

*opened* · opened 2022-07-18 · labels: improvement

Sentence orders can be shown in viewing treebanks view. This is a feedback from a non-linguist that participated in the recent testing.

## ✅ #138 — Document recent test cases (July 2022)

*closed* · opened 2022-07-18 · labels: documentation, test

User acceptance tests are being conducted recently, the results and feedback should be documented.

## ✅ #139 — Change pasting, remove styles, only plain text

*closed* · opened 2022-07-25 · labels: bug, implementation, improvement, test

When a text is pasted, the style is copied directly. Need to change the pasting functionality as plain text.

Can see the effect in [Annotator 3's test cases](https://docs.google.com/document/d/14uZFW8-0JctMlmw31hUY89zF4Osr6HZcFVpA8Y2buy8).

## 🔲 #140 — Read Olcay Hoca's paper related to our tool

*opened* · opened 2022-10-16 · labels: high-priority, reading

Olcay Hoca's recent paper related to our tool should be read.
