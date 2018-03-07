from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from sampledata import getyaml
from src import loginOS, vxlan

disable_warnings(InsecureRequestWarning)


data = getyaml.readyaml('data-vxlan.yaml')
vxlan_data = data['vxlan']
for ip in (data['ipadd']):
    baseurl = "https://{}/rest/v4/".format(ip)
    try:
        cookie_header = loginOS.login_os(data, baseurl)
        for x in vxlan_data:
            result = vxlan.configure_vxlan(baseurl, x, cookie=cookie_header)
            vxlan.print_vxlandeploy(result, ip)
    except Exception as error:
        print('Ran into exception: {}. Logging out...'.format(error))
    finally:
        loginOS.logout(baseurl, cookie_header)
