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
