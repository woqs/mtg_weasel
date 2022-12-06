import sqlite3
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(
    prog = 'MTG Weasel deck analyze tool',
    description = 'Understand your deck'
)
parser.add_argument('-n', '--name', help="The deck name")
parser.add_argument('-l', '--list', help="List all decks available", action='store_true')
args = parser.parse_args()

con = sqlite3.connect("decks.db", isolation_level=None)
con.row_factory = sqlite3.Row
cursor = con.cursor()

if args.list:
    res = cursor.execute("SELECT name FROM sqlite_master")
    table_names = [row["name"] for row in res.fetchall()]

    for table_name in table_names:
        if table_name.startswith("deck_"):
            print(table_name[5:])

if args.name is not None:
    res = cursor.execute("SELECT * FROM deck_"+args.name)
    
    cards_mana_value = {}
    for card in res.fetchall():
        if "Land" in card["type"]:
            continue
        if card["manavalue"] not in cards_mana_value:
            cards_mana_value[card["manavalue"]] = 1
        else:
            cards_mana_value[card["manavalue"]] += 1

    lists = sorted(cards_mana_value.items())
    x, y = zip(*lists)

    plt.bar(x, y)
    plt.margins(y=0.25)
    plt.show()

exit(0)
