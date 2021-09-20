import os
import pickle
from urllib import parse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4.element import SoupStrainer
from datetime import datetime

# data파일 구조
# 캐릭터 정보 딕셔너리가 리스트로 있음.

class Character():
    def __init__(self, name, clss):
        self.name = name
        self.clss = clss
        self.todo = [] # {name, icon, freq}
class Expadition():
    def __init__(self, num, name):
        self.num = num
        char = SoupStrainer(['ul', 'title'])

        self.load_profile(num)
        # 전투정보실 페이지 받아오기
        raw_page = urlopen(f"https://lostark.game.onstove.com/Profile/Character/{parse.quote(name)}")
        parsed_page = BeautifulSoup(raw_page, "html.parser", parse_only=char)
        profile = parsed_page.select("ul.profile-character-list__char, title")
        profile[1] = profile[1].find_all("span")

        # 로아 점검중일때
        if("점검" in profile[0]):
            print("원정대 조회 실패: 로스트아크 점검중")
        # 점검중이 아닐때
        else:
            self.character = []
            for i in range(0, len(profile[1]), 2):
                profile[1][i] = str(profile[1][i])[7:-8]
                char_cls = profile[1][i][profile[1][i].find("alt")+5 : profile[1][i].find("src")-2]
                char_name = profile[1][i][profile[1][i].find("<span>")+6 : profile[1][i].find("</span>")]
                self.character.append(Character(char_name, char_cls))
            self.save_profile()

    def load_profile(self, num):
        self.character = []
        if not os.path.exists(f"./data/expaditaion{num}"):
            print("저장된 정보 없음.")
            return
        with open(f"./data/expaditaion{self.num}.data", "rb") as file:
            len = pickle.load(file)
            for i in range(len):
                temp = pickle.load(file)
                self.character.append(Character(temp["name"], temp["clss"]))
                self.character[i].todo = temp["todo"]

    def save_profile(self):
        if not os.path.exists("./data"):
            os.makedirs("./data")
        with open(f"./data/expaditaion{self.num}.data", "wb") as file:
            for i in self.character:
                pickle.dump({"name": i.name, "clss": i.clss, "todo": i.todo}, file)