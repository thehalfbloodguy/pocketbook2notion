from bs4 import BeautifulSoup
from dataclasses import dataclass
from collections import OrderedDict
import os
import re
import ebooklib
from ebooklib import epub


@dataclass
class Note:
    id: str
    div_class: str
    page_no: str
    text: str

class NotesPage():
    def __init__(self, path):
        self.path = path

    def parse(self):
        # TODO: remove div_class?
        with open(self.path, encoding='utf-8') as HTMLFile:
            index = HTMLFile.read()
            soup = BeautifulSoup(index, features="html.parser")
            divs = soup.find_all('div', class_=re.compile("bookmark"))
            self.notes = []
            for div in divs:
                id = div.get('id')
                if id:
                    div_class = div.get('class')[-1]
                    page_no = div.find(class_="bm-page").text
                    text = div.find(class_="bm-text").text
                    self.notes.append(Note(id, div_class, page_no, text))

class BookParser:
    def parse(self, file_path):
        raise NotImplementedError("Subclasses should implement this method")

class EPUBParser(BookParser):
    def parse(self, file_path):
        raise NotImplementedError("No EPUB structure parsing yet")

def parse_book_structure(book_path):
    if book_path and book_path.endswith('.epub'):
        parser = EPUBParser()
        book_structure = parser.parse(book_path)
        return book_structure
    return None

def find_book_by_name(directory, book_name):
    for root, _, files in os.walk(directory):
        for file in files:
            if book_name in file:
                return os.path.join(root, file)
    return None