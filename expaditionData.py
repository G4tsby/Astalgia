from urllib.request import urlopen
from urllib import parse
from bs4 import BeautifulSoup
import pickle
import os

class Character():
    def __init__(self, name):
        self.name = name
        
        self.profile_html = urlopen(f"https://lostark.game.onstove.com/Profile/Character/{parse.quote(self.name)}")
        self.profile = BeautifulSoup(self.profile_html, "html.parser")
        
        self.level = str(self.profile.select("#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info > div.level-info__item > span"))[45:-8]
        self.char = str(self.profile.select("#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__expedition"))[84:]
        self.target_idx = self.char.find("<small>")
        self.item_level = self.char[:self.target_idx] + self.char[self.target_idx+7:self.target_idx+10]

class Expadition():
    number_expadition = 0

    def __init__(self, name):
        self.number = self.number_expadition

        self.profile_html = urlopen(f"https://lostark.game.onstove.com/Profile/Character/{parse.quote(name)}")
        self.profile = BeautifulSoup(self.profile_html, "html.parser")
        if("점검" in str(self.profile.select("head > title"))):
            print("원정대 조회 실패: 로스트아크 점검중")
            self.load_profile()
        else:
            self.char = list(self.profile.select("#expand-character-list > ul > li > span > button > span"))
            self.character = [] 
            for i in self.char:
                self.character.append(Character(str(i)[6:-7]))

            self.save_profile()
        self.number_expadition += 1

    def save_profile(self):
        if not os.path.exists("./data"):
            os.makedirs("./data")
        with open(f"./data/expaditaion{self.number}.data", "wb") as file:
            pickle.dump(len(self.character), file)
            for i in self.character:
                pickle.dump(i.name, file)
                pickle.dump(i.level, file)
                pickle.dump(i.item_level, file)
                pickle.dump(i.name, file)

    def load_profile(self):
        self.character = []
        with open(f"./data/expaditaion{self.number}.data", "rb") as file:
            len = pickle.load(file)
            for i in range(len):
                self.character.append(Character(pickle.load(file)))
                self.character[i].level = pickle.load(file)
                self.character[i].item_level = pickle.load(file)
                self.character[i].name = pickle.load(file)
        for i in self.character:
            print(i.name)