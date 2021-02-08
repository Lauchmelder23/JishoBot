import requests
import urllib.parse
import json
import re
from bs4 import BeautifulSoup

TEMPLATE_URL = "https://jisho.org/api/v1/search/words?keyword={0}"
TEMPLATE_KANJI_URL = "https://jisho.org/search/{0}"
HEADER = {
    "User-Agent": "Jisho Bot",
    "From": "https://github.com/Lauchmelder23/JishoBot"
}

class JishoSense():
    def __init__(self, sense):
        self.english_definitions = sense["english_definitions"]
        self.fenglish_definitions = "; ".join(self.english_definitions)
        self.parts_of_speech = sense["parts_of_speech"]
        self.fparts_of_speech = ", ".join(sense["parts_of_speech"])
        if self.fparts_of_speech == "":
            self.fparts_of_speech = "\u200b" # Zero width space to have empty embed value

class JishoNode():
    def __init__(self, node):
        self.slug = node["slug"]
        if "is_common" in node:
            self.is_common = node["is_common"]
        else:
            self.is_common = False
        
        self.tags = node["tags"]
        self.jlpt = node["jlpt"]

        self.ftags = ""
        if self.is_common:
            self.ftags += "Common "
        for tag in self.tags:
            self.ftags += f"| {tag} "
        for jlpt in self.jlpt:
            self.ftags += f"| {jlpt} "

        self.japanese = []
        for entry in node["japanese"]:
            if "word" not in entry:
                word = entry["reading"]
                reading = ""
            elif "reading" not in entry:
                word = entry["word"]
                reading = ""
            else:
                word = entry["word"]
                reading = entry["reading"]

            self.japanese.append((word, reading))
        self.senses = []

        for sense in node["senses"]:
            self.senses.append(JishoSense(sense))

class JishoResponse():
    def __init__(self, query: str):
        self.query_string = query
        self.raw = self.query()
        self.nodes = []
        self.disassemble()

        self.size = len(self.nodes)

    def query(self):
        url = TEMPLATE_URL.format(urllib.parse.quote_plus(self.query_string))
        r = requests.get(url, headers=HEADER)

        if r.status_code != 200:
            print(f"ERROR: Failed to access Jisho API... {r.status_code}")
            return None
        
        return json.loads(r.text)

    def disassemble(self):
        self.status = self.raw["meta"]["status"]
        self.entries = len(self.raw["data"])

        for node in self.raw["data"]:
            self.nodes.append(JishoNode(node))
            


class JishoKanjiNode():
    def __init__(self):
        # Information about the Kanji
        self.kanji = ""
        self.url = "https://jisho.org/search/"
        self.meaning = ""
        self.kun = []
        self.on = []
        self.radical = []
        self.grade = ""
        self.jlpt = ""
        self.strokes = ""
        self.image_url = ""


class JishoKanji():
    def __init__(self, query):     
        self.query_string = query

        # List of JishoKanjiNodes
        self.nodes = []
        self.entries = 0

        self.query()

    def query(self):
        self.url = TEMPLATE_KANJI_URL.format(urllib.parse.quote_plus(self.query_string + "#kanji"))
        r = requests.get(self.url, headers=HEADER)

        if r.status_code != 200:
            print(f"ERROR: Failed to access Jisho API... {r.status_code}")
            return None

        body = BeautifulSoup(r.text, features="html.parser")

        info_blocks = body.find_all("div", {"class": "kanji details"})

        for info in info_blocks:
            self.entries += 1
            self.nodes.append(JishoKanjiNode())

            self.nodes[-1].kanji = info.findChild("h1").string
            self.nodes[-1].url += urllib.parse.quote_plus(self.nodes[-1].kanji + "#kanji")

            # Meanings
            self.nodes[-1].meaning = info.findChild("div", {"class": "kanji-details__main-meanings"}, recursive=True).string

            readings_block = info.findChild("div", {"class": "kanji-details__main-readings"}, recursive=True)

            # Kun Yomi
            kun_block = readings_block.findChild("dl", {"class": "dictionary_entry kun_yomi"}, recursive=True)
            if kun_block is not None:
                readings = kun_block.findChildren("a", recursive=True)
                for reading in readings:
                    self.nodes[-1].kun.append(reading.string)

            # On Yomi
            on_block = readings_block.findChild("dl", {"class": "dictionary_entry on_yomi"}, recursive=True)
            if on_block is not None:
                readings = on_block.findChildren("a", recursive=True)
                for reading in readings:
                    self.nodes[-1].on.append(reading.string)

            # Radical
            radical_block = info.findChild("div", {"class": "radicals"}, recursive=True).findChild("span")
            self.nodes[-1].radical.append(re.sub(r'[ \n"]', "", radical_block.contents[2].string))
            self.nodes[-1].radical.append(re.sub(r'[ \n"]', "", radical_block.contents[1].string))

            # JLPT/Grade info
            grade_block = info.findChild("div", {"class": "grade"}, recursive=True)
            if grade_block is not None:
                self.nodes[-1].grade = grade_block.findChild("strong").string[-1]
            
            self.nodes[-1].jlpt = info.findChild("div", {"class": "jlpt"}, recursive=True).findChild("strong").string

            # Strokes
            self.nodes[-1].strokes = info.findChild("div", {"class": "kanji-details__stroke_count"}, recursive=True).findChild("strong").string

            # Stroke order diagram
            r = requests.get(url=("https://jitenon.com/kanji/" + urllib.parse.quote_plus(self.nodes[-1].kanji)), headers=HEADER)
            if r.status_code != 200:
                continue

            strokediag = BeautifulSoup(r.text, features="html.parser")
            image_url = strokediag.find("div", {"class": "kanji_main ChangeElem_Panel"}).findChild("img")["src"]
            image_url = "https:" + image_url
            image_url = image_url.replace("shotai3", "shotai2")
            self.nodes[-1].image_url = image_url
