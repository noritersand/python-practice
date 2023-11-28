import os
import requests  # request img from web
import shutil  # save img locally

from target_list import download_target_list

dependsOnUrl = False # True
extension = ''
download_target_list

parentDir = 'c:/dev/test/'
if not os.path.isdir(parentDir):
    os.mkdir(parentDir)

str = ''
for target in download_target_list:
    url = target['url']
    if (dependsOnUrl):
        extension = url[url.rfind('.'): len(url)]
    fileName = target['name'] + extension
    str += 'url = ' + url + '\n'
    str += 'fileLocation = ' + parentDir + fileName + '\n\n'

with open(parentDir + 'preview.txt', 'w') as f:
    f.write(str)

for target in download_target_list:
    url = target['url']
    if (dependsOnUrl):
        extension = url[url.rfind('.'): len(url)]
    fileName = target['name'] + extension
    destination = parentDir + fileName
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(destination, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ', destination)
    else:
        print('Image Couldn\'t be retrieved')
