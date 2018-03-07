# coding=utf-8


"""
Modules Import
"""
from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from sampledata import getyaml
from src import loginOS, lldp

disable_warnings(InsecureRequestWarning)

"""
Allows to automatically rename local port based on LLDP Remote Devices Informations 
"""

data = getyaml.readyaml('data-lldp.yaml')
for ip in data['ipadd']:
    baseurl = "https://{}/rest/v4/".format(ip)
    try:
        cookie_header = loginOS.login_os(data, baseurl)
        result = lldp.lldp(baseurl, cookie_header, info="remote")
        for dev in result['lldp_remote_device_element']:
            result = lldp.lldp_renameport(baseurl, dev, cookie_header)
    except Exception as error:
        print('Ran into exception: {}. Logging out..'.format(error))
    finally:
        loginOS.logout(baseurl, cookie_header)
