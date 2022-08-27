import httpx
import json
import time
import base64
import random
import uuid
from datetime import datetime
from spinner import spin_text

class ApiClient:
    def __init__(self, token, password, analytics_token, timeout=1):
        self.genHeader()
        self.proxies = {
            "http://": "",
            "https://": "",
        }
        self.client = httpx.Client(http2=True, proxies=self.proxies)
        self.timeout = timeout
        self.uuid = str(uuid.uuid4())
        self.token = token
        self.password = password
        self.analytics_token = analytics_token
        

    def nonce(self):
        date = datetime.now()
        unixts = time.mktime(date.timetuple())
        return str((int(unixts) * 1000 - 1420070400000) * 4194304)

    def genHeader(self):
        xproperties = {
        "browser":"Discord Android",
        "browser_user_agent":f"Discord-Android/126019",
        "client_build_number":126019,
        "client_version":"126.19 - Stable",
        "device":"Android SDK built for x86_64, sdk_phone_x86_64",
        "os":"Android",
        "os_sdk_version":"27",
        "os_version":"10.1.0",
        "system_locale":"en-US",
        "accessibility_support_enabled":False,
        "accessibility_features":random.randrange(1, 200),
        "client_performance_cpu":-67,
        "client_performance_memory":random.randrange(113708, 413708),
        "cpu_core_count":random.randrange(1, 5)
        }
        self.xproperties_encoded = base64.b64encode(json.dumps(xproperties).encode('ascii')).decode("utf-8")
        self.headers = {"accept-encoding": "gzip", "accept-language": "en-US", "connection": "keep-alive", "host": "discord.com", "user-agent": xproperties["browser_user_agent"]}
    
    def genContextProperties(self, data):
        self.contextproperties_encoded = base64.b64encode(json.dumps(data).encode('ascii')).decode("utf-8")
        return self.contextproperties_encoded

    def launchScience(self):
        schienceData1 = {"events": [
            {
            "properties": {
                "event_time_name": "GatewayConnection",
                "gateway_connection": 5380,
                "gateway_hello": -1,
                "voice_connection": -1,
                "stream_requested": -1,
                "stream_connection": -1,
                "stream_first_frame": -1,
                "video_first_frame": -1,
                "media_engine_connection": -1,
                "connection_video_first_frame": -1,
                "connection_stream_first_frame": -1
            },
            "type": "video_event_times"
            }
        ],
        "token": self.analytics_token
        }
        schienceData2 = {
        "events": [
            {
            "properties": {
                "opened_from": "launcher",
                "theme": "dark",
                "load_id": self.uuid
            },
            "type": "app_opened"
            },
            {
            "properties": {
                "foreground_app_enabled": True,
                "os_enabled": True,
                "background_app_enabled": True
            },
            "type": "notification_permission_status"
            },
            {
            "properties": {
                "event_time_name": "GatewayConnection",
                "gateway_connection": 343,
                "gateway_hello": -1,
                "voice_connection": -1,
                "stream_requested": -1,
                "stream_connection": -1,
                "stream_first_frame": -1,
                "video_first_frame": -1,
                "media_engine_connection": -1,
                "connection_video_first_frame": -1,
                "connection_stream_first_frame": -1
            },
            "type": "video_event_times"
            },
            {
            "properties": {
                "screen_name": "guild",
                "load_id": "bf0d937b-5b3c-4db0-8014-3eca432ee40c",
                "duration_ms_since_app_opened": 6137,
                "has_cached_data": False,
                "theme": "dark"
            },
            "type": "app_ui_viewed"
            },
            {
            "properties": {
                "duration_ms_since_connection_start": 9483,
                "duration_ms_since_identify_start": 9140,
                "identify_total_server_duration_ms": 2366,
                "identify_api_duration_ms": 268,
                "identify_guilds_duration_ms": 18,
                "compressed_byte_size": 2075845,
                "uncompressed_byte_size": 14920243,
                "compression_algorithm": "zlib",
                "packing_algorithm": "json",
                "unpack_duration_ms": 439,
                "is_reconnect": False,
                "is_fast_connect": False,
                "num_guilds": 173,
                "num_guild_channels": 19664,
                "num_guild_category_channels": 2257
            },
            "type": "ready_payload_received"
            }
        ],
        "token": self.analytics_token
        }
        while True:
            try:
                r = self.client.post("https://discord.com/api/v9/science", data=json.dumps(schienceData1), headers=self.headers, timeout=10)
                r = self.client.post("https://discord.com/api/v9/science", data=json.dumps(schienceData2), headers=self.headers, timeout=10)
                break
            except Exception:
                time.sleep(self.timeout)
    
    def login(self):
        url = "https://discord.com/api/v9/experiments"
        while True:
            try:
                r = self.client.get(url, headers=self.headers)
                break
            except Exception:
                time.sleep(self.timeout)
        fingerprint = r.json()['fingerprint']
        self.headers["content-type"] = "application/json; charset=UTF-8"
        self.headers['x-fingerprint'] = fingerprint
        self.launchScience()
        del self.headers['x-fingerprint']
        #now login
        self.headers["authorization"] = self.token
        self.headers["x-super-properties"] = self.xproperties_encoded
        while True:
            try:
                r = self.client.get("https://discord.com/api/v9/users/@me", headers=self.headers, timeout=10)
                break
            except Exception:
                time.sleep(self.timeout)
        if 'You need to verify' in r.text:
            return 'locked'
        self.username = r.json()["username"]
        self.id = r.json()["id"]
        if self.username:
            return "good"


    def changeProfilePicture(self, image_file):
        _data1 = {
        "events": [
            {
            "properties": {
                "settings_type": "user",
                "destination_pane": "User Profile"
            },
            "type": "settings_pane_viewed"
            }
        ],
        "token": self.analytics_token
        }
        _data2 = {
        "events": [
            {
            "properties": {
                "event_time_name": "GatewayConnection",
                "gateway_connection": 326,
                "gateway_hello": -1,
                "voice_connection": -1,
                "stream_requested": -1,
                "stream_connection": -1,
                "stream_first_frame": -1,
                "video_first_frame": -1,
                "media_engine_connection": -1,
                "connection_video_first_frame": -1,
                "connection_stream_first_frame": -1
            },
            "type": "video_event_times"
            },
            {
            "properties": {
                "event_time_name": "GatewayHello",
                "gateway_connection": 326,
                "gateway_hello": 2,
                "voice_connection": -1,
                "stream_requested": -1,
                "stream_connection": -1,
                "stream_first_frame": -1,
                "video_first_frame": -1,
                "media_engine_connection": -1,
                "connection_video_first_frame": -1,
                "connection_stream_first_frame": -1
            },
            "type": "video_event_times"
            }
        ],
        "token": self.analytics_token
        }
        with open(image_file, "rb") as img_file:
            my_string = base64.b64encode(img_file.read()).decode("utf-8")
        burp0_json={
        "avatar": "data:image/png;base64,"+my_string}
        while True:
            try:
                self.client.post("https://discord.com/api/v9/science", data=json.dumps(_data1), headers=self.headers, timeout=10)
                self.client.post("https://discord.com/api/v9/science", data=json.dumps(_data2), headers=self.headers, timeout=10)
                r = self.client.patch("https://discord.com/api/v9/users/@me", headers=self.headers, json=burp0_json, timeout=10)
                if "RATE_LIMIT" in r.text:
                    return False
                else:
                    return True
            except Exception:
                time.sleep(1)

    def changeProfileName(self, name):
        _data1 = {
        "events": [
            {
            "properties": {
                "settings_type": "user",
                "destination_pane": "User Profile"
            },
            "type": "settings_pane_viewed"
            }
        ],
        "token": self.analytics_token
        }
        _data2 = {
        "events": [
            {
            "properties": {
                "location_section": "",
                "type": "Account Settings Password Verification"
            },
            "type": "open_modal"
            }
        ],
        "token": self.analytics_token
        }
        
        while True:
            try:
                self.client.post("https://discord.com/api/v9/science", data=json.dumps(_data1), headers=self.headers, timeout=10)
                self.client.post("https://discord.com/api/v9/science", data=json.dumps(_data2), headers=self.headers, timeout=10)
                r = self.client.patch("https://discord.com/api/v9/users/@me", data=json.dumps({"username": name, "password": self.password, "push_provider": "gcm"}), headers=self.headers)
                if "RATE_LIMIT" in r.text:
                    return False, 404
                elif "Too many users have this username" in r.text:
                    return False, 403
                else:
                    return True, 200
            except Exception:
                time.sleep(1)
    
    def changeStatus(self):
        _data = {
        "events": [
            {
            "properties": {
                "has_custom_status": False,
                "location_section": "Account Panel",
                "type": "User Status Menu",
                "location_object": "Avatar"
            },
            "type": "open_popout"
            }
        ],
        "token": self.analytics_token
        }
        while True:
            try:
                self.client.post("https://discord.com/api/v9/science", data=json.dumps(_data), headers=self.headers, timeout=10)
                r = self.client.patch("https://discord.com/api/v9/users/@me/settings", data=json.dumps({"status": "invisible"}), headers=self.headers, timeout=10)
                if r.status_code == 200:
                    return True
                else:
                    return False
            except Exception:
                time.sleep(1)
   
    def sendMessage(self, userId, message_content):
        message_content = spin_text(message_content)
        url = "https://discord.com/api/v9/users/@me/channels"
        _data = {"recipients": [userId]}
        while True:
            try:
                r = self.client.post(url, data=json.dumps(_data), headers=self.headers, timeout=10)
                break
            except Exception:
                time.sleep(self.timeout)
        if r.status_code == 200:
            channel_id = r.json()['id']
        elif r.status_code == 401:
            return False, 401
        elif r.status_code == 403:
            return False, 403
        elif r.status_code == 429:
            return False, 429
        elif "Cannot send messages to this user" in r.text:
            return False, 500
        else:
            return False, 500
        channelId = r.json()['id']
        _data2 = {"events": [
            {
            "properties": {
                "channel_is_nsfw": False,
                "channel_view": "Full View",
                "channel_type": 1,
                "channel_id": channelId,
                "channel_size_total": 1
            },
            "type": "channel_opened"
            }
        ],
        "token": self.analytics_token
        }
        while True:
            try:
                self.client.post("https://discord.com/api/v9/science", data=json.dumps(_data2), headers=self.headers, timeout=10)
                break
            except Exception:
                time.sleep(self.timeout)
        username = r.json()['recipients'][0]['username']
        burp0_json = {
        "content": message_content.replace("@user", f"<@{userId}>"),
        "nonce": self.nonce(),
        "tts": False
        }
        url = f"https://discord.com/api/v9/channels/{channelId}/messages"
        while True:
            while True:
                try:
                    res = self.client.post(url, data=json.dumps(burp0_json), headers=self.headers, timeout=10)
                    break
                except Exception:
                    time.sleep(1)
            
            if res.status_code == 403 and res.json()["code"] == 40003:
                return False, 403
            elif res.status_code == 429:
                return False, 403
            elif 'Unauthorized' in res.text:
                return False, 403
            elif 'Cannot send messages to this user' in res.text:
                return False, 500
            elif "captcha_sitekey" in res.text:
                #captcha_key = self.solveCaptcha(res.json()['captcha_sitekey'], res.json()['captcha_rqdata'])
                #burp0_json["captcha_key"] = captcha_key
                #burp0_json["captcha_rqtoken"] = res.json()['captcha_rqtoken']
                #burp0_json["nonce"] = self.nonce()
                return False, 400
            else:
                return True, 200
    
    def solveCaptcha(self, captcha_sitekey, captcha_rqdata):
        api = ""
        url = "http://capcat.xyz/api/tasks"
        headers = {"Content-Type": "application/json"}
        data = {
            'apikey': api,
            'sitkey': captcha_sitekey
        }
        while True:
            try:
                r = self.client.post(url, headers=headers, data=json.dumps(data))
                ids = r.json()['id']
                print(r.text)
                break
            except:
                time.sleep(10)
        
        url="http://capcat.xyz/api/result"
        data = {
            'apikey': api,
            'id': ids
        }
        while True:
            try:
                r = self.client.post(url, headers=headers, data=json.dumps(data))
                if "working" in r.text:
                    time.sleep(15)
                elif r.json()['code'] == 1:
                    print("Solved Captcha")
                    return r.json()['data']
            except:
                time.sleep(10)

    def guildScience1(self):
        _data1 = {
        "events": [
            {
            "properties": {
                "name": "2021-06_desktop_school_hubs",
                "revision": 0,
                "population": -1,
                "bucket": 1
            },
            "type": "experiment_user_triggered"
            },
            {
            "properties": {
                "tutorial": "create-first-server-tip",
                "acknowledged": True
            },
            "type": "close_tutorial"
            }
        ],
        "token": self.analytics_token
        }
        _data2 = {"events": [
            {
            "properties": {
                "flow_type": "Mobile NUX Post Reg",
                "from_step": "Registration",
                "to_step": "Ask to join",
                "skip": False
            },
            "type": "nuo_transition"
            },
            {
            "properties": {
                "impression_group": "guild_add_flow"
            },
            "type": "impression_guild_add_join"
            }
        ],
        "token": self.analytics_token
        }
        while True:
            try:
                r = self.client.post("https://discord.com/api/v9/science", data=json.dumps(_data1), headers=self.headers, timeout=10)
                r = self.client.post("https://discord.com/api/v9/science", data=json.dumps(_data2), headers=self.headers, timeout=10)
                return
            except Exception as e:
                time.sleep(1)

    def guildScience2(self, invite, channelId, guildId):
        _data = {"events": [
            {
            "properties": {
                "flow_type": "Mobile NUX Post Reg",
                "from_step": "Ask to join",
                "to_step": "Accept Instant Invite",
                "skip": False,
                "seconds_on_from_step": 234146
            },
            "type": "nuo_transition"
            },
            {
            "properties": {
                "voice_action": False,
                "type": "invite"
            },
            "type": "deep_link_received"
            },
            {
            "properties": {
                "invite_code": invite
            },
            "type": "invite_opened"
            },
            {
            "properties": {
                "authenticated": True,
                "channel_id": channelId,
                "channel_type": 0,
                "code": invite,
                "guild_id": guildId,
                "invite_type": "Server Invite",
                "resolved": False,
                "size_online": 896,
                "size_total": 6858,
                "request_method": "GET",
                "status_code": 200,
                "url": f"https://discord.com/api/v9/invites/{invite}?with_counts=true",
                "user_banned": False
            },
            "type": "network_action_invite_resolve"
            },
            {
            "properties": {
                "resolved": True,
                "authenticated": True,
                "location": "Join Guild Modal",
                "code": invite,
                "channel_id": channelId,
                "channel_type": 0,
                "guild_id": guildId
            },
            "type": "resolve_invite"
            },
            {
            "properties": {
                "resolved": True,
                "authenticated": True,
                "location": "",
                "code": invite,
                "channel_id": channelId,
                "channel_type": 0,
                "guild_id": guildId
            },
            "type": "resolve_invite"
            }
        ],
        "token": self.analytics_token
        }
        while True:
            try:
                r = self.client.post("https://discord.com/api/v9/science", data=json.dumps(_data), headers=self.headers, timeout=10)
                return
            except Exception:
                time.sleep(self.timeout)

    def joinGuild(self, invite):
        self.guildScience1()
        url = f"https://discord.com/api/v9/invites/{invite}?inputValue={invite}&with_counts=true&with_expiration=true"
        while True:
            try:
                r = self.client.get(url, headers=self.headers, timeout=10)
                break
            except Exception:
                time.sleep(self.timeout)
        if r.status_code == 403:
            return False, 403
        self.guildName = r.json()['guild']['name']
        self.guildId = r.json()['guild']['id']
        verification_level = r.json()['guild']['verification_level']
        try:
            self.welcomeChannel = r.json()['guild']['welcome_screen']['welcome_channels'][0]['channel_id']
        except:
            self.welcomeChannel = 0
        self.guildScience2(invite, self.welcomeChannel, self.guildId)
        data = {"location":"Accept Invite Page","location_guild_id":self.guildId,"location_channel_id":self.welcomeChannel,"location_channel_type":0}
        self.headers['x-context-properties'] = self.genContextProperties(data)
        url = f"https://discord.com/api/v9/invites/{invite}"
        while True:
            try:
                r = self.client.post(url, headers=self.headers, data=json.dumps({}), timeout=10)
                break
            except Exception:
                time.sleep(self.timeout)
        del self.headers['x-context-properties']
        if r.status_code == 403:
            return False, 404
        if verification_level > 0:
            url = f"https://discord.com/api/v9/guilds/{self.guildId}/member-verification"
            while True:
                try:
                    r = self.client.get(url, headers=self.headers, timeout=10)
                    break
                except Exception:
                    time.sleep(self.timeout)
            burp0_json = r.json()
            i = 0
            print(burp0_json)
            for forms in burp0_json['form_fields']:
                del burp0_json['form_fields'][i]['description']
                burp0_json['form_fields'][i]['response'] = True
                i += 1
            while True:
                try:
                    r = self.client.put(f"https://discord.com/api/v9/guilds/{self.guildId}/requests/@me", headers=self.headers, data=json.dumps(burp0_json), timeout=10)
                    break
                except Exception:
                    time.sleep(self.timeout)
            return True, 200
        return True, 200