import requests, json, urllib.parse, string, random, time, os
from datetime import datetime, timedelta

CONFIG_FILE = "/home/user1/startups/config.json"
COOKIE_FILE = "/home/user1/startups/shushant-startups/session_data.json"
CHECK_INTERVAL = 60  
REFRESH_INTERVAL = 25  

with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

TOKEN = config["token_1"]
EMAIL = config["username"]
PASSWORD = config["password"]

def generate_session_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))

def refresh_session():
    time.sleep(random.randint(1,9))
    
    with open(COOKIE_FILE, "r") as f: data = json.load(f)
    if data['updatting'] == True :
        return
    
    data['updatting'] = True
    data['status_update'] = False
    with open(COOKIE_FILE, "w") as f: json.dump(data, f, indent=2)
    print("session is updatting")
    
    session_id = generate_session_id()
    jsonData = [
        { "Action": "Fill", "Selector": "input[type='email']", "Value": EMAIL },
        { "Action": "Fill", "Selector": "input[type='password']", "Value": PASSWORD },
        { "Action": "Click", "Selector": "button[type='submit']" },
        { "Action": "Wait", "Timeout": 5000 }
    ]
    encodedJson = urllib.parse.quote_plus(json.dumps(jsonData))
    login_url = (
        f"http://api.scrape.do/?token={TOKEN}&url={urllib.parse.quote_plus('https://www.crunchbase.com/login')}"
        f"&render=true&playWithBrowser={encodedJson}&sessionid={session_id}"
    )

    response = requests.get(login_url)
    cookies = response.headers.get("Scrape.do-Cookies", "")
    file_name = "/home/user1/startups/shushant-startups/crunchbase_logged11_in.html"
    with open(file_name, '+w') as f:f.write(response.text)
    
    data["session_id"] = session_id
    data["cookies"] = cookies
    data["last_refreshed"] = datetime.utcnow().isoformat()
    data['updatting'] = False
    data['status_update'] = True

    with open(COOKIE_FILE, "w") as f: 
        json.dump(data, f, indent=2)

    print(f"[+] Session refreshed at {data['last_refreshed']} (Session ID: {session_id})")


def needs_refresh():
    if not os.path.exists(COOKIE_FILE):
        return True
    try:
        with open(COOKIE_FILE, "r") as f:
            data = json.load(f)
        last_refreshed = data.get("last_refreshed")
        if not isinstance(last_refreshed, str):
            return True
        last_time = datetime.fromisoformat(last_refreshed)
        return datetime.utcnow() - last_time > timedelta(minutes=REFRESH_INTERVAL)
    except Exception as e:
        print(f"[!] Error parsing session file: {e}")
        return True

# # Main loop: check every 1 minute
# print("[*] Starting session refresher...")
# refresh_session()
# while True:
#     needs_refres = needs_refresh()
#     print(needs_refres)
#     if needs_refres:
#         refresh_session()
#     else:
#         print("[*] Session still valid. Next check in 60s.")
#     time.sleep(CHECK_INTERVAL)
