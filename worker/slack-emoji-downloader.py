import os
import requests  # request img from web
import shutil  # save img locally

target = [
    {
        "name": "son-astonished",
        "value": "https://emoji.slack-edge.com/T02R0EL7S9J/son-astonished/3c0aeaba674ef209.png",
    },
    {
        "name": "son-blood-quest",
        "value": "https://emoji.slack-edge.com/T02R0EL7S9J/son-blood-quest/fe160e4d3614ba37.png",
    },
    {
        "name": "son-carrot",
        "value": "https://emoji.slack-edge.com/T02R0EL7S9J/son-carrot/3cc5880e64c7de05.png",
    },
    {
        "name": "son-covid",
        "value": "https://emoji.slack-edge.com/T02R0EL7S9J/son-covid/3a514cb4294644d9.png",
    },
]

parentDir = "c:/dev/test/"
if not os.path.isdir(parentDir):
    os.mkdir(parentDir)

str = ""
for ele in target:
    url = ele["value"]
    fileName = ele["name"] + url[url.rfind(".") : len(url)]
    str += "url = " + url + "\n"
    str += "fileLocation = " + parentDir + fileName + "\n\n"

with open(parentDir + "preview.txt", "w") as f:
    f.write(str)

for ele in target:
    url = ele["value"]
    fileName = ele["name"] + url[url.rfind(".") : len(url)]
    destination = parentDir + fileName
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(destination, "wb") as f:
            shutil.copyfileobj(res.raw, f)
        print("Image sucessfully Downloaded: ", destination)
    else:
        print("Image Couldn't be retrieved")
