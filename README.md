# Generate vocabulary list
This is for generating vocabulary list.
You can write up to 63 vocabularies for 5 mins so far


## Requirements
- [ ] Mac OS
- [ ] Google Chrome
- [ ] Google Cloud Platform
- [ ] Google Spreadsheet
- [ ] Docker
- [ ] Internet Connection


## Set up
1. Docker Container

```
$ git clone git@github.com:hellomyzn/generate-vocabulary-list.git
$ cd generate-vocabulary-list
$ docker-compose up -d --build
```

2. Google Cloud Platform
- [Google Spread Sheets に Pythonを用いてアクセスしてみた](https://qiita.com/164kondo/items/eec4d1d8fd7648217935)

3. Put Auth json Key file
Put json key you created on step2 to src/

4. Create .env file
```
$ touch backend/.env
```
```
JSONF=file name
SPREAD_SHEET_KEY=spread sheet key
SHEET_NAME=sheet name
SLEEP_TIME=0.7
```

5. Bookmark 
Save some (cambridge links)[https://dictionary.cambridge.org/] on Bookmark
Bookmark directory: /Bookmarks Bar/GVL
Edit .env file
```
# Generate Vocabulary List
BOOKMARK_NAME="GVL"
```

6. Copy Bookmarks
```
$ cp /Users/$USER/Library/Application\ Support/Google/Chrome/Default/Bookmarks ./backend/data/Bookmarks
```

7. Create an examples.txt
Create example.txt file in `data` directory so that you can write your own example sentence on GSS or CSV
```
# Format
Vacabulary1
Example Sentence1

Vacabulary2
Example Sentence2

Vacabulary3
Example Sentence3
```

8. Create a vocabularies.csv
Create vocabularies.csv file in `data` directory so that you can write vocabularies on CSV


## Usage
### Steps

1. Run Command
```
# Into docker continer (python3 server)
$ docker-compose exec python3 bash

# Run python command
$ python main.py
```

2. If you want to renew a Bookmarks file, copy it again.
![image](https://user-images.githubusercontent.com/20104403/147403426-3de72213-6211-4714-a929-f2191d4f19b2.png)

3. Press y/n for a few options

![image](https://user-images.githubusercontent.com/20104403/147403489-1eb3abad-fb46-4321-89ec-92419279551f.png)

4. Wait for proce processing
![image](https://user-images.githubusercontent.com/20104403/147403553-af042d5d-e854-4f52-b4a3-961375061bac.png)
![image](https://user-images.githubusercontent.com/20104403/147403560-fe5a3c1c-31a3-4821-a473-0257bccb94a6.png)

5. If you want to delte current Bookmarks file, press 'y'
![image](https://user-images.githubusercontent.com/20104403/147403594-82df235b-efc5-44c6-b4f6-363dc49d22f8.png)

6. If you want to edit your Bookmarks, open chrome://bookmarks/ on your google chrome browser
![image](https://user-images.githubusercontent.com/20104403/147403671-94409855-8329-45a1-9f20-46850943f5c1.png)



## Environment
Based on https://qiita.com/jhorikawa_err/items/fb9c03c0982c29c5b6d5

### Docker Command
```
# build
$ docker-compose up -d --build

# down
$ docker-compose down

# python3 server
$ docker-compose exec python3 bash

# Hello world
$ docker compose exec python3 python src/sample.py

# Ruine the world
$ docker-compose down --rmi all --volumes --remove-orphans 
```
