from account import Account
import time
from threading import Thread
import json
from termcolor import colored

with open('settings.json') as f:
    settings = json.load(f)


def bot1(userStorage, id):
    account = userStorage.tokenList.pop(0)
    token = account.split(":")[2]
    password = account.split(":")[1]
    acc = Account(token, password, id+1, monitor=False, settings=settings, storage=userStorage)
    acc.setup()
    acc.run()
    userStorage.semThreads.append(id)

def start1(userStorage):
    threads = []
    while userStorage.tokenList:
        id = userStorage.semThreads.pop(0)
        t = Thread(target=bot1, args=(userStorage, id))
        t.daemon = True
        threads.append(t)
        t.start()
        while len(userStorage.semThreads) == 0:
            time.sleep(1) 
    userStorage.printYellow("All tokens are in use", "Main")
    for t in threads:
        t.join()

def setup(userStorage):
    if settings["monitorToken1"]:
        acc = Account(settings["monitorToken1"], "password", "Monitor 1", monitor=True, settings=settings, storage=userStorage)
        Thread(target=acc.setup).start()
    elif settings["monitorToken2"]:
        acc = Account(settings["monitorToken2"], "password", "Monitor 2", monitor=True, settings=settings, storage=userStorage)
        Thread(target=acc.setup).start()


class StoreUser():
    def __init__(self) -> None:
        self.blacklist = []
        self.userList = []
        self.semThreads = list(range(settings["maxThreads"]))
        self.semCongruent = list(range(settings['congruentThreads']))
        with open('tokens.txt') as f:
            self.tokenList = f.read().splitlines() 
    
    def printBlank(self, suffix, description):
        prefix = f'[{description} - {time.strftime("%H:%M:%S")}] >> '
        print(prefix + suffix)

    def printGreen(self, suffix, description):
        prefix = f'[{description} - {time.strftime("%H:%M:%S")}] >> '
        print(prefix + colored(suffix, 'green'))
    
    def printRed(self, suffix, description):
        prefix = f'[{description} - {time.strftime("%H:%M:%S")}] >> '
        print(prefix + colored(suffix, 'red'))
    
    def printYellow(self, suffix, description):
        prefix = f'[{description} - {time.strftime("%H:%M:%S")}] >> '
        print(prefix + colored(suffix, 'yellow'))

if __name__ == '__main__':
    userStorage = StoreUser()
    setup(userStorage)
    start1(userStorage)

