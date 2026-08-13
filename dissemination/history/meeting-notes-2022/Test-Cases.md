# Test Cases

# Test Cases

This page is being written currently, #107.

These tests should be under the domain: `https://URL`, used with the variable `$domain`.

## Test case columns:

- Step: step number
- Action: action to be taken for the step
- Data: data required to act on the step
- Expected: what is the expected outcome of the step
- Actual: what actually happened after the action
- Comments: miscellaneous information

## 1. Registering to the system

| Step | Action | Data | Expected | Actual | Comments |
|-|-|-|-|-|-|
| 1 | Go to the registration page | URL to go to: `$domain/accounts/register` | The page is loaded.  <br><br> ![image](uploads/44cd15e70ab645e7a19289458288c8ae/image.png) |  |  |
| 2 | Enter credentials | Username: [Your first name written without spaces]<br>First Name: [Your first name here]<br>Last Name: [Your last name here]<br>Email Address: [Your email address here]<br>Password & Password again: [A password you choose] | An example is given below. The fields should be filled with your data. <br> ![image](uploads/d575a2ed6f13a98349592b53bdf502bf/image.png) |  |  |
| 3 | Click _Register_ |  | You are registered and redirected to the url `$domain/accounts/login`. <br><br> ![image](uploads/e812fdd6c7f4b63b786e40eec4e51055/image.png) |  |  |

## 2. Logging in to the system as the registered user

### 2.1 Preconditions

- You need to be registered. The previous test case should help with this.

| Step | Action | Data | Expected | Actual | Comments |
|-|-|-|-|-|-|
| 1 | Go to the log in page | URL to go to: `$domain/accounts/login` | The page is loaded. <br> ![image](uploads/e812fdd6c7f4b63b786e40eec4e51055/image.png) |  |  |
| 2 | Enter credentials | Username: [Your username you had chosen while registering]<br>Password: [The password you had chosen while registering] | An example is given below. The fields should be filled with your data. <br> ![image](uploads/f8a0ac53b63b70577aef2b966ec7bdb3/image.png) |  |  |
| 3 | Click _Log in_ |  | You are logged in and redirected to the url `$domain/accounts/home`. |  |  |

## 3. Creating a treebank

### 3.1 Preconditions

- You must be logged in.

| Step | Action | Data | Expected | Actual | Comments |
|-|-|-|-|-|-|
| 1 | Go to the treebank creation page | URL to go to: `$domain/create_treebank` | The page is loaded. <br> ![image](uploads/a32a049e68c1a391253c3428aaf8144f/image.png) |  |  |
| 2 | Enter the treebank name | The treebank name is: _Turkish\_Bank_ | ![image](uploads/52f7b2d8a1e0a932221e5a1b88127ebd/image.png) |  |  |
| 3 | Click _Create_ |  | You have created the treebank and seen the message: <br> _You have created a treebank successfully._ <br><br> ![image](uploads/db8e6757a16932fd111afa0cbed234fe/image.png) |  |  |

## 4. Uploading a file

### 4.1 Preconditions

- You must be logged in.
- At least one treebank must have been created.

| Step | Action | Data | Expected | Actual | Comments |
|-|-|-|-|-|-|
| 1 | Go to the file upload page | URL to go to: `$domain/upload_file` | The page is loaded. <br> ![image](uploads/7cf410262dac51f1ffa6cbd8738e08d0/image.png) |  |  |
| 2 | Select a treebank to upload to | The treebank name is: _Turkish\_Bank_ (created in the test case named _Creating a treebank_) | The treebank's title is seen as selected in the dropdown below `Choose a treebank to upload to:`. |  |  |
| 3 | Click `Choose File` |  | A file dialog opens up. |  |  |
| 4 | `Open` a file | A `conllu` format file should be chosen. For this test case, a file is provided in the `Test Cases/test_case_1.conllu` path of this project's repository. | The filename appears instead of `No file chosen`. <br> ![image](uploads/54c548527ba6d3e655fc0a327abfbaa7/image.png) |  |  |
| 5 | Click _Upload_ |  | `You have uploaded a file successfully.` message should be seen. <br> ![image](uploads/39a18160c8b348db2d9714fd7ec2eeda/image.png) |  |  |

## 5. Going to a sentence

### 5.1 Preconditions

- You must be logged in.

| Step | Action | Data | Expected | Actual | Comments |
|-|-|-|-|-|-|
| 1 | Go to the treebank viewing page | URL to go to: `$domain/view_treebanks` | The page is loaded. <br> ![image](uploads/03fb0fbb49af1267e5f25669c43effbf/image.png) |  |  |
| 2 | Click _View Sentences_ beside a treebank to view its sentences | The treebank name is: _Turkish\_Bank_ (created in the test case named _Creating a treebank_ and that has been uploaded sentences in the test case named _Uploading a file_) | You are redirected to the url `$domain/view_treebank/Turkish_Bank/` and see the screen below: <br> ![image](uploads/4e483a0ec0bbba0cfbb17ea06d74fb2a/image.png) |  |  |
| 3 | Click the pen icon beside a sentence to go to its annotation page | The sentence situated at the topmost, with the `sent_id` _ins\_833_. | You are redirected to the url `$domain/annotate/Turkish_Bank/1` and see the screen below: <br> ![image](uploads/cac619d8b91e3aca52b8b7e02bcc814d/image.png) |  |  |
| 4 | Enter the sentence number to go to in the text field beside the dropdown that has _Go to sentence_ as selected | The sentence number being the one given in a test case | It should look like the example below, `32` the number in this case: <br> ![image](uploads/da7048035763db3cf605e672f5ffa750/image.png) |  |  |
| 5 | Click the tick to the right of the above-mentioned dropdown |  | You are redirected to the url `$domain/annotate/Turkish_Bank/32`, 32 being the number given to the dropdown: <br> ![image](uploads/705f162e0c647d1f08e3074406fe487b/image.png)  |  |  |

## 6. Showing a column

This specific case will test showing a hidden column named `Case` but can be used in general for any column.

### 6.1 Preconditions

- You must be logged in.
- You need to go to the sentence to be annotated by using the information in the test case `Going to a sentence`.

| Step | Action | Data | Expected | Actual | Comments |
|-|-|-|-|-|-|
| 1 | Go to the first sentence given in the data. The test case named _Going to a sentence_ should help with this. | the sentence number: 1 | You should be in the annotation page of the first sentence in the treebank _Turkish\_Bank_. <br> ![image](uploads/cac619d8b91e3aca52b8b7e02bcc814d/image.png) |  |  |
| 2 | Click the dropdown that has `Columns` as selected |  | ![image](uploads/7b5ac92192cab9981bf23e08f08c4766/image.png) |  |  |
| 3 | Click the column in the dropdown | the column: `Case` | ![image](uploads/c20e650b1f55dab18ef78dabbab0d5b3/image.png) |  |  |
| 4 | Click the tick beside the dropdown |  | The hidden column is now shown. <br> ![image](uploads/1c511695c778c4958d6125295c230f65/image.png) |  |  |

## 7. Saving an annotation

This case will test saving an annotation.

### 7.1 Preconditions

- You must be logged in.
- You need to go to the sentence to be annotated by using the information in the test case `Going to a sentence`.

| Step | Action | Data | Expected | Actual | Comments |
|-|-|-|-|-|-|
| 1 | Go to the first sentence given in the data. The test case named _Going to a sentence_ should help with this. | the sentence number: 1 | You should be in the annotation page of the first sentence in the treebank _Turkish\_Bank_. <br> ![image](uploads/cac619d8b91e3aca52b8b7e02bcc814d/image.png) |  |  |
| 2 | Click the button for saving an annotation | The icon of the button: <br> ![image](uploads/487b048271d44214937d1d11cd1b9ebf/image.png) <br><br> The place of the icon in the annotation page: <br> ![image](uploads/93bf963a3044300b7eef8cff6f099ce8/image.png) | You are redirected to the same annotation page after the annotation having been saved. The edits before saving should be seen in the annotation table. |  |  |

## 7. Annotating a sentence

<!-- come to same page after annotation to see it's been saved -->

### 7.1 Preconditions

- You must be logged in.
- You need to go to the sentence to be annotated by using the information in the test case `Going to a sentence`.

There are 3 different iterations for this test case, based on complexity of the sentences. They are: _simple_, _complex_ & _splitting a form_.

### 1. Simple

The text for this sentence:
> O hanımı asistan yaptılar.

| Step | Action | Data | Expected | Actual | Comments |
|-|-|-|-|-|-|
| 1 | Go to the 36th sentence of the treebank Turkish_Bank | The sentence number is _36_. | The annotation page is loaded with the mentioned sentence. <br> ![image](uploads/84687bdfce6cc80a6723a85474a000a4/image.png) |  |  |
| 2 | Edit `UPOS` of the 2nd form `hanımı` | `hanımı`'s `UPOS`: `NOUN | The cell for the edit is now filled. <br> ![image](uploads/51e811ecd035ddbc2a2c0f3a89d4085d/image.png) |  |  |
| 3 | Show the column `Case` (the test case named `Showing a column` can help with this.) | the column: `Case` | The column is now shown. <br> ![image](uploads/97592a21147e597efdebbb5d7de22c81/image.png) |  |  |
| 4 | Edit `Case` of the 2nd form `hanımı` | `hanımı`'s `Case`: `Nom` | The cell for the edit is now filled. <br> ![image](uploads/412bf80b241e0746f7ad20568fa7daae/image.png) |  |  |
| 5 | Show the column `Aspect` (the test case named `Showing a column` can help with this.) | the column: `Aspect` | The column is now shown. <br> ![image](uploads/8d76d700c03e4190dd4ae8aa542abed1/image.png) |  |  |
| 6 | Edit `Aspect` of the 4th form `yaptılar` | `yaptılar`'s `Aspect`: `Perf` | The column is now shown. <br> ![image](uploads/01dd8837747d53c49ab4a4f400eca16d/image.png) |  |  |
| 7 | Save the annotation. The test case named _Saving an annotation_ can help with this. | You are redirected to the same annotation page after the annotation having been saved. The edits before saving should be seen in the annotation table. |  |  |  |

1. `Ctrl`/`cmd` with arrows can be used to move between cells.
2. The edits to complete the annotation is: The 2nd form's `UPOS` should be `NOUN` and its `Case` should be `Nom`. The 4th form should have `Perf` as `Aspect` in `FEATS`. The 5th form should have 4 as `HEAD`.

### 2. Complex

Coming from the previous _simple_ annotation test case, now the columns _Case_ and _Aspect_ are open for other annotations, if not hidden otherwise.

The text for this sentence:
> Araştırmada yöneltilen "Sosyal güvenlik sistemi hakkında bilginiz var mı?" sorusuna ise, iş değiştirmeyi düşünenlerin yüzde 58'i "evet" yanıtı verirken, iş arayan katılımcılarda bu oran yüzde 54'te kaldı.

| Step | Action | Data | Expected | Actual | Comments |
|-|-|-|-|-|-|
| 1 | Go to the 128th sentence of the treebank Turkish_Bank | The sentence number is _128_. | The annotation page is loaded with the mentioned sentence. <br> ![image](uploads/2ac7b7ab65944b54f6714deb119ddd7c/image.png) |  |  |
| 2 | Edit `DEPREL` of the 3rd form `"` | `"`'s `DEPREL`: `punct` | The cell for the edit is now filled. |  |  |
| 3 | Edit `DEPREL` of the 8th form `bilginiz` | `bilginiz`'s `DEPREL`: `nsubj` | The cell for the edit is now filled. |  |  |
| 4 | Edit `Case` of the 18th form `düşünenlerin` | `düşünenlerin`'s `Case`: `Gen` | The cell for the edit is now filled. |  |  |
| 5 | Show the column `Person` (the test case named `Showing a column` can help with this.) | the column: `Person` | The column is now shown. |  |  |
| 6 | Edit `Person` of the 19th form `yüzde` | `yüzde`'s `Person`: `3` | The cell for the edit is now filled. |  |  |
| 7 | Show the column `Tense` (the test case named `Showing a column` can help with this.) | the column: `Tense` | The column is now shown. |  |  |
| 8 | Edit `Tense` of the 29th form `arayan` | `arayan`'s `Tense`: `Pres` | The cell for the edit is now filled. |  |  |
| 9 | Show the column `Evident` (the test case named `Showing a column` can help with this.) | the column: `Evident` | The column is now shown. |  |  |
| 10 | Edit `Evident` of the 30th form `katılımcılarda` | `katılımcılarda`'s `Evident`: `Fh` | The cell for the edit is now filled. |  |  |
| 11 | Save the annotation. The test case named _Saving an annotation_ can help with this. | You are redirected to the same annotation page after the annotation having been saved. The edits before saving should be seen in the annotation table. |  |  |  |

1. `Ctrl`/`cmd` with arrows can be used to move between cells.
2. The edits to complete the annotation is: The 3rd form should have `punct` as its `DEPREL`. The 8th form should have `nsubj` as its `DEPREL`. The 18th form should have `Gen` as its `Case` in `FEATS`. The 19th form should have `3` as `Person` in `FEATS`. The 29th form should have `Pres` as `Tense` in `FEATS`. The 30th form should have `Fh` as `Evident` in `FEATS`.

### 3. Splitting a _form_

The text for this sentence:
> "Unutulan değerlerimize sahip çıkalım" haftası etkinlikleri çerçevesinde Arkeoloji Müzesi'nde düzenlenen konferansta kentliler atalarının davranış biçimlerinin detaylarını öğrenirken hayranlıklarını gizleyemediler.

| Step | Action | Data | Expected | Actual | Comments |
|-|-|-|-|-|-|
| 1 | Go to the 104th sentence of the treebank Turkish_Bank | The sentence number is _104_. | The annotation page is loaded with the mentioned sentence. |  |  |
| 2 | Click on a cell on the row of the 19th form `öğrenirken` | the form: the 19th form `öğrenirken` |  |  |  |
| 3 | Enter keyboard shortcut `shift + alt + down arrow` together to create a row under the 19th form | the keyboard shortcut: `shift + alt + down arrow` together | There are extra two rows created below the 19th form. The lemma has been split. <br> ![image](uploads/1158645f722893073326b48c0352d624/image.png) |  |  |
| 4 | Annotate according to **3** below | the annotation data: **3** footnote below | The annotation has been completed. |  |  |
| 5 | Save the annotation. The test case named _Saving an annotation_ can help with this. | You are redirected to the same annotation page after the annotation having been saved. The edits before saving should be seen in the annotation table. |  |  |  |

1. `Ctrl`/`cmd` with arrows can be used to move between cells.
2. `Shift`, `Alt` and the down arrow together can be used to create a row under a certain row when focused on a cell within the row.
3.
- 19 öğrenir öğren VERB Ptcp Aspect=Hab|Polarity=Pos|Tense=Pres|VerbForm=Part 22 advcl \_ \_
- 20 ken y AUX Zero Polarity=Pos|VerbForm=Conv 19 cop \_ \_

## 8. See own annotations

### 8.1 Preconditions

- You must be logged in.

| Step | Action | Data | Expected | Actual | Comments |
|-|-|-|-|-|-|
| 1 | Go to page showing your annotations | URL to go to: `$domain/my_annotations/` | The page is loaded. <br> ![image](uploads/41d03670c5bed619cc0f092cafc124fa/image.png) |  |  |
| 2 | Select `All` in the dropdown. | selection: `All` | All the annotations should be listed. <br> ![image](uploads/d8afbbc8cdc9421c9c762847acbedf5f/image.png) |  |  |

## 9. Search annotations based on criteria chosen

### 9.1 Preconditions

- You must be logged in.

| Step | Action | Data | Expected | Actual | Comments |
|-|-|-|-|-|-|
| 1 | Go to the search page | URL to go to: `$domain/search/` | The page is loaded. <br> ![image](uploads/f2218b94ac8033c2bbb0e76705067efe/image.png) |  |  |
| 2 | Select the treebank in the dropdown | the treebank: _Turkish\_Bank_ | The treebank has now been selected. <br> ![image](uploads/fa404fdb42b64499a6b407e4097ffcd8/image.png) |  |  |
| 3 | Select _Field_ as `UPOS`. | the field: `UPOS` | ![image](uploads/31d26ebd23e0b7cc85f6fd04c7dac135/image.png) |  |  |
| 4 | Enter _Query_ of the field `UPOS` as `NOUN`. | the query: `NOUN` | ![image](uploads/52042c550505c67c4d177206c77f7fd8/image.png) |  |  |
| 5 | Click the + (plus) button beside `Query` | `+` button | There should be another query and field added below the initial query. <br> ![image](uploads/255536dc748bf6544a65a9da6493e10c/image.png) |  |  |
| 6 | Select the empty _Field_ as `DEPREL`. | the field: `DEPREL` | ![image](uploads/26f6b9debf1d2ff4543a62f9745d9aa7/image.png) |  |  |
| 7 | Enter _Query_ of the field `DEPREL` as `nmod`. | the query: `nmod` | ![image](uploads/4e31aa2f8c6db057c349db6d28ad7740/image.png) |  |  |
| 8 | Click the `Search` button |  | The results should be listed as: <br> 90 results found. <br> Query was upos: NOUN, deprel: nmod in the treebank _Turkish\_Bank_ <br> ![image](uploads/e808e98d88eec6914fc8ddf63b4d6186/image.png) |  |  |

1. `+` can be used to expand the query into multiple categories.

## 10. Exporting a treebank

### 10.1 Preconditions

- You must be logged in.
- The treebank to be exported must exist.

| Step | Action | Data | Expected | Actual | Comments |
|-|-|-|-|-|-|
| 1 | Go to the treebank viewing page | URL to go to: `$domain/view_treebanks/` | The page is loaded. <br> ![image](uploads/b8b7cfeea4e619408973f7fdfadc8a9c/image.png) |  |  |
| 2 | Click `Download` in the row of the treebank requested | the treebank: _Turkish\_Bank_ | The file should be downloaded in the `conllu` format of _UD_ to your local computer system. <br>  |  |  |

