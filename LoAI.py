import os
from urllib.request import urlopen
from urllib import parse
from bs4 import BeautifulSoup

class Character():
    def __init__(self, name):
        self.name = name
        
        self.profile_html = urlopen(f"https://lostark.game.onstove.com/Profile/Character/{parse.quote(self.name)}")
        self.profile = BeautifulSoup(self.profile_html, "html.parser")
        
        self.level = str(self.profile.select("#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info > div.level-info__item > span"))[45:-8]
        self.char = str(self.profile.select("#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__expedition"))[84:]
        self.target_idx = self.char.find("<small>")
        self.item_level = self.char[:self.target_idx] + self.char[self.target_idx+7:self.target_idx+10]
        print(self.name, self.level, self.item_level)

class Expadition():
    def __init__(self, name):
        self.profile_html = urlopen(f"https://lostark.game.onstove.com/Profile/Character/{parse.quote(name)}")
        self.profile = BeautifulSoup(self.profile_html, "html.parser")
        self.char = list(self.profile.select("#expand-character-list > ul > li > span > button > span"))

        self.character = [] 
        for i in self.char:
            self.character.append(Character(str(i)[6:-7]))

if __name__ == '__main__':
    name = input()
    expadition = Expadition(name)