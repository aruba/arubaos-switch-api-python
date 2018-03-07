# coding=utf-8


"""
Modules Import
"""
from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from sampledata import getyaml
from src import loginOS, tn

disable_warnings(InsecureRequestWarning)


"""
Configure Tunneled-Node feature
"""


data = getyaml.readyaml('data-tn.yaml')
tunnel = data['tunneled_node']
tunneled_ports = data['tunneled_ports']

for ip in (data['ipadd']):
    baseurl = "https://{}/rest/v4/".format(ip)
    cookie_header = loginOS.login_os(data, baseurl)
    try:
        print("Tunneled-Node deployment")
        print("TN Mode : {}-Based".format(tunnel['mode']))
        result = tn.tn_configuration(baseurl, tunnel, ports=tunneled_ports, cookie=cookie_header)
        if result == 200:
            print("Tunneled Node has been successfully deployed.")
        else:
            print("An error occurred during TN deployment")
    except Exception as error:
        print('Ran into exception: {}. Logging out...'.format(error))
    finally:
        loginOS.logout(baseurl, cookie_header)
