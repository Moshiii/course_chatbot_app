## Create virtual env
```
pip3 install virtualenv
virtualenv chatbot
```
## Activate virtual env
```
source chatbot/Scripts/activate
```

## Install packages
```
pip3 install -r requirements.txt
```
## Replace OPENAI_API_KEY in .env
replace OPENAI_API_KEY=${REPLACE_WITH_KEY}

## Run flask app
```
python app.py
```

## App run in local
login api: http://localhost:5000/api/discordLogin
test api: https://localhost:5000/api/test
logout api: http://localhost:5000/api/discordLogout
home: https://localhost:5000/


## query dynamics:


attatch some links from wiki after the answer.

focus:
based on a user input, 
first API call: the query is vecrotized and compare the cosine similarity with the context vectors
the top context will be provided along with the query to get the answer.
second API call: ask chatgpt to extract the keywords from the question and call wikipedia APi to get the page content
third API call: ask chatgpt to summerize/extract key infomation form the wiki pages

return answer fron call2 + call3


exploration :
based on a user input, 
first API call: the query is vecrotized and compare the cosine similarity with the context vectors
the top context will be provided along with the query to get the answer.
second API call: ask chatgpt to extract the top3 keywords from the respons and call wikipedia APi to get the page content
ping the link, if exist then return it.

return return answer fron call2 + call3 links




two respond style
focus vs comprehensive/exploraion 


UI interface :

chatting:
background to give a feeling of professor office/class room
or a background of professor in a laptop and a conversation interface
on the left is a professor standing up in front of a blackboard
on the right is a student raing their hand

have a feeling of in a class



landing page:
exiting technology about machanical engineering 
a picture of prof and welome message in the landing page saying well come to my office I am happy to answer you question ...

at the landing page, befor direct to the authepage. 
a popup says: in using the system,the student code of conduct apply, please do not abuse the system.

a popup says: please always refer to you study material and textbook for answer and verification of the correctness of the answer the system provides. 



