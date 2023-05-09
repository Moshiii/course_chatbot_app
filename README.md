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


# deploy backend aws

# goto Moshi_credentials.csv

cd /var/tmp && sudo rm -rf * course_chatbot_app

git clone https://github.com/Moshiii/course_chatbot_app.git

sudo cp -r /var/tmp/course_chatbot_app/* /opt/chatbot

sudo systemctl restart chatbot.service

# override .env file
sudo cp -r /var/tmp/course_chatbot_app/.env /opt/chatbot

# add package 

cd /opt/chatbot
source chatbot/bin/activate
sudo pip install -r requirements.txt

# in the aws server check backend output:
sudo journalctl -u chatbot.service



# discord setup

https://discord.com/developers/applications
1. 点new application， 输入一个name， create
2.  选择oauth2，记录client id
3. client secret 选reset secret，记录下client secret
4. add redirect： https://ec2-44-212-203-117.compute-1.amazonaws.com:5000/api/discordLogin/callback
5. 登录discord，右键点server， server settings， 找到widget， copy server id
6. update CLIENT_ID, CLIENT_SECRET in https://github.com/Moshiii/course_chatbot_app/blob/main/.env
7. update group id in https://github.com/Moshiii/course_chatbot_app/blob/main/app.py#L28 with server id

## frontend deployment:
npm run build之后 用winscp copy dist 到 ec2 /var/tmp底下
然后进入aws console，ssh到 ec2
cd /usr/share/nginx/html/ && sudo rm -rf dist/ && sudo cp -r /var/tmp/dist/ .

## todo
syllbus
refuse to answer problem
domain name
pdf page


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
a popup says: In using the system,the student code of conduct apply, please do not abuse the system. Please always refer to you study material and textbook for answer and verification of the correctness of the answer the system provides. 



