import json
import sqlite3
import sys
import ijson

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
    cursor.execute("""CREATE INDEX atomic_cards_manavalue_index ON atomic_cards(manavalue)""")

print("Inserting Data")
with open("./AtomicCards.json", "rb") as f:
    for cards in ijson.kvitems(f, "data"):
        card = cards[1][0]
        try:
            cursor.execute("INSERT INTO atomic_cards VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    ''.join(card["colorIdentity"]),
                    ''.join(card["colors"]),
                    card["layout"],
                    ','.join(card["legalities"]) if "legalities" in card else "",
                    card["manaCost"] if "manaCost" in card else "",
                    int(card["manaValue"]) if "manaValue" in card else 0,
                    card["name"],
                    ','.join(card["printings"]) if "printings" in card else "",
                    ','.join(card["subtypes"]),
                    ','.join(card["supertypes"]),
                    card["text"] if "text" in card else "",
                    card["type"],
                    ','.join(card["types"]),
                    card["power"] if "power" in card else 0,
                    card["toughness"] if "toughness" in card else 0,
                )
            )
        except Exception as e:
            print(card)
            raise e
        else:
            print("-", end="")
            sys.stdout.flush()

cursor.close()
con.close()
print("Finished")
