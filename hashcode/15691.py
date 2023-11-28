from datetime import datetime
now = datetime.now()
print(type(now))
print(now.date())

if now.hour >= 0 and now.hour < 7:
    print('ㅎㅇ')

