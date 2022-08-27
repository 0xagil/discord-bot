from dis import dis
import websocket
import json
import _thread as thread
import time


class DiscordSocketClient:

    def __init__(self, token, description, scraping=False, storage="", settings={}):
        self.token = token
        self.heartbeat_interval = 41
        self.counter = 0
        self.index = 0
        self.fetchedUsers = []
        self.newUser_old = []
        self.newUser = []
        self.finished = False
        self.scraping = scraping
        self.logIn = False
        self.settings=settings
        self.fristRun = True
        self.storage = storage
        self.description = description
        self.analyticsToken = ""
    
    def start(self):
        self.ws = websocket.WebSocketApp("wss://gateway.discord.gg/?encoding=json&v=9",
                                        on_message=self.on_message,
                                        on_error=self.on_error,
                                        on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()

    def on_message(self, object, message):
        message = json.loads(message)
        type = message['t']
        if not type:
            type = 'None'
        if type == 'READY':
            self.analyticsToken = message['d']['analytics_token']
            self.logIn = True
            self.ws.send(json.dumps({"op":4,"d":{"guild_id":None,"channel_id":None,"self_mute":True,"self_deaf":False,"self_video":False}}))
            if self.scraping:
                self.scrape()
        if self.scraping:
            if type == 'MESSAGE_CREATE':
                userId = message['d']['author']['id']
                if 'channel_id' in message['d']:
                    channelId = message['d']['channel_id']
                else:
                    channelId = None
                guildId = message['d']['guild_id']
                if guildId == self.settings['guildId']:
                    #print(message)
                    if self.settings["welcomeChannel"]:
                        if channelId == self.settings["welcomeChannel"]:
                            userId = message['d']['mentions'][0]['id']
                            self.storage.printBlank(f"Fetched User: {userId} - Welcome Channel", self.description)
                        else:
                            self.storage.printBlank(f"Fetched User: {userId} - Message", self.description)

                    else:
                        self.storage.printBlank(f"Fetched User: {userId} - Message", self.description)
            elif type == 'MESSAGE_REACTION_ADD':
                userId = message['d']['user_id']
                messageId = message['d']['message_id']
                channelId = message['d']['channel_id']
                guildId = message['d']['guild_id']
                if guildId == self.settings['guildId'] and channelId == self.settings['reactionChannel'] and userId not in self.fetchedUsers:
                    self.storage.userList.append(userId)
                    self.fetchedUsers.append(userId)
                    self.storage.printBlank(f"Fetched User: {userId} - Reaction", self.description)
            elif type == 'GUILD_MEMBER_LIST_UPDATE':
                
                if message['d']['ops'][0]['op'] == 'SYNC':
                    self.newUser_old = self.newUser.copy()
                    for items in message['d']['ops'][0]['items']:
                        if 'member' in items:
                            #states: idle, online, dnd
                            userId = items['member']['user']['id']
                            if 'mobile' in items['member']['presence']['client_status']:
                                mobileState = items['member']['presence']['client_status']['mobile']
                            else:
                                mobileState = 'dnd'
                            if 'web' in items['member']['presence']['client_status']:
                                webState = items['member']['presence']['client_status']['web']
                            else:
                                webState = 'dnd'
                            if userId not in self.fetchedUsers:
                                if not self.fristRun:
                                    if webState == 'idle' or webState == 'online':
                                        self.storage.printBlank(f"Fetched User: {userId} - Browser State: {webState}", self.description)
                                        self.storage.userList.append(userId)    
                                
                                self.fetchedUsers.append(userId)
                            self.newUser.append(userId)
                if len(self.newUser_old) == len(self.newUser):
                    self.index = 0
                    self.newUser = []
                    if self.fristRun:
                        self.storage.printBlank(f"Fetched all users", self.description)
                        self.fristRun = False
                if not self.finished and self.scraping:
                    self.scrape()
        return message

    def on_error(self, error, test):
        print("Error:", test)
        return error

    def on_close(self, object, code, error):
        if code == 4008:
            self.index = 0
        self.start()

    def heartbeat(self, *args):
        self.driver = True
        while self.driver:
            try:
                heartbeatJSON={'op':1, 'token': self.token, 'd': self.counter}
                time.sleep(self.heartbeat_interval)
                self.ws.send(json.dumps(heartbeatJSON))
                self.counter += 1
            except KeyboardInterrupt:
                self.driver = False
            except:
                pass
        self.ws.close()
        print("Heartbeat terminating...")

    def on_open(self, okay):
        _data = {"d": {
                "capabilities": 351,
                "client_state": {
                "guild_hashes": {},
                "highest_last_message_id": 0,
                "read_state_version": -1,
                "useruser_guild_settings_version": -1
                },
                "compress": False,
                "large_threshold": 100,
                "properties": {
                "browser": "Discord Android",
                "browser_user_agent": "Discord-Android/126019",
                "client_build_number": 126019,
                "client_version": "126.19 - Stable",
                "device": "Android SDK built for x86_64, sdk_phone_x86_64",
                "os": "Android",
                "os_sdk_version": "27",
                "os_version": "8.1.0",
                "system_locale": "en-US"
                },
                "token": self.token
            },
            "op": 2
            }
        self.ws.send(json.dumps(_data))
        thread.start_new_thread(self.heartbeat, ())

    def scrape(self):
        if self.index == 0:
            self.ranges = [[0,99]]
        elif self.index == 1:
            self.ranges = [[0,99], [100, 199]]
        elif self.index == 2:
            self.ranges = [[0,99], [100, 199], [200, 299]]
        else:
            if len(self.ranges) == 3:
                self.ranges.pop(1)
                self.index -= 1
            else:
                self.ranges.append([self.index*100, self.index*100+99])
        _data = {"op":14, 
                 "d": {"guild_id": self.settings['guildId'],
                       "channels": {self.settings['channelId']: self.ranges}}
                }
        self.ws.send(json.dumps(_data))
        self.index += 1

