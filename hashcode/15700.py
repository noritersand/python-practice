import requests

# def fn(keyword):
#     r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
#     print('r.status_code:', r.status_code) # 200
#     print('r.headers:', r.headers['content-type']) # 'application/json; charset=utf8'
#     print('r.encoding:', r.encoding) # 'utf-8'
#     print('r.text:', r.text) # '{"type":"User"...'
#     print('r.json:', r.json())
#     for i in r.json():
#         if(i['keyword'] == keyword) : # 검색키워드
#             amount = i['bidAmt']
#     return amount
# fn('hi')

def fn(n):
    if (n == 1):
        amount = 'return value'
    return amount

fn(2)