from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from src import loginOS, ports
from sampledata import getyaml

disable_warnings(InsecureRequestWarning)

data = getyaml.readyaml()
for ip in (data['ipadd']):
    baseurl = "https://{}/rest/v4/".format(ip)
    try:
        cookie_header = loginOS.login_os(data, baseurl)
        # Get all mac address from switch
        mac_table = ports.get_mac_table(baseurl, cookie_header)
        print("MAC\t\tVLAN\tPORT")
        print("-----------------------------")

        for eachitem in mac_table["mac_table_entry_element"]:
            for entry, edata in eachitem.items():
                if entry == "mac_address":
                    macadd = edata
                elif entry == "vlan_id":
                    vlanid = edata
                elif entry == "port_id":
                    portnum = edata
                # else:
            print("Mac address: {mac}\t Port id:{portnum}\t Vlan ID: {vlanid}".format(mac=macadd, vlanid=vlanid, portnum=portnum), end="")
            print("")

    except Exception as error:
        print('Ran into exception: {}. Logging out..'.format(error))
    finally:
        loginOS.logout(baseurl, cookie_header)
