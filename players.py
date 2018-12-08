import json
import pandas as pd
import time
from scrape import Scraper


def pandaFrame(data):
    frame = pd.DataFrame(data=players)
    print(frame.head())


def jsondump(data):
    with open('result.json', 'w') as fp:
        json.dump(data, fp)


def main():
    t0 = time.time()

    LETTERS = 24

    for i in range(0, LETTERS, 4):

        # letters for each thread
        letter1 = chr(ord('a') + i)
        letter2 = chr(ord('a') + i + 1)
        letter3 = chr(ord('a') + i + 2)
        letter4 = chr(ord('a') + i + 3)

        thread1 = Scraper(('Thread ' + str(i)), letter1)
        thread2 = Scraper(('Thread ' + str(i + 1)), letter2)
        thread3 = Scraper(('Thread ' + str(i + 2)), letter3)
        thread4 = Scraper(('Thread ' + str(i + 3)), letter4)

        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()

        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()

    thread24 = Scraper(('Thread ' + str(24)), chr(ord('a') + 24))
    thread25 = Scraper(('Thread ' + str(25)), chr(ord('a') + 25))
    thread24.start()
    thread25.start()
    thread24.join()
    thread25.join()

    t1 = time.time()
    total = t1-t0
    print('ran for: ' + str(total))

main()
