import time


def sleep_and_countdown(sec: int, by_sec: int):

    for i in range(sec):

        time.sleep(by_sec)

        print("{} sec left".format(sec - i))