import os
import requests  # request img from web
import shutil  # save img locally
from target_list import download_target_list

dependsOnUrl = False # True
extension = ''
download_target_list

parentDir = './output/'
if not os.path.isdir(parentDir):
    os.mkdir(parentDir)

preview_content = ''
for target in download_target_list:
    url = target['url']
    if dependsOnUrl:
        extension = url[url.rfind('.'):]
    
    fileName = target['name'] + extension
    fileLocation = os.path.join(parentDir, fileName)
    preview_content += f"url = {url}\n"
    preview_content += f"fileLocation = {fileLocation}\n\n"

preview_path = os.path.join(parentDir, 'preview.txt')
with open(preview_path, 'w', encoding='utf-8') as f:
    f.write(preview_content)

for target in download_target_list:
    url = target['url']
    if (dependsOnUrl):
        extension = url[url.rfind('.'): len(url)]
    fileName = target['name'] + extension
    destination = parentDir + fileName
    
    try:
        with requests.get(url, stream=True) as res:
            if res.status_code == 200:
                with open(destination, 'wb') as f:
                    shutil.copyfileobj(res.raw, f)
                print(f"Image successfully Downloaded: {destination}")
            else:
                print(f"Image Couldn't be retrieved. url: {url}, status_code: {res.status_code}")
    except Exception as e:
        print(f"Error occurred while downloading {url}: {e}")