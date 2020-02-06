from fileinput import filename
import os

folder = "c:/dev/repo/python-lab/hashcode/"

for fileName in os.listdir(folder):
    if "hashcode" not in fileName:
        continue

    source = folder + fileName
    # print(source)
    # print(fileName[8:len(fileName)])
    destination = folder + fileName[8 : len(fileName)]

    os.rename(source, destination)

print(os.listdir(folder))
