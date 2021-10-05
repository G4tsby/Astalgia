from urllib import parse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4.element import SoupStrainer
import time


name = "행복관NPC"
char = SoupStrainer(['ul', 'title'])
raw_page = urlopen(f"https://lostark.game.onstove.com/Profile/Character/{parse.quote(name)}")
parsed_page = BeautifulSoup(raw_page, "html.parser", parse_only=char)
profile = parsed_page.select("ul.profile-character-list__char, title")
if len(profile) > 2:
    for i in range(1, len(profile)):
        profile[i] = profile[i].find_all("span")

for i in range(1, len(profile)):
    for j in range(0, len(profile[i]), 2):
        profile[i][j] = str(profile[i][j])[7:-8]
        char_cls = profile[i][j][profile[i][j].find("alt")+5 : profile[i][j].find("src")-2]
        char_name = profile[i][j][profile[i][j].find("<span>")+6 : profile[i][j].find("</span>")]
        print(char_name, char_cls)