import re
kor_txt = """가나다 ㄱㄴㄷ ㅏㅓㅐ        |        ㄲ킈ㅗ ㅗㅜㅑㅒfd|jkaFSA 498130$#@!*&^ %)(-_=+ []{}<>,./?'"`"')"""
# kor_txt = kor_txt.replace("|","")
print(re.sub('[^ㄱ-ㅎ|ㅏ-ㅣ가-힣|a-zA-Z|0-9 |`!@#$%^&*()\[\]{}\-\_\'\"><\/\?]', '', kor_txt))

