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
Retrieve and display LLDP Information for each devices. 
"""

data = getyaml.readyaml('data-lldp.yaml')
for ip in data['ipadd']:
    baseurl = "https://{}/rest/v4/".format(ip)
    try:
        cookie_header = loginOS.login_os(data, baseurl)
        result = lldp.lldp(baseurl, cookie_header)
        print("\nLLDP Global Status")
        lldp.print_lldpstatus(result)
        if result['admin_status'] == 'LLAS_ENABLED':
            result = lldp.lldp_remote(baseurl, cookie_header)
            print("\nLLDP remote devices information\n")
            lldp.print_lldpremote(result)
    except Exception as error:
        print('Ran into exception: {}. Logging out..'.format(error))
    finally:
        loginOS.logout(baseurl, cookie_header)
