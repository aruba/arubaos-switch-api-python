from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from src import loginOS, vlan, common
from sampledata import getyaml

disable_warnings(InsecureRequestWarning)


data = getyaml.readyaml()
for ip in data['ipadd']:
    baseurl = "https://{}/rest/v4/".format(ip)
    vlandata = data['vlan']
    try:
        cookie_header = loginOS.login_os(data, baseurl)
        # --------------- Clear Port Names --------------- #
        for i in range(len(data['port'])):
            cmd = "interface " + data['port'][i]['id']
            common.anycli(baseurl, cmd, cookie_header)
            cmd = "no name "
            common.anycli(baseurl, cmd, cookie_header)
        # --------------- Delete trunks  --------------- #
        for i in range(len(data['lacpport'])):
            cmd = "configure terminal"
            print(cmd)
            common.anycli(baseurl, cmd, cookie_header)
            cmd = "no trunk " + data['lacpport'][i]['port_id']
            print(cmd)
            common.anycli(baseurl, cmd, cookie_header)
        # --------------- Delete Device profile and identity  --------------- #
        cmd = "no device-profile device-type " + data['deviceprofile1']['device_profile_name']
        common.anycli(baseurl, cmd, cookie_header)
        cmd = "no device-profile name " + data['deviceprofile1']['device_profile_name']
        common.anycli(baseurl, cmd, cookie_header)
        cmd = "no device-identity name " + data['deviceidentity']['device_name']
        common.anycli(baseurl, cmd, cookie_header)
        # --------------- Delete trunks  --------------- #
        for vlans in vlandata:
            vlan.delete_vlans(baseurl, cookie_header, vlans['vlan_id'])
        # --------------- Reset ratelimits on interface  --------------- #
        cmd = "interface 1/2"
        common.anycli(baseurl, cmd, cookie_header)
        cmd = "no rate-limit all in"
        common.anycli(baseurl, cmd, cookie_header)
        cmd = "no rate-limit all out"
        common.anycli(baseurl, cmd, cookie_header)
    except Exception as error:
        print('Ran into exception: {}. Logging out..'.format(error))
    finally:
        loginOS.logout(baseurl, cookie_header)
