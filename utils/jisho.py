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
        self.japanese = []
        for entry in node["japanese"]:
            if "word" not in entry:
                word = entry["reading"]
                reading = ""
            else:
                word = entry["word"]
                reading = entry["reading"]

            self.japanese.append((word, reading))
        self.senses = []

        for sense in node["senses"]:
            self.senses.append(JishoSenses(sense))

class JishoResponse():
    def __init__(self, query: str):
        self.query_string = query
        self.raw = self.query()
        self.nodes = []
        self.disassemble()

    def query(self):
        url = TEMPLATE_URL.format(urllib.parse.quote_plus(self.query_string))
        r = requests.get(url)

        if r.status_code != 200:
            print(f"ERROR: Failed to access Jisho API... {r.status_code}")
            return None
        
        return json.loads(r.text)

    def disassemble(self):
        self.status = self.raw["meta"]["status"]
        self.entries = len(self.raw["data"])

        for node in self.raw["data"]:
            self.nodes.append(JishoNode(node))
            
