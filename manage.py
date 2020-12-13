import argparse
import os
from os import path
from database import Database

parser = argparse.ArgumentParser(description='App manager.')
parser.add_argument('command', metavar="cmd", type=str, help='command to manage the app')

args = parser.parse_args()


def create_database():
    db = Database()
    with db.get_cursor() as cursor:
        cursor.execute("CREATE TABLE inventory (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
    db.commit()
    print("Finished creating table")


def fill_database():
    db = Database()
    with db.get_cursor() as cursor:
        cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("banana", 150))
        cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("orange", 154))
        cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("apple", 100))
    db.commit()
    print("Inserted 3 rows of data")


def drop_database():
    db = Database()
    with db.get_cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS inventory;")
    db.commit()
    print("Finished dropping tables")


if args.command == "init":
    if path.exists("initialized.txt"):
        print("This project already initialized")
    else:
        try:
            create_database()
            fill_database()
            open("initialized.txt", "w+")
            print("project initialized")
        except Exception as inst:
            print("cannot initialize project: " + str(inst))

elif args.command == "destroy":
    drop_database()
    os.remove("initialized.txt")
