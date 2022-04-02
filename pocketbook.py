from bs4 import BeautifulSoup
import re

# TODO: change to struct?
class Note():
    def __init__(self, id, div_class, page_no, text):
        self.id = id
        self.div_class = div_class
        self.page_no = page_no
        self.text = text.strip()

class NotesPage():
    def __init__(self, path):
        self.path = path

    def parse(self):
        # TODO: remove div_class?
        with open(self.path) as HTMLFile:
            index = HTMLFile.read()
            soup = BeautifulSoup(index, 'lxml')
            divs = soup.find_all('div', class_=re.compile("bookmark"))
            self.notes = []
            for div in divs:
                id = div.get('id')
                if id:
                    div_class = div.get('class')[-1]
                    page_no = div.find(class_="bm-page").text
                    text = div.find(class_="bm-text").text
                    self.notes.append(Note(id, div_class, page_no, text))