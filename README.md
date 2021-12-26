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
- [Qiita](https://qiita.com/164kondo/items/eec4d1d8fd7648217935)

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
```
# Into docker continer (python3 server)
$ docker-compose exec python3 bash

# Run python command
$ python main.py
```


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