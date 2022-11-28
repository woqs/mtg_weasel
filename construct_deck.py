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
parser.add_argument('-i', '--import_csv', help="Load from a CSV")
args = parser.parse_args()

con = sqlite3.connect("decks.db", isolation_level=None)
con.row_factory = sqlite3.Row
cursor = con.cursor()

res = cursor.execute("SELECT name FROM sqlite_master")
table_names = res.fetchone()
deck_name = "deck_"+args.name
if table_names is None or deck_name not in table_names:
    print("Deck does not exist, creating")
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

if args.add is not None:
    con_cards = sqlite3.connect("cards.db")
    cursor_cards = con_cards.cursor()
    cards = cursor_cards.execute("SELECT * FROM atomic_cards WHERE name LIKE \"{}%\"".format(args.add)).fetchall()
    card = None
    if len(cards) == 1:
        card = cards[0]
    else:
        for loop_card in cards:
            if loop_card[6].lower() == args.add.lower():
                card = loop_card
                break
        if card is None:
            print("card \""+args.add+"\" not found or name not precise enough")
            exit(1)
    cursor.executemany("INSERT INTO "+deck_name+"""
            (color_identity, colors, layout, legalities, manacost, manavalue, name, printings, subtypes, supertypes, description, type, types, power, toughness) 
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        [card]
    )
    print("Card added Successfully in deck "+deck_name)
    exit(0)

if args.list is not None:
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

if args.import_csv is not None:
    exit(0)
