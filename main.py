import threading
import time
import random

class Plate:
    def __init__(self):
        self.apple_count = 0
        self.orange_count = 0
        self.condition = threading.Condition()

    def add_apple(self):
        with self.condition:
            while self.apple_count + self.orange_count >= 1:
                self.condition.wait()  # 等待水果不超2
                self.condition.notify_all()  # 通知所有线程有新水果放入
            self.apple_count += 1
            print("父亲放入了一个苹果")


    def add_orange(self):
        with self.condition:
            while self.apple_count + self.orange_count >= 1:
                self.condition.wait()  # 等待水果数不超过2
                self.condition.notify_all()  # 通知所有线程有新水果放入
            self.orange_count += 1
            print("母亲放入了一个橘子")


    def take_orange(self):
        with self.condition:
            while self.orange_count == 0:
                self.condition.wait()  # 等待至少有一个橘子的条件
            self.orange_count -= 1
            print("儿子拿走了一个橘子")
            self.condition.notify_all()  # 通知其他线程有橘子被拿走

    def take_apple(self):
        with self.condition:
            while self.apple_count == 0:
                self.condition.wait()  # 等待至少有一个苹果的条件
            self.apple_count -= 1
            print("女儿拿走了一个苹果")
            self.condition.notify_all()  # 通知其他线程有苹果被拿走


def father(plate):
    while True:
        plate.add_apple()
        time.sleep(2)

def mother(plate):
    while True:
        plate.add_orange()
        time.sleep(2)

def son(plate):
    while True:
        plate.take_orange()
        time.sleep(2)

def daughter(plate):
    while True:
        plate.take_apple()
        time.sleep(2)

if __name__ == "__main__":
    plate = Plate()

    threads = [
        threading.Thread(target=father, args=(plate,)),
        threading.Thread(target=mother, args=(plate,)),
        threading.Thread(target=son, args=(plate,)),
        threading.Thread(target=daughter, args=(plate,))
    ]

    random.shuffle(threads)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()#阻塞，使其等待
