import argparse
import os
import sqlite3
import sys
from pathlib import Path
from pprint import pprint
from subprocess import run

import requests
from bs4 import BeautifulSoup as bs

FILE = os.path.join(str(Path.home()), ".pyurl/pyurl.db")


def __version__():
    """Version info"""
    return "pyurl – 0.1.0"


# check FILE path exists or not
if not os.path.exists(FILE):
    os.mkdir(os.path.join(str(Path.home()), ".pyurl"))
    open(FILE, "w").close()
    db = sqlite3.connect(FILE)
    cursor = db.cursor()
    cursor.execute(
        "CREATE TABLE 'urls' ('url_id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'url' NOT NULL)"
    )
    cursor.execute(
        """CREATE TABLE 'links'
        ('link_id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'url_id' INTEGER NOT NULL,
        'link' TEXT NOT NULL, 'status' TEXT NOT NULL)"""
    )
    db.commit()
    db.close()


db = sqlite3.connect(FILE)
cursor = db.cursor()


def check(sync_urls: str, cursor: sqlite3.Cursor, db: sqlite3.Connection, status: str):
    """Checking update in the back

    Args:
        sync_urls: URL(s) to be checked
        cursor: Cursor object of sqlite3
        db: Connection object of sqlite3
        status: 'viewed' or 'unviewed'

    Return:
        List of update links
    """

    links_from_db = []
    links_fetch = []
    out_updates = []
    https_updates = []
    for sync_url in sync_urls.split(","):
        sync_url = sync_url.strip("/")
        f_links = fetch(sync_url)  # .split(",")
        for f_link in f_links:
            links_fetch.append(f_link.strip())

        db_links = cursor.execute(
            "SELECT link FROM links JOIN urls ON links.url_id=urls.url_id WHERE urls.url=?",
            (sync_url,),
        )
        for link in db_links:
            links_from_db.append(link[0])

        links_set = set(links_from_db)
        updates = [x for x in links_fetch if x not in links_set]
        url_split = sync_url.split("/")
        for update in updates:
            if sync_url in update:
                https_updates.append(update)
            elif len(url_split) > 3:
                url_split = url_split[:3]
                https_updates.append("/".join(url_split) + "/" + update.strip("/"))
            else:
                https_updates.append(sync_url + "/" + update.strip("/"))

        url_id = cursor.execute(
            "SELECT url_id FROM urls WHERE url=?", (sync_url,)
        ).fetchone()[0]
        for update in updates:
            items = (url_id, update, status)
            cursor.execute(
                "INSERT INTO links (url_id, link, status) VALUES (?, ?, ?)", items
            )
            db.commit()

        out_updates.extend(https_updates)

    return out_updates


def fetch(url: str):
    """Fetch the links on the page of the added website

    Args:
        url: url of the website to be fetched

    Return:
        List of the added website links
    """

    html = requests.get(url)
    soup = bs(html.text, "lxml")
    # links = str(soup.find_all("a"))
    links = []
    for link in soup.find_all("a"):
        links.append(str(link.get("href")))

    return links


def open_from_cli(updates: list):
    """Open the links from CLI"""
    for update in updates:
        print(f"Opening {update}...")
        if sys.platform.startswith("linux"):
            run(["xdg-open", update], check=True)
        elif sys.platform.startswith("darwin"):
            run(["open", update], check=True)
        elif sys.platform.startswith("win32"):
            run(["start", update], check=True)
        elif sys.platform.startswith("cygwin"):
            run(["start", update], check=True)
        else:
            print("==> 😔 Cannot open the links from terminal in your system!")


def url_exists(urls: str, p_urls: sqlite3.Cursor):
    """Check URL(s) already exist(s) or not

    Args:
        urls: URL(s) from the user input
        p_urls: URL(s) in the db

    Return:
        List of already existed URL(s)
    """

    match = []
    for p_url in p_urls:
        for url in urls.split(","):
            url = url.strip("/")
            if p_url[0] == url:
                match.append(url)

    return match


def view(viewing: bool):
    return "viewed" if viewing else "unviewed"


def add(add_urls: str):
    """Add the url of the website to the db

    Args:
        add_urls: url(s) of the website(s) to be added

    Return:
        1 if successful else 0
    """

    status = "viewed"
    # db = sqlite3.connect(FILE)
    # cursor = db.cursor()
    p_urls = cursor.execute("SELECT url FROM urls")
    match = url_exists(add_urls, p_urls)
    if match:
        print(f"==> {match} is already added. You can leave it!")
        return 0
    else:
        for url in add_urls.split(","):
            url = url.strip("/")
            links = fetch(url)  # .split(",")
            url = (url,)
            cursor.execute("INSERT INTO urls (url) VALUES (?)", url)
            db.commit()
            url_id = cursor.execute(
                "SELECT url_id FROM urls WHERE url=?", url
            ).fetchone()[0]
            for link in links:
                items = (url_id, link.strip(), status)
                cursor.execute(
                    "INSERT INTO links (url_id, link, status) VALUES (?, ?, ?)", items
                )
                db.commit()
        # db.close()
        print("==> 🎉 URL added successfully!")
        return 1


def sync(sync_urls: str, viewing: bool):
    """Check for the added websites update status

    Args:
        sync_urls: url(s) of the website(s) to be synced
        viewing: True or False

    Return:
        List of new links found on the websites
    """

    # db = sqlite3.connect(FILE)
    # cursor = db.cursor()
    status = view(viewing)
    if sync_urls == "all":
        updates = []
        urls = cursor.execute("SELECT url FROM urls").fetchall()
        for url in urls:
            update = check(url[0], cursor, db, status)
            updates.extend(update)
    else:
        updates = check(sync_urls, cursor, db, status)

    if updates:
        pprint(f"Found new {updates}")
        if status == "viewed":
            open_from_cli(updates)
        else:
            print("==> 😎 You can now visit the links you want!")
    else:
        print("==> No new pages published on your added websites!")

    # db.close()

    return updates


def remove(urls: str):
    """Remove the added URL(s)"""
    # db = sqlite3.connect(FILE)
    # cursor = db.cursor()
    for url in urls.split(","):
        url = url.strip("/")
        url_id = cursor.execute(
            "SELECT url_id FROM urls WHERE url=?", (url,)
        ).fetchone()
        if url_id is not None:
            cursor.execute("DELETE FROM urls WHERE url_id=?", (url_id[0],))
            cursor.execute("DELETE FROM links WHERE url_id=?", (url_id[0],))
            print(f"==> Removing {url}...")
        elif url_id is None:
            print(f"==> `{url}` doesn't exist!")
        else:
            print(f"==> {OSError}")

    db.commit()
    # db.close()


def log(logging: bool):
    """Print the added URL(s)"""
    if logging:
        # db = sqlite3.connect(FILE)
        # cursor = db.cursor()
        urls = cursor.execute("SELECT url FROM urls")
        print("URL(s) are:")
        for url in urls:
            print(f"==> {url[0]}")
        # db.close()
        return 1
    else:
        return 0


def no_view(no_viewing: bool, viewing: bool):
    """Show unviewed links

    Args:
        no_viewing: True or False
        viewing: True or False

    Return:
        1 for 'unviewed', 0 for 'viewed'
    """
    if no_viewing:
        status = "unviewed"
    else:
        status = "viewed"
        return 0

    links = []
    urls = []
    https_no_views = []
    # db = sqlite3.connect(FILE)
    # cursor = db.cursor()
    no_view_links = cursor.execute(
        "SELECT link, url_id FROM links WHERE status=?", (status,)
    )
    for no_view_link in no_view_links:
        links.append(no_view_link[0])
        no_view_urls = cursor.execute(
            "SELECT url FROM urls WHERE url_id=?", (no_view_link[1],)
        )
        for no_view_url in no_view_urls:
            urls.extend(no_view_url[0].split())

    for url in urls:
        url_split = url.split("/")
        for link in links:
            if url in link:
                https_no_views.append(link)
            elif len(url_split) > 3:
                url_split = url_split[:3]
                https_no_views.append("/".join(url_split) + "/" + link.strip("/"))
            else:
                https_no_views.append(url + "/" + link.strip("/"))

    if https_no_views:
        print(f"==> You have not opened {https_no_views} yet!")
        status = view(viewing)
        if status == "viewed":
            cursor.execute("UPDATE links SET status=?", (status,))
            db.commit()
            open_from_cli(https_no_views)
        else:
            print("==> 😎 You can now visit the links you want!")
    else:
        print("==> 🎉 You have read all updates!")

    # db.close()
    return 1


def main():
    parser = argparse.ArgumentParser(
        prog="pyurl",
        usage="%(prog)s <commands> [URL(s)]",
        description="Get notified about new blogs, updates of your favourite webistes and visit them at once",
        conflict_handler="resolve",
    )

    group = parser.add_argument_group("Commands")
    group.add_argument("-a", "--add", dest="add", help="Add the website url")
    group.add_argument(
        "-s", "--sync", dest="sync", help="Check the added websites update status"
    )
    group.add_argument("-rm", "--remove", dest="remove", help="Remove the added URL(s)")
    group.add_argument(
        "-l",
        "--log",
        dest="log",
        action="store_true",
        help="Output the urls of the added websites",
    )
    group.add_argument(
        "-o",
        "--open",
        dest="open",
        action="store_true",
        help="Open the new found website links",
    )
    group.add_argument(
        "-nv",
        "--no-view",
        dest="noview",
        action="store_true",
        help="Output the un-opened links",
    )

    group = parser.add_argument_group("Options")
    group.add_argument(
        "-V",
        "--version",
        action="version",
        version=__version__(),
        help="Output version number",
    )
    group.add_argument("-h", "--help", action="help", help="Output usage information")

    args = parser.parse_args()
    add_urls = args.add
    sync_urls = args.sync
    rm_urls = args.remove
    log_urls = args.log
    open_urls = args.open
    no_view_urls = args.noview

    URLS = [add_urls, log_urls, rm_urls]
    FUNCTIONS = [add, log, remove]

    if sync_urls is not None:
        sync(sync_urls, open_urls)

    if open_urls is True and sync_urls is None:
        print("==> TIP: `-o` has to be used with `-s` or `-nv`")

    if no_view_urls is True:
        no_view(no_view_urls, open_urls)

    for i in range(len(URLS)):
        if URLS[i] is not None:
            FUNCTIONS[i](URLS[i])


if __name__ == "__main__":
    main()
    db.close()
