import os
import requests  # request img from web
import shutil  # save img locally

from target_list import image_list

dependsOnUrl = False # True
extension = '.png'
target = image_list

parentDir = "c:/dev/test/"
if not os.path.isdir(parentDir):
    os.mkdir(parentDir)

str = ""
for ele in target:
    url = ele["url"]
    if (dependsOnUrl):
        extension = url[url.rfind("."): len(url)]
    fileName = ele["name"] + extension
    str += "url = " + url + "\n"
    str += "fileLocation = " + parentDir + fileName + "\n\n"

with open(parentDir + "preview.txt", "w") as f:
    f.write(str)

for ele in target:
    url = ele["url"]
    if (dependsOnUrl):
        extension = url[url.rfind("."): len(url)]
    fileName = ele["name"] + extension
    destination = parentDir + fileName
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(destination, "wb") as f:
            shutil.copyfileobj(res.raw, f)
        print("Image sucessfully Downloaded: ", destination)
    else:
        print("Image Couldn't be retrieved")
