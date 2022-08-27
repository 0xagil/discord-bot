from pydoc import describe
from api import ApiClient
import time
from termcolor import colored
from socketer import DiscordSocketClient
from threading import Thread

class Account:
    def __init__(self, token, password, id, monitor=False, settings={}, storage=None):
        self.password = password
        self.token = token
        if type(id) == int:
            self.description = f"Bot {id}"
            self.botId = id
        else:
            self.description = id
        self.monitor = monitor
        self.settings = settings
        self.storage = storage
        self.accountState = False
        self.messageCount = 0

    def setup(self):
        self.discord_websocket = DiscordSocketClient(self.token, self.description, scraping=self.monitor, storage=self.storage, settings=self.settings)
        Thread(target=self.discord_websocket.start).start()
        while not self.discord_websocket.analyticsToken:
            time.sleep(.1)
        self.storage.printGreen(f"Launched Websocket", self.description)
        self.api = ApiClient(self.token, self.password, self.discord_websocket.analyticsToken)
        state = self.api.login()
        if state == "good":
            self.storage.printGreen(f"Login successful", self.description)
            self.api.changeStatus()
            self.accountState = True
        elif state == 'locked':
            self.storage.printRed(f"Token: {self.token[:20]} locked", self.description)
            self.accountState = False
        
    def run(self):
        state, code = self.api.joinGuild(self.settings['invite'])
        if state:
            self.storage.printGreen(f"Joined Guild: {self.api.guildName}", self.description)
        elif code == 403:
            self.storage.printRed(f"Joiner - Locked account", self.description)
            self.accountState = False
            return
        elif code == 404:
            self.storage.printRed(f"Joiner - Banned account", self.description)
            self.accountState = False
            return
        self.changeAccount()
        while self.accountState:
            if len(self.storage.userList) > 0:
                userId = self.storage.userList.pop(0)
                state, code = self.messageUser(userId, self.settings['messageContent'])
                if state:
                    self.messageCount += 1
                    self.storage.printGreen(f"Message - Sent to {userId} [DM: {self.messageCount}]", self.description)
                    time.sleep(65)
                elif code == 403:
                    self.storage.printRed(f"Message - Locked account", self.description)
                    self.accountState = False
                    self.storage.userList.append(userId)
                elif code == 403:
                    self.storage.printYellow(f"Message - Rate limit exceeded", self.description)
                    time.sleep(120)
                elif code == 500:
                    self.storage.printYellow(f"Message - User {userId} cannot receive messages", self.description)
                    time.sleep(65)
                elif code == 400:
                    self.storage.printRed(f"Message - Captcha account", self.description)
                    self.accountState = False
                    self.storage.userList.append(userId)

            time.sleep(.02)
        self.storage.printYellow(f"Session ended", self.description)

    def changeAccount(self):
        state, code = self.api.changeProfileName(self.settings['desiredName'])
        if code == 200:
            self.storage.printGreen(f"Username - Changed to {self.settings['desiredName']}", self.description)
        elif code == 403:
            self.storage.printYellow(f"Username - Too many have this name", self.description)
        elif code == 404:
            self.storage.printRed(f"Username - Rate limit exceeded", self.description)
        time.sleep(2)
        state = self.api.changeProfilePicture(self.settings['profilePicture'])
        if state:
            self.storage.printGreen(f"ProfilePicture - Changed successfuly", self.description)
        else:
            self.storage.printRed(f"ProfilePicture - Rate limit", self.description)

    def messageUser(self, userId, message_content):
        return self.api.sendMessage(userId, message_content)

