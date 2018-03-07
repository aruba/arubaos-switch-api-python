from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from src import loginOS, vlan, deviceidentity, ports
from sampledata import getyaml

disable_warnings(InsecureRequestWarning)


data = getyaml.readyaml()
for ip in data['ipadd']:
    baseurl = "https://{}/rest/v4/".format(ip)
    try:
        cookie_header = loginOS.login_os(data, baseurl)
        # --------------- Name the Ports --------------- #
        portname = data['port']
        print('Port Information: {}'.format(portname))
        for name in portname:
            ports.name_ports(baseurl, cookie_header, name)
        # --------------- Create Vlans tagged and untagged --------------- #
        vlandata = data['vlan']
        for vlans in vlandata:
            print("Vlan to create \n", vlans)
            vlan.create_vlan(baseurl, cookie_header, vlans)
        # --------------- Get all Vlans --------------- #
        vlans = vlan.get_vlan(baseurl, cookie_header)
        print('Vlans in the system are: \n')
        for i in range(len(vlans['vlan_element'])):
            print("Vlan ID: {} and Vlan Name: {}".format(
                vlans['vlan_element'][i]['vlan_id'], vlans['vlan_element'][i]['name']))
        # --------------- create LACP ports with trunk --------------- #
        lacpport = data['lacpport']
        for i in range(len(lacpport)):
            ports.create_lacp_port(baseurl, cookie_header, lacpport[i])
        # --------------- Get LACP ports with trunk --------------- #
        lacpports = ports.get_lacp_port(baseurl, cookie_header)
        for i in (range(len(lacpports['lacp_element']))):
            print("Port ID: {}, Trunk Group: {} ".format(lacpports['lacp_element'][i]['port_id'],
                                                         lacpports['lacp_element'][i]['trunk_group']))
        # --------------- Associate a port to a vlan (show vlan <vlanid>) --------------- #
        vlanport = data['vlanport']
        for x in range(len(vlanport)):
            vlan.create_vlan_with_port(baseurl, vlanport[x], cookie_header)
        # --------------- Create Device profile and device identity --------------- #
        devicep1 = data['deviceprofile1']
        deviceidentity.create_deviceprofile(baseurl, devicep1, cookie_header)
        devicei = data['deviceidentity']
        deviceidentity.create_deviceidentity(baseurl, devicei, cookie_header)
        # --------------- Run Cable Diagnostics Tests --------------- #
        ports.clear_cable_diagnostics(baseurl, cookie_header)
        ports.test_cable_diagnosticsrange(baseurl, cookie_header, data['portlist'])
        ports.get_cable_diagnostics(baseurl, cookie_header)
    except Exception as error:
        print('Ran into exception: {}. Logging out..'.format(error))
    finally:
        loginOS.logout(baseurl, cookie_header)
