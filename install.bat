@echo off
echo 필요 패키지들을 설치합니다.
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
.\python\python.exe .\get-pip.py --no-warn-script-location
echo Lib\site-packages>> .\python\python39._pth
echo ..>> .\python\python39._pth
.\python\python.exe -m pip install --upgrade pip --no-warn-script-location
.\python\python.exe -m pip install -r .\requirements.txt --no-warn-script-location
pause