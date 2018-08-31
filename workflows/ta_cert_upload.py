# coding=utf-8


"""
Modules Import
"""
from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from sampledata import getyaml
from src import loginOS, system

disable_warnings(InsecureRequestWarning)

"""
Upload TA cert to all the switches mentioned in data.yml file.
"""

data = getyaml.readyaml('data.yaml')
for ip in data['ipadd']:
    baseurl = "https://{}/rest/v5/".format(ip)
    try:
        cookie_header = loginOS.login_os(data, baseurl)
        result = system.upload_tacert(baseurl, cookie_header, "TEST", "../sampledata/tacert.txt")
        print(result)

    except Exception as error:
        print('Ran into exception: {}. Logging out..'.format(error))
    finally:
        loginOS.logout(baseurl, cookie_header)
