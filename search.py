import sqlite3
import argparse
from rich.table import Table
from rich.console import Console
from rich.style import Style
from rich.color import Color
import re

parser = argparse.ArgumentParser(
    prog = 'MTG Weasel',
    description = 'Search for MTG cards'
)
parser.add_argument('-n', '--name', help="The name of the card, starting by")
parser.add_argument('-d', '--description', help="Search in the card description, for multiple words usage : \"word otherWord\"")
parser.add_argument('-c', '--colors', help="colors on the card, RUGBW")
parser.add_argument('-t', '--type', help="Type of the card, Legenday, Instant, Creature, Zombie, Elf ...")
parser.add_argument('-m', '--manavalue', help="Manavalue less or equal to")
args = parser.parse_args()

con = sqlite3.connect("cards.db", isolation_level=None)
con.row_factory = sqlite3.Row
cursor = con.cursor()

res = cursor.execute("SELECT name FROM sqlite_master")
table_names = res.fetchone()
if table_names is None or "atomic_cards" not in table_names:
    print("Please initiate the database befor starting searching for cards")
    exit(1)

if args.name is None and args.description is None and args.colors is None and args.type is None:
    print("Please try using an option to search for a card like -n CardName")
    exit(1)

query="SELECT * FROM atomic_cards WHERE "
needAnd = False

if args.name is not None:
    query += "name LIKE \"{}%\" ".format(args.name)
    needAnd = True
if args.type is not None:
    if needAnd: query += "AND "
    i = 0
    for word in args.type.split():
        if i != 0: query += "AND "
        query += "type LIKE \"%{}%\" ".format(word)
        i += 1
    needAnd = True
if args.colors is not None:
    if needAnd: query += "AND "
    colorToExclude = ["B", "G", "R", "U", "W"]
    for color in args.colors:
        colorToExclude.remove(color)
    i = 0
    for color in colorToExclude:
        if i != 0: query += "AND "
        query += "colors NOT LIKE \"%{}%\" ".format(color)
        i += 1
    needAnd = len(colorToExclude) != 0
if args.description is not None:
    if needAnd: query += "AND "
    i = 0
    for word in args.description.split():
        if i != 0: query += "AND "
        query += "description LIKE \"%{}%\" ".format(word)
        i += 1
    needAnd = True
if args.manavalue is not None:
    if needAnd: query += "AND "
    query += "manavalue <= {} ".format(args.manavalue)

table = Table(title="Cards", row_styles=["", Style(bgcolor=Color.from_rgb(40,40,40))])
table.add_column("Name")
table.add_column("Mana Cost")
table.add_column("Type")
table.add_column("Description")
table.add_column("Body")
for card in cursor.execute(query):
    description = card["description"]
    if args.description is not None:
        for word in args.description.split():
            pattern = re.compile(word, re.IGNORECASE)
            description = pattern.sub("[yellow]"+word+"[/yellow]", description)
    cardType = card["type"]
    if args.type is not None:
        for word in args.type.split():
            pattern = re.compile(word, re.IGNORECASE)
            cardType = pattern.sub("[yellow]"+word+"[/yellow]", cardType)
    manacost = card["manacost"]
    for c, color in {"G": "green", "R": "red", "U": "blue", "W": "white", "B": "violet"}.items():
        manacost = manacost.replace("{"+c+"}", "["+color+"]{"+c+"}[/"+color+"]")

    table.add_row(
        card["name"] if args.name is None else card["name"].replace(args.name, "[yellow]"+args.name+"[/yellow]"),
        manacost,
        cardType,
        description,
        str(card["power"])+"/"+str(card["toughness"])
    )

console = Console()
console.print(table)
