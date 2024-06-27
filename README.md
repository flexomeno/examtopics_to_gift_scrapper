# ExamTopics Scraper to GIFT Moodle format

## What is this?
This is a Python-built CLI quiz for quizzes from ExamTopics. 
It gets questions from pages (saved locally as HTML at the moment), this scrapper was designed by: https://github.com/awfulwaffle77/ExamTopicsQuizMaker

All my credits for this repo. Thanks a lot !!!!

## Saving pages
You need to download pages from your browser, I did by "Save complete page"


## How to use it

1. Create a new directory in the directory of the repository(inside ExamTopicsQuizMaker), 
named `res` 
2. CTRL+s to save the page. It has to be HTML. Save it in the `res` directory
3. Repeat for all pages in the exam

The structure of the folder should now be:

ExamTopicsQuizMaker \
&ensp;|-> 📄 convert.py \
&ensp;|-> 📄 main.py \
&ensp;|-> 📄 requirements \
&ensp;|-> 📄 _classes.py \
&ensp;|-> 📁 res \
&emsp;|-> 📄 all pages needed, in HTML format 

3. Install requirements with `pip install -r requirements`
4. Run `main.py` with `python main.py` or however your python3
command is called
5. Two files will be generated: extracted_questions_and_answers.txt and questions_in_gift_format.txt
6. Upload to your Moodle Quiz using GIFT Format