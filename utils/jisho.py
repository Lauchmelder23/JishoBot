import requests
import urllib.parse
import json

TEMPLATE_URL = "https://jisho.org/api/v1/search/words?keyword={0}"

class JishoSenses():
    def __init__(self, sense):
        self.english_definitions = sense["english_definitions"]
        self.english_definitions_formatted = "; ".join(self.english_definitions)
        self.parts_of_speech = sense["parts_of_speech"]

class JishoNode():
    def __init__(self, node):
        self.slug = node["slug"]
        self.is_common = node["is_common"]
        self.tags = node["tags"]
        self.jlpt = node["jlpt"]
        self.japanese_word = node["japanese"]["word"]
        self.japanese_reading = node["japanese"]["reading"]
        self.senses = []
        for sense in node["senses"]
            self.senses.append(JishoSenses(sense))

class JishoResponse():
    def __init__(self, query: str):
        self.query = query
        self.raw = query()
        self.nodes = []
        disassemble()

    def query(self):
        url = TEMPLATE_URL.format(urllib.parse.quote_plus(self.query))
        r = requests.get(url)

        if r.status_code != 200:
            print(f"ERROR: Failed to access Jisho API... {r.status_code}")
        
        return json.loads(r.text)

    def disassemble(self):
        self.status = self.raw["meta"]["status"]
        self.entries = len(self.raw["data"])

        for node in self.raw["data"]:
            self.nodes.append(JishoNode(node))
            
