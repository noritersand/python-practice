str = 'Hell?O'
str2 = 'hell?o'

# print(str.islower()) # False
# print(str2.islower()) # True

# if (str2.islower()):
    # print('It is lowercase') # 'It is lowercase'

str3 = ' H E L L O ';
# print(str3.replace(' ', ''))

str4 = '''


                                공백이 엄청 많은
            어떤 텍스트


                            '''
print(str4.strip()) # 제44회 공군참모총장배 Space Challenge 2023 경인지역 예선대회
# print(str4.replace(' ', ''))

str5 = 'EVENT_CD|AWARD_NO'
new_var = str5.split('|')
print(new_var)  # ['EVENT_CD', 'AWARD_NO']
print(new_var[0])  # EVENT_CD
print(new_var[1])  # 'AWARD_NO'
