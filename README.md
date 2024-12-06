# pocketbook2notion
A project to sync notes from Pocketbook reader to Notion database

### Usage
1. Export notes to internal storage
2. Create a secret.txt file with Notion secret token alongside other project files
3. Modify config.json to contain your:
   * database id
   * path to notes on your device while it is connected to your computer
4. Connect the reader to your computer in "PC Link" mode
5. Install requirements & run `python main.py`

### TODOs
- [x] turn quote block into "quote" type
- [ ] rotation of background colors for quotes?
- [ ] leave only necessary headers
- [ ] change DB from Playground to real
- [ ] option to sync with PB cloud account if not connected to the reader?
- [ ] sync abstractins' fields with Notion API docs
- [ ] add typings, docstrings
- [ ] comply with PEP8 (ahol tools)
- [ ] prettify README
- [ ] error handling
- [ ] support for all OS
- [ ] add links to Usage section
- [ ] different books can have the same name & cause collisions if matched only by name
- [ ] if you export notes & there already is a page for that book - it adds (n) at the end - take it into account
- [ ] book structure & text detection (main formats: fb2, epub) & insert notes according to it
- [ ] split notes over 2000 symbols in length