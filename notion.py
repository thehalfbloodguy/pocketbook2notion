import copy
import json
import requests

def populate_template(note):
    child = {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text":
                        {
                            "content": f"{note.text} (page {note.page_no})"
                        }
                }
            ]
        }
    }
    return child

class Database():
    '''
    Represents Notion database object
    '''
    def __init__(self, id):
        self.id = id
        self.url = f"https://api.notion.com/v1/databases/{self.id}"

    def retrieve(self, headers):
        response = requests.request("GET", self.url, headers=headers)
        return response

    def createPage(self, title, notes, headers):
        # TODO: add 'book' type, add vertical bar near a high light (different child block type?)
        # TODO: handle cases over 100 notes
        createUrl = 'https://api.notion.com/v1/pages'
        children = []
        for i in range(len(notes)):
            children.append(populate_template(notes[i]))
        print(children)

        newPageData = {
            "parent": {"database_id": self.id},
            "properties": {
                "Name": {
                    "title": [{
                            "text": {
                                "content": title
                            }
                        }]
                }
            },
            "children": children
        }
        data = json.dumps(newPageData)

        headers = copy.deepcopy(headers)
        headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })

        response = requests.request("POST", createUrl, headers=headers, data=data)
        return response

    def query(self, headers):
        url = f"{self.url}/query"
        payload = {}
        headers = copy.deepcopy(headers)
        headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        response = requests.request("POST", url, json=payload, headers=headers)
        return response

class Block():
    def __init__(self, id):
        self.id = id
        self.block_url = f"https://api.notion.com/v1/blocks/{self.id}"

    def get_children(self, headers):
        url = f"{self.block_url}/children"
        response = requests.request("GET", url, headers=headers)
        return response

    def add_child(self, note, headers):
        text_block = {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": f"{note.text} (page {note.page_no})"
                    }
                }]
            }
        }
        url = f"{self.block_url}/children"

        response = requests.request("PATCH", url, json={"children": [text_block]}, headers=headers)
        return response

class Page(Block):
    '''
    Represents Notion page object
    '''
    def __init__(self, id):
        super().__init__(id)
        self.url = f"https://api.notion.com/v1/pages/{self.id}"