import json
import os

from notion import Database, Page
from pocketbook import NotesPage


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

    pb_book_names = os.listdir(PB_NOTES_DIR)
    if '.sync_file.json' in pb_book_names:
        synced_notes = json.load(open(f"{PB_NOTES_DIR}/.sync_file.json"))
        pb_book_names.remove('.sync_file.json')
    else:
        synced_notes = dict()

    db = Database(DATABASE_ID)
    response = db.query(HEADERS)
    results = response.json()['results']
    db_page_map = {res['properties']['Name']['title'][0]['plain_text']: res['id'] for res in results}
    for pb_book_name in pb_book_names:
        book_page = NotesPage(f'{PB_NOTES_DIR}/{pb_book_name}')
        book_page.parse()
        if pb_book_name in db_page_map:
            page = Page(db_page_map[pb_book_name])
            response = page.get_children(HEADERS)
            page_blocks = response.json()['results']
            unsynced_notes = list(filter(lambda x: x.id not in synced_notes[pb_book_name], book_page.notes))
            for note in unsynced_notes:
                page.add_child(note, HEADERS)
                synced_notes[pb_book_name].append(note.id)
        else:
            response = db.createPage(pb_book_name, book_page.notes, HEADERS)
            synced_notes[pb_book_name] = [note.id for note in book_page.notes]
    json.dump(synced_notes, open(f"{PB_NOTES_DIR}/.sync_file.json", "w"))