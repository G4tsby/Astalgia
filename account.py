import os
import pickle
from urllib import parse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4.element import SoupStrainer


class Character:
    def __init__(self, name, clss):
        self.name = name
        self.clss = clss
        self.todo = []  # {name, icon, freq}


class Account:
    def __init__(self, num, name):
        self.num = num

        self.load_profile()
        # 전투정보실 페이지 받아오기
        self.get_char_data(name)

        # 로아 점검중일때
        if "점검" in str(self.profile[0]):
            print("원정대 조회 실패: 로스트아크 점검중")
        # 점검중이 아닐때 캐릭터 정보 파싱
        else:
            temp = []
            for i in range(len(self.character)):
                temp.append(self.character[i].todo)
            self.character = []
            self.parse_char()
            # 원정대 대표 캐릭터가 첫 인덱스로 가게 순서 변경
            for i in range(len(self.character)):
                if self.character[i].name == name:
                    self.character = [self.character[i]] + self.character[:i] + self.character[(i + 1):]
                    break
            for i in range(len(temp)):
                self.character[i].todo = temp[i]
            temp = None
            self.save_profile()

    def get_char_data(self, name):
        char = SoupStrainer(['ul', 'title'])
        raw_page = urlopen(f"https://lostark.game.onstove.com/Profile/Character/{parse.quote(name)}")
        parsed_page = BeautifulSoup(raw_page, "html.parser", parse_only=char)
        self.profile = parsed_page.select("ul.profile-character-list__char, title")
        if len(self.profile) > 2:
            for i in range(1, len(self.profile)):
                self.profile[i] = self.profile[i].find_all("span")

    def parse_char(self):
        if len(self.profile) == 1:
            print("닉네임 잘못됨")
            return
        if len(self.profile) > 2:
            for i in range(1, len(self.profile)):
                self.profile[i] = list(self.profile[i])
                if len(self.profile[i]) == 3:
                    self.profile[i] = self.profile[i][1:]
                for j in range(0, len(self.profile[i]), 2):
                    self.profile[i][j] = str(self.profile[i][j])[7:-8]
                    char_clss = self.profile[i][j][
                                self.profile[i][j].find("alt") + 5: self.profile[i][j].find("src") - 2]
                    char_name = self.profile[i][j][
                                self.profile[i][j].find("<span>") + 6: self.profile[i][j].find("</span>")]
                    self.character.append(Character(char_name, char_clss))
        else:
            self.profile[1] = list(self.profile[1])
            for i in range(1, len(self.profile[1]), 2):
                self.profile[1][i] = str(self.profile[1][i])[7:-8]
                char_clss = self.profile[1][i][self.profile[1][i].find("alt") + 5: self.profile[1][i].find("src") - 2]
                char_name = self.profile[1][i][
                            self.profile[1][i].find("<span>") + 6: self.profile[1][i].find("</span>")]
                self.character.append(Character(char_name, char_clss))

    def load_profile(self):
        self.character = []
        if not os.path.exists(f"./data/account{self.num}.data"):
            print("저장된 정보 없음.")
            return
        with open(f"./data/account{self.num}.data", "rb") as file:
            len = pickle.load(file)
            for i in range(len):
                temp = pickle.load(file)
                self.character.append(Character(temp["name"], temp["clss"]))
                self.character[i].todo = temp["todo"]

    def save_profile(self):
        if not os.path.exists("./data"):
            os.makedirs("./data")
        with open(f"./data/account{self.num}.data", "wb") as file:
            pickle.dump(len(self.character), file)
            for i in self.character:
                pickle.dump({"name": i.name, "clss": i.clss, "todo": i.todo}, file)
