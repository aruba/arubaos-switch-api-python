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
Retrieve and display LLDP Informations for each devices. 
"""

# Login to Switch
data = getyaml.readyaml('data-tn.yaml')

for x in data['ipadd']:
    baseurl = "https://{}/rest/v4/".format(x)
    try:
        cookie_header = loginOS.login_os(data, baseurl)
        result = tn.get_tnconf(baseurl, cookie_header)
        print("\nTunneled-Node Global Configuration")
        tn.print_tnconfig(result)
        if result['is_tn_server_configured'] is True:
            result = tn.get_tnstats(baseurl, cookie_header)
            print("\nTunneled-Node Statistics\n")
            tn.print_tnstats(result)
            print("\nUsers currently connected with Tunneled-Node\n")
            result = tn.get_tn_users(baseurl, cookie_header)
            print(result)
    except Exception as error:
        print('Ran into exception: {}. Logging out..'.format(error))
    finally:
        loginOS.logout(baseurl, cookie_header)
