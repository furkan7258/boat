# Models

# Models for the web application

## Model List

### User

#### Fields

- Username : unique
- Password

Explanation: Users of the application.

### ExtendUser

#### Fields

- User
- Preferences

### Treebank

#### Fields

- Title : unique

Explanation: Treebanks that can have sentences associated.

### Sentence

#### Fields

- Order
- Treebank
- Sentence ID
- Text
- Comments : optional

Sentence ID and Text together composite keys

### Annotation

#### Fields

- Annotator
- Sentence
- Notes : optional
- Status

### Word Line

#### Fields

- Annotation
- ID
- FORM
- LEMMA
- UPOS
- XPOS
- FEATS
- HEAD
- DEPREL
- DEPS
- MISC

## Basic Class Diagram

![DBMS_ER_diagram__UML_notation__for_BoAT](uploads/d30b209e65b95b8d312b56e84d63ec21/DBMS_ER_diagram__UML_notation__for_BoAT.png)

