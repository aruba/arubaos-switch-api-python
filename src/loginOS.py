import json
import requests



def login_os(data, url):
    username = data['user']
    password = data['password']
    params = {'userName': username, 'password': password}
    proxies = {'http': None, 'https': None}
    url_login = url + "login-sessions"
    response = requests.post(url_login, verify=False, data=json.dumps(params), proxies=proxies, timeout=3)
    if response.status_code == 201:
        print("Login to switch: {} is successful".format(url_login))
        session = response.json()
        r_cookie = session['cookie']
        return r_cookie
    else:
        print("Login to switch failed")


def logout(url, cookie):
    url_login = url + "login-sessions"
    headers = {'cookie': cookie}
    proxies = {'http': None, 'https': None}
    r = requests.delete(url_login, headers=headers, verify=False, proxies=proxies)
    if r.status_code == 204:
        print("Logged out!", r.status_code)
    else:
        print("Logout is not successful", r.status_code)
