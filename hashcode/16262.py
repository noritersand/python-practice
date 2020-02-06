class Queue:
    maxsize = None

    def __init__(self, maxsize):
        self.items = maxsize

queue = Queue(maxsize = 10)
print(queue.items) # 10 출력