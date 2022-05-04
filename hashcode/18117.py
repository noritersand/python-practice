import os

file_der1 = 'C:/Users/maker01/Downloads/a'

if os.path.exists(file_der1):
    file_list1 = os.listdir(file_der1)
else:
    print("없지롱")
