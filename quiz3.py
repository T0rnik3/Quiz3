# Tornike Giorgaia
import json
import sqlite3

import requests

# Harvard Art Museums API


key = "573d1f29-e784-44d1-b4d9-b109ad00d45b"
url = "https://api.harvardartmuseums.org/exhibition"
payload = {"apikey": key, "venue": "HAM"}

r = requests.get(url, params=payload)
res = r.json()

print("/" * 70)
print("API Url:\t", r.url)
print("Status Code:\t", r.status_code)
print("\\" * 70)
print()
# print(r.headers)


def save_headers():
    """Saving Request Headers:"""
    with open("headers.txt", "w") as file:
        file.write(str(r.headers))


def save_json():
    """Saving API Json file"""
    with open("./HAM_API.json", "w") as file:
        json.dump(res, file, indent=4)


def read_json():
    """Reading from Saved FILE:"""
    with open("./HAM_API.json", "r") as file:
        res = json.load(file)


exhebition_list = []


def show_page(records):
    """This Function Prints ALL Exhebitions from one Page"""
    with open("result.txt", "w", encoding="utf-8") as file:
        file.write("THIS IS LOG FILE".center(60, "."))
        file.write("\n")
        file.write("IT CONTAINS OUTPUTS OF SCRIPT".center(60, "."))
        file.write("\n\n")

    for i, record in enumerate(records, start=1):
        title = record["title"]
        begindate = record["begindate"]
        enddate = record["enddate"]
        exh_url = record["url"]
        venues = record["venues"]
        cities = []
        with open("result.txt", "a", encoding="utf-8") as output:
            output1 = f"Exhebition No.{i}:\nName:\t{title}\nDates:\tfrom {begindate} to {enddate}\nURL:\t{exh_url}\nVenues:"

            output.write(f"{output1}\n")
            print(output1)
            for n, venue in enumerate(venues, start=1):
                name_vanue = venue["name"]
                city = venue["city"]
                cities.append(city)
                output2 = f"City {n}:\t{city}\nPlace:\t{name_vanue}\n"
                print(output2)
                output.write(f"{output2}\n")

        exhebition_list.append((title, begindate, enddate, exh_url, str(cities)))


def show_pages():
    # Printing Exhebitions from Range of Inputed PAGES
    r = requests.get(url, params=payload)
    res = r.json()
    max_pages = res["info"]["pages"]
    pages = input(f"How Many Pages do you want to Request ? (MAX PAGES: {max_pages})\n")
    for page in range(1, int(pages) + 1):
        page_split = f" PAGE {page}: ".center(60, "#")
        records = res["records"]
        print(page_split)
        show_page(records)

        next_page = res["info"]["next"]
        r = requests.get(next_page)
        res = r.json()


def create_table():
    # Connecting and creating a cursor
    conn = sqlite3.connect("HAM.sqlite")
    cursor = conn.cursor()

    # Dropping a Table
    cursor.execute(
        """--sql
        DROP TABLE if exists exhebitions;
        """
    )

    # Creating a Table
    """
    In This Table We Have 
    << Title of Exhebition
    << Date of Exhebition Beginning
    << Date of Exhebition ending
    << Url of Exhebition
    << Cities Where Exhebition was held 
    """
    cursor.execute(
        """--sql
            CREATE TABLE if not exists exhebitions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(300),
            begin_date VARCHAR(100),
            end_date VARCHAR(100),
            urls VARCHAR(200),
            cities VARCHAR(200));
        """
    )

    # Inserting DATA into exhebition table
    cursor.executemany(
        """--sql
        INSERT INTO exhebitions (title, begin_date, end_date, urls, cities) 
        VALUES (?, ?, ?, ?, ?);
        """,
        exhebition_list,
    )
    conn.commit()

    conn.close()


def main():
    # show_page(res["records"])
    save_headers()
    save_json()
    show_pages()
    create_table()


if __name__ == "__main__":
    main()
