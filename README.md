# Automatic Health Check
Fill out the ASU health check automatically! 

## How it works
This script will log into your ASU account with Firefox and fill out the "none," "none" options on the survey completely hands free! You can go even further by automating this script to run in the background of your computer (assuming that you're healthy). Minimal installation with some command line interface!

## Requirements
- Firefox browser
- The latest verson of python
  - Python libraries from the requirements package
- Geckodriver for HTTP Requests 

## Install

```pip
pip install -r requirements.txt
```

Linux:
```npm
npm install geckodriver
```

macOS (brew):
```brew
brew install geckodriver
```

Windows:
```link
https://github.com/mozilla/geckodriver/releases
```

## Usage 

```python
python main.py
```

## Disclosure
Please only use this script if you are 100% healthy and already know the answer is "none," "none" meaning that you have no symptoms and are feeling well. (Please don't sue me lol)
