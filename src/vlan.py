import json
import requests


def create_vlan(baseurl, cookie_header, vlan):
    """
    Create VLAN in switch
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :param vlan: data imported from yaml file specifying vlan details
    :return: Print status of vlan creation success/failure on screen
    """
    url = baseurl + 'vlans'
    headers = {'cookie': cookie_header}
    response = requests.post(url, verify=False, data=json.dumps(vlan), headers=headers)
    if response.status_code == 201:
        print("Vlan ID: {} & VLAN Name: {} creation is successful" .format(vlan['vlan_id'], vlan['name']))
    else:
        print("Vlan creation is not successful")


def get_vlan(baseurl, cookie_header):
    """
    Get all VLANs in switch
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :return: Return all vlans in json format
    """
    url = baseurl + 'vlans'
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()


def create_vlan_with_port(baseurl, vlanport, cookie_header):
    """
    Associate VLAN to a port
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :param vlanport: data imported from yaml file specifying vlan and port details
    :return: Print status of vlan to port association success/failure on screen
    """
    url = baseurl + 'vlans-ports'
    headers = {'cookie': cookie_header}
    response = requests.post(url, verify=False, data=json.dumps(vlanport), headers=headers)
    if response.status_code == 201:
        print("Vlan {} assignment to the port {} is successful" .format((vlanport['vlan_id']), vlanport['port_id']))
    else:
        print("Vlan assignment to the port is not successful")


def delete_vlans(baseurl, cookie_header, vlanids):
    """
    Delete a Vlan in the switch
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :param vlanids: data imported from yaml file specifying vlans to be deleted
    :return: Print status of vlan to port association success/failure on screen
    """
    url = baseurl + 'vlans/'+str(vlanids)
    headers = {'cookie': cookie_header}
    response = requests.delete(url, verify=False, headers=headers)
    if response.status_code == 204:
        print("Vlan {} deletion is successful" .format(vlanids))
    else:
        print("Vlan {} deletion is not successful" .format(vlanids))


def get_ip_addresses(baseurl, cookie_header):
    """
    This functions queryies the switch's VLAN assigned IP addresses.
    :return: Response IP address data.  Check the API schema for details.
    """

    url = baseurl + 'ipaddresses'
    headers = {'cookie': cookie_header}

    try:
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200 | response.status_code <= 226:
            return response
    except (requests.RequestException, requests.ConnectionError, requests.HTTPError) as error:
        print('\nRequests module exception: {}'.format(error.args))
