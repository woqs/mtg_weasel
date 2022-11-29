import sqlite3
import argparse
from rich.table import Table
from rich.console import Console
from rich.style import Style
from rich.color import Color

parser = argparse.ArgumentParser(
    prog = 'MTG Weasel deck construction tool',
    description = 'Construct your deck'
)
parser.add_argument('-n', '--name', help="The deck name", required=True)
parser.add_argument('-a', '--add', help="Add a card, by its name")
parser.add_argument('-l', '--list', help="List a deck's cards", action='store_true')
parser.add_argument('-i', '--import_csv', help="Load from a CSV, give the csv name")
parser.add_argument('-D', '--delete_deck', help="Remove a deck", action='store_true')
args = parser.parse_args()

con = sqlite3.connect("decks.db", isolation_level=None)
con.row_factory = sqlite3.Row
cursor = con.cursor()

res = cursor.execute("SELECT name FROM sqlite_master")
table_names = res.fetchall()
table_names = [row["name"] for row in table_names]
deck_name = "deck_"+args.name

def createTable(cursor, deck_name):
    cursor.execute("""CREATE TABLE {} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        color_identity TEXT,
        colors TEXT,
        layout TEXT,
        legalities TEXT,
        manacost TEXT,
        manavalue INTEGER,
        name TEXT,
        printings TEXT,
        subtypes TEXT,
        supertypes TEXT,
        description TEXT,
        type TEXT,
        types TEXT,
        power INTEGER,
        toughness INTEGER
    )""".format(deck_name))

def addCardToDeck(deck_name, card_name):
    con_cards = sqlite3.connect("cards.db")
    cursor_cards = con_cards.cursor()
    cards = cursor_cards.execute("SELECT * FROM atomic_cards WHERE name LIKE \"{}%\"".format(card_name)).fetchall()
    card = None
    if len(cards) == 1:
        card = cards[0]
    else:
        for loop_card in cards:
            if loop_card[6].lower() == card_name.lower():
                card = loop_card
                break
        if card is None:
            print("card \""+card_name+"\" not found or name not precise enough")
            exit(1)
    cursor.executemany("INSERT INTO "+deck_name+"""
            (color_identity, colors, layout, legalities, manacost, manavalue, name, printings, subtypes, supertypes, description, type, types, power, toughness) 
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        [card]
    )
    print("Card "+card_name+" added Successfully in deck "+deck_name)

if args.delete_deck == False and args.import_csv is None and (table_names is None or deck_name not in table_names):
    print("Deck does not exist, creating")
    createTable(cursor, deck_name)

if args.add is not None:
    addCardToDeck(deck_name, args.add)
    exit(0)

if args.list:
    table = Table(title="Deck : "+deck_name, row_styles=["", Style(bgcolor=Color.from_rgb(40,40,40))])
    table.add_column("Name")
    table.add_column("Mana Cost")
    table.add_column("Type")
    table.add_column("Description")
    table.add_column("Body")
    for card in cursor.execute("SELECT * FROM "+deck_name):
        manacost = card["manacost"]
        for c,color in {"G": "green", "R": "red", "U": "blue", "W": "white", "B": "violet"}.items():
            manacost = manacost.replace("{"+c+"}", "["+color+"]{"+c+"}[/"+color+"]")
        table.add_row(
        card["name"],
        manacost,
        card["type"],
        card["description"],
        str(card["power"])+"/"+str(card["toughness"])
    )
    console = Console()
    console.print(table)
    exit(0)

if args.import_csv is not None or args.delete_deck:
    if deck_name in table_names:
        cursor.execute("DROP TABLE "+deck_name)
    print("Deck "+deck_name+" deleted")

if args.import_csv is not None:
    createTable(cursor, deck_name)
    import csv
    with open(args.import_csv, newline='') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            for x in range(int(row[0])):
                addCardToDeck(deck_name, row[1])
    exit(0)
exit(0)
