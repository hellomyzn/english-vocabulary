# Generate vocabulary list
This is for generating vocabulary list.
You can write up to 26 vocabularies so far

## Requirements
- [ ] Mac OS
- [ ] Google Chrome
- [ ] Docker


## Set up
```
# build
$ git clone git@github.com:hellomyzn/generate-vocabulary-list.git
$ cd generate-vocabulary-list
$ docker-compose up -d --build
```

```
# Into docker continer (python3 server)
# 
$ docker-compose exec python3 bash
```

### Usage

```
$ python3 main.py 
```

### FYI
```
# Set symbolic link of Bookmark for Mac User
$ cp /Users/$USER/Library/Application\ Support/Google/Chrome/Default/Bookmarks backend/data/Bookmarks
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