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
    def __init__(self, name, cls):
        self.name = name
        self.cls = cls
        
class Expadition():
    def __init__(self, num, name):
        self.num = num
        char = SoupStrainer(['ul', 'title'])

        # 전투정보실 페이지 받아오기
        if name == "마이크로포서드":
            exit()
        raw_page = urlopen(f"https://lostark.game.onstove.com/Profile/Character/{parse.quote(name)}")
        profile = BeautifulSoup(raw_page, "html.parser", parse_only=char).select("ul.profile-character-list__char, title")
        profile[1] = profile[1].find_all("span")

        # 로아 점검중일때
        if("점검" in str(BeautifulSoup(raw_page, "html.parser", parse_only=char))):
            print("원정대 조회 실패: 로스트아크 점검중")
            self.load_profile(num)
        
        # 점검중이 아닐때
        else:
            self.character = []
            for i in range(0, len(profile[1]), 2):
                profile[1][i] = str(profile[1][i])[7:-8]
                char_cls = profile[1][i][profile[1][i].find("alt")+5 : profile[1][i].find("src")-2]
                char_name = profile[1][i][profile[1][i].find("<span>")+6 : profile[1][i].find("</span>")]
                self.character.append(Character(char_name, char_cls))
            self.save_profile()

    def save_profile(self):
        if not os.path.exists("./data"):
            os.makedirs("./data")
        with open(f"./data/expaditaion{self.num}.data", "wb") as file:
            temp = []
            for i in self.character:
                pickle.dump({"name": i.name, "cls": i.cls}, file)

    def load_profile(self):
        self.character = []
        if not os.path.exists("./data/expaditaion0"):
            print("저장된 정보 없음.")
            return
        with open(f"./data/expaditaion{self.num}.data", "rb") as file:
            len = pickle.load(file)
            for i in range(len):
                self.character.append(Character(pickle.load(file)))
                self.character[i].name = pickle.load(file)
                self.character[i].cls = pickle.load(file)