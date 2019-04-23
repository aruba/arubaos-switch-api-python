'''
Dynamic OUI feature detects OUI using LLDP.

https://wiki.wireshark.org/LinkLayerDiscoveryProtocol
Common LLDP OUIs:
00-80-c2 - IEEE 802.1
00-12-0F - IEEE 802.3
00-12-BB - TIA TR-41 Committee - Media Endpoint Discovery (LLDP-MED, ANSI/TIA-1057)
00-0E-CF - PROFIBUS International (PNO) Extension for PROFINET discovery information
30-B2-16 - Hytec Geraetebau GmbH Extensions
'''

import json
import requests
from src import common


def create_deviceprofile(baseurl, deviceprofile1, cookie_header):
    """
    Create Device Profile with a tagged vlan
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :param deviceprofile1: imported data from yaml file for device profile
    :return: Print the status of device profile creation success/failure on the screen
    """
    url = baseurl + 'device_profiles'
    headers = {'cookie': cookie_header}
    response = requests.post(url, verify=False, data=json.dumps(deviceprofile1), headers=headers)
    if response.status_code == 201:
        print("Device Profile: {} creation is successful" .format(deviceprofile1['device_profile_name']))
    else:
        print("Device Profile: {} creation is not successful" .format(deviceprofile1['device_profile_name']))

    cmd1 = "configure terminal"
    cmd2 = "device-profile name " + deviceprofile1['device_profile_name'] + " tagged-vlan " \
           + str(deviceprofile1['tagged_vlan_id'])
    common.anycli(baseurl, cmd1, cookie_header)
    common.anycli(baseurl, cmd2, cookie_header)


def create_deviceidentity(baseurl, deviceidentity, cookie_header):
    """
    Create a new Device Identity
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :param deviceidentity: imported data from yaml file for device identity creation
    :return: Print the status of device identity creation success/failure on the screen
    """
    url = baseurl + 'device_identities'
    headers = {'cookie': cookie_header}
    response = requests.post(url, verify=False, data=json.dumps(deviceidentity), headers=headers)
    if response.status_code == 201:
        print("Device Identity: {} creation is successful" .format(deviceidentity['device_name']))
    else:
        print("Device Identity: {} creation is not successful" .format(deviceidentity['device_name']))
