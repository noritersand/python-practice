import os

sourceDir = "c:/dev/temp/"

for fileName in os.listdir(sourceDir):
    source = sourceDir + fileName
    print(source)

    # 파일명에서 hashcode 제거하기
    # if "hashcode" not in fileName:
        # continue
    # print(fileName[8:len(fileName)])
    # destination = folder + fileName[8 : len(fileName)]
    # os.rename(source, destination)

    # 언더바를 하이픈으로
    newFileName = fileName.replace('_', '-')
    print(newFileName)
    destination = sourceDir + newFileName
    os.rename(source, destination)
    
# print(os.listdir(folder))