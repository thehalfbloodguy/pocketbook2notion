import json
import time
import os

from collections import defaultdict

from notion import Database, Page
from pocketbook import NotesPage

MAX_NOTE_LENGTH = 2000
MAX_BATCH_SIZE = 100

if __name__ == "__main__":

    with open('secret.txt') as secret_file:
        NOTION_SECRET = secret_file.read()
    HEADERS = {
        "Notion-Version": "2022-02-22",
        "Authorization": "Bearer " + NOTION_SECRET
    }
    with open('config.json') as config_file:
        config = json.load(config_file)
        DATABASE_ID = config['database_id']
        PB_NOTES_DIR = config['pb_notes_dir']

    pb_notes_pagenames = os.listdir(PB_NOTES_DIR)
    if '.sync_file.json' in pb_notes_pagenames:
        synced_notes = json.load(open(f"{PB_NOTES_DIR}/.sync_file.json"))
        pb_notes_pagenames.remove('.sync_file.json')
    else:
        synced_notes = defaultdict(list)

    # Add new books to Notion database if needed
    db = Database(DATABASE_ID)
    response = db.query(HEADERS)
    results = response.json()['results']
    db_page_map = {res['properties']['Name']['title'][0]['plain_text']: res['id'] for res in results}
    for pb_notes_pagename in pb_notes_pagenames:
        book_name = os.path.splitext(pb_notes_pagename)[0]
        if book_name not in db_page_map:
            response = db.createEmptyPage(book_name, HEADERS)

    # Add unsynced notes to book pages in Notion database
    time.sleep(0.1)
    response = db.query(HEADERS)
    results = response.json()['results']
    db_page_map = {res['properties']['Name']['title'][0]['plain_text']: res['id'] for res in results}
    for pb_notes_pagename in pb_notes_pagenames:
        book_name = os.path.splitext(pb_notes_pagename)[0]
        book_page = NotesPage(f'{PB_NOTES_DIR}/{pb_notes_pagename}')
        book_page.parse()
        page = Page(db_page_map[book_name])
        response = page.get_children(HEADERS)
        page_blocks = response.json()['results']
        unsynced_notes = list(filter(lambda x: x.id not in synced_notes[pb_notes_pagename], book_page.notes))
        for note in unsynced_notes:
            if len(note.text) < MAX_NOTE_LENGTH: # add splitting if it is >= MAX_NOTE_LENGTH
                response = page.add_child(note, HEADERS)
                synced_notes[pb_notes_pagename].append(note.id)

    json.dump(synced_notes, open(f"{PB_NOTES_DIR}/.sync_file.json", "w"))