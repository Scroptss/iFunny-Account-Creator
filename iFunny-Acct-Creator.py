import json
import requests
import time
from datetime import datetime
from termcolor import colored
import asyncio
import webbrowser
from secrets import token_hex
from hashlib import sha1
from base64 import b64encode

# Email base (Before the @whatever.com)
emailbase = ''

# Password for the accounts
password = '' 

# Base username for the accounts
nickbase = ''

host = "https://api.ifunny.mobi"


def load_json_file(index = 0):

    with open("accounts.json","r") as file:
        data = json.load(file)


    if not data:
        data["index"] = 0
        data["accounts"] = []
    
    return data


def save_json_file(data):

    with open("accounts.json","w") as file:
        json.dump(data,file,indent=1)
    
    return
    

# Getting an existing basic auth token, or creating a basic auth token if one doesnt exist
def get_basic_token(index):    
    
    data = load_json_file(index)

    try:
        if data["index"] == index:
            return data["accounts"][index]["basic"]
    
    except:
        client_id = "JuiUH&3822"
        client_secret = "HuUIC(ZQ918lkl*7"
        device_id = token_hex(32)
        hashed = sha1(f"{device_id}:{client_id}:{client_secret}".encode('utf-8')).hexdigest()
        basic = b64encode(bytes(f"{f'{device_id}_{client_id}'}:{hashed}", 'utf-8')).decode()
        return basic
    

def cprint(*args, end_each=" ", end_all=""):

	dt = str(datetime.fromtimestamp(int(time.time())))
	print(colored(dt, "white"), end=end_each)
	for i in args:
		print(colored(str(i[0]), i[1].lower()), end=end_each)
	print(end_all)


async def prime_basic(basic):

    header = {'Host': 'api.ifunny.mobi','Accept': 'video/mp4, image/jpeg','Applicationstate': '1','Accept-Encoding': 'gzip, deflate','Ifunny-Project-Id': 'iFunny','User-Agent': 'iFunny/7.14.2(22213) iphone/14.0.1 (Apple; iPhone8,4)','Accept-Language': 'en-US;q=1','Authorization': 'Basic '+ basic,}
    requests.get(host+"/v4/counters",headers=header)
    cprint(("Priming your basic auth token...","green"))
    time.sleep(3)
    return


async def resolve_errors(req, basic = None):

    if req["error"] == "captcha_required":
        cprint(("Captcha required, Solve the captcha that appears, then press Enter in the terminal","red"))
        webbrowser.open_new(req["data"]["captcha_url"])
        input()
        return
     
    if req["error"] == "invalid_email":
        cprint(("Something went wrong. Try again?","red"))
        return
     
    if req["error"] == "unsupported_grant_type":
        cprint(("Something went wrong. Try again?","red"))
        return
     
    if req["error"] == "too_many_user_auths":
        cprint(("Please wait about 10 minutes for iFunny's dumb user auth ratelimit, and run this again.","red"))
        return
     
    if req["error"] == "invalid_grant":
        cprint(("Invalid characters in the Email or Password, or you have created too many accounts from this IP address (VPN or Try again in ~10 mins)'","red"))
        await asyncio.sleep(5)
        return True
     
    if req["error"] == "forbidden":
        await prime_basic(basic)
        return
    


async def login_and_save_info(email, password, basic, index):

    while True:

        loginHeader = {'Host': 'api.ifunny.mobi','Applicationstate': '1','Accept': 'video/mp4, image/jpeg','Content-Type': 'application/x-www-form-urlencoded','Authorization': 'Basic '+ basic,'Content-Length':'77','Ifunny-Project-Id': 'iFunny','User-Agent': 'iFunny/7.19.3(22399) iphone/15.1 (Apple; iPhone11,8)','Accept-Language': 'en-US;q=1','Accept-Encoding': 'gzip, deflate'}
        paramz = {'grant_type':'password','username': email,'password': password}
        
        req = requests.post(host+"/v4/oauth2/token",headers=loginHeader,data=paramz).json()

        if "error" in req:
            await resolve_errors(req, basic)   
            continue
        
        await asyncio.sleep(2)
        data = load_json_file(index)
        data["index"] = index + 1
        data["accounts"].append({"email":email,"username":f"{nickbase}{index}","password":password,"bearer":req["access_token"],"basic":basic})
        save_json_file(data)
        cprint(("Logged in successfully!","green"))
        break
    return


# Where the magic happens :)
async def main_loop():
    
    data = load_json_file()
    index = int(data['index'])

    # Main login loop that tries logging in.
    while True:
        email = emailbase + f"{index}@hotmail.com"
        nick = nickbase + str(index)
        basic = get_basic_token(index)
        await prime_basic(basic)
        url = host + "/v4/users"
        paramz = {'reg_type':'pwd', 'email': email, 'password': password, 'limited':'false', 'nick':nick, 'accepted_mailing':'0'}
        header = {'Host': 'api.ifunny.mobi', 'Accept': 'video/mp4, image/jpeg', 'Applicationstate': '1', 'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Basic '+ basic, 'Content-Length': '112', 'Ifunny-Project-Id': 'iFunny', 'User-Agent': 'iFunny/7.14.2(22213) iphone/14.0.1 (Apple; iPhone8,4)', 'Accept-Language': 'en-US;q=1', 'Accept-Encoding': 'gzip, deflate',}

        while True:

            cprint(("Logging In...","green"))
            req = requests.post(url,headers=header,data=paramz).json()

            # Checking for any errors in the login response. Most likely to get a captcha error when creating each account for the first time.
            if req.get("error"):
                await resolve_errors(req, basic)

            r = requests.post(url,headers=header,data=paramz).json()
            await asyncio.sleep(2)
            await login_and_save_info(email,password,basic,index)
            index += 1
            break


if __name__ == "__main__":
    asyncio.run(main_loop())
