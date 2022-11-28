import json
import sqlite3
import sys

con = sqlite3.connect("cards.db", isolation_level=None)
cursor = con.cursor()

res = cursor.execute("SELECT name FROM sqlite_master")
table_names = res.fetchone()
if table_names is None or "atomic_cards" not in table_names:
    print("Table does not exist, creating")
    cursor.execute("""CREATE TABLE atomic_cards(
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
    )""")

print("Loading json")
f = open("./AtomicCards.json", "r")
data = json.loads(f.read())

print("Inserting Data")
for cards in data["data"].values():
    cursor.execute("INSERT INTO atomic_cards VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (
            ''.join(cards[0]["colorIdentity"]),
            ''.join(cards[0]["colors"]),
            cards[0]["layout"],
            ','.join(cards[0]["legalities"]) if "legalities" in cards[0] else "",
            cards[0]["manaCost"] if "manaCost" in cards[0] else "",
            cards[0]["manaValue"],
            cards[0]["name"],
            ','.join(cards[0]["printings"]) if "printings" in cards[0] else "",
            ','.join(cards[0]["subtypes"]),
            ','.join(cards[0]["supertypes"]),
            cards[0]["text"] if "text" in cards[0] else "",
            cards[0]["type"],
            ','.join(cards[0]["types"]),
            cards[0]["power"] if "power" in cards[0] else 0,
            cards[0]["toughness"] if "toughness" in cards[0] else 0,
        )
    )
    print("-", end="")
    sys.stdout.flush()

cursor.close()
con.close()
f.close()
print("Finished")
