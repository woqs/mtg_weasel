# MTG Weasel

This tool comes from my personal need to be able to search for cards in the command line environment.

## Requirements

You will need to install the requirements python needs for this project with :
```
pip install -r requirements.txt
```

You will also need to download the atomic cards on the MTGJSON site [here](https://mtgjson.com/downloads/all-files/#atomiccards)

## Setup

Once the `AtomicCard.json` file downloaded, launch :
```
python initiate.py
```

This will construct the database

## Usage

### Search

```
python search.py [-n "cardName"] [-d "text in desc"] [-t "Legendary Troll"] [-c GR]
```

