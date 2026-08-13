# Requirements Validation

[A validation meeting](https://gitlab.com/furkan.akkurt/web-annotation-tool/-/wikis/11.03.2022-15:00) has taken place. Some images had been prepared for demonstration in the meeting.

# Images

1. Log in page:

    The user `iambusra` writes their log in information and clicks `Log in`. After logging in, the user is redirected to the `Files` page.

    ![Log_in_page](uploads/28a0e5d9c0071c17302caf6d1dc95756/Log_in_page.png)

2. Files page:

    The user can see their files loaded previously here and their annotation percentages. A user can also load a file by selecting a file from a file dialog.

    ![Files_page](uploads/fbeb274b389177d45f40f9a28a674957/Files_page.png)

3. Search page:

    The user searches for `çık` by lemma in their files without checking the `Only annotated` box.

    ![Search_page](uploads/2f3750fffb2693fca74084150c90c92d/Search_page.png)

4. Search result page:

    The results of the previous search is displayed here where the user can click a sentence and go to the annotation page.

    ![Search_result_page](uploads/3296b47e78d49f6e1c89ab5b261317aa/Search_result_page.png)

5. Annotation page:

    The user can annotate the sentence here. A dependency graph and errors are displayed under the table for fields of the forms of the sentence. The user can navigate to other sentences by `Next` and `Previous` buttons, or by selecting the index of the sentence and clicking `Do`. The edits can be reset, undone or redone by their buttons. The table columns can be added or removed by the drop-down atop. The edits so far can be saved by the `Save` button.

    ![Annotation_page](uploads/1f06a5443a3bb96f2b446c09fe7385ca/Annotation_page.png)

# Results

- Requirements are mostly complete. Some alterations are still to be done, taking into account the discussion that took place.
- Some design decisions have been made as a result of the discussion in the above-mentioned meeting. The discussion has been documented [here](https://gitlab.com/furkan.akkurt/web-annotation-tool/-/wikis/11.03.2022-15:00).
