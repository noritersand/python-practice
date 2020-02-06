obj = {
  "type": "push",
  "targets": [
    "stream",
    "android",
    "ios"
  ],
  "push":{
    "type": "sms_changed",
    "source_device_iden": "ujzEgGbqE7UsjuPC94UrhA",
    "notifications": [{
        "thread_id": "316",
        "title": "부계",
        "body": "ㅁ",
        "timestamp":1648564069
      }
    ]
  }
}
print(obj['push']['notifications'][0]['body']) # ㅁ
