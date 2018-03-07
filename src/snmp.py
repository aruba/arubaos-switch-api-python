import json
import requests


def config_snmp_hosts(baseurl, snmphosts, cookie_header):
    """
    This function configure SNMP hosts

    :param baseurl: The resource URL for the device, in String format.
    :param cookie_header: The login cookie for the session.
    :param snmphosts: snmp hosts parsed from yaml file
    :return: print success or failure of SNMP hosts creation on screen
    """
    url = baseurl + 'snmp-server/hosts'
    headers = {'cookie': cookie_header}
    response = requests.post(url, verify=False, data=json.dumps(snmphosts), headers=headers)
    print("response status is", response.status_code)
    if response.status_code == 201:
        print("SNMP Hosts configuration successful for {}".format(snmphosts['host_ip']['octets']))
    else:
        print("SNMP Hosts configuration failed")


def snmp_linktrap_enable(linktrap, baseurl, cookie_header):
    """
    This function enable snmp traps for a port enable/disable

    :param baseurl: The resource URL for the device, in String format.
    :param cookie_header: The login cookie for the session.
    :param linktrap: port data is parsed from yaml file to enable or disable port details
    :return: Prints rap enables or failure on screen
    """
    url = baseurl + 'snmp-server/traps/linktraps/' + linktrap['port_id']
    headers = {'cookie': cookie_header}
    response = requests.put(url, verify=False, data=json.dumps(linktrap), headers=headers)
    print("response status is", response.status_code)
    if response.status_code == 200:
        print("SNMP Link trap status is {} for port - {}".format((linktrap['is_enabled']), linktrap['port_id']))
    else:
        print("Update of link trap enable for port {} failed".format(linktrap['port_id']))


def get_snmp_communities(baseurl, cookie_header):
    """
    This function gets all of the SNMP Communities from the device and returns their info in JSON format

    :param baseurl: The resource URL for the device, in String format.
    :param cookie_header: The login cookie for the session.
    :return: JSON data containing all of the SNMP Communites on the switch.
    """
    url = baseurl + 'snmp-server/communities'
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()


def create_snmp_community(baseurl, cookie_header, name, community):
    """
    This function creates a new SNMP Community with the 'name' parameter

    :param baseurl: The resource URL for the device, in String format.
    :param cookie_header: The login cookie for the session.
    :param name: The SNMP Community Name to be created, 1-32 digits, in String format
    :param community: JSON passed from the get_snmp_community call
    :return: return status code of the API call
    """
    url = baseurl + 'snmp-server/communities'
    headers = {'cookie': cookie_header}
    data = {
        "access_type": community['access_type'],
        "community_name": name,
        "restricted": community['restricted']
    }
    print(data)
    response = requests.post(url, verify=False, data=json.dumps(data), headers=headers)
    if response.status_code == 201:
        print("SNMP Community Created successfully for {}".format(data['community_name']))
        return response.status_code
    else:
        print("SNMP Community Creation Failed - " + str(response))


def update_snmp_community(baseurl, cookie_header, name, access_type="UT_OPERATOR", restricted=True):
    """
    This function updates a SNMP Community with the 'name' parameter, to change the access type or restriction

    :param baseurl: The resource URL for the device, in String format.
    :param cookie_header: The login cookie for the session.
    :param name: The SNMP Community Name to be updated, in String format
    :param access_type: The updated access level of the SNMP Community.  The options are UT_OPERATOR and UT_MANAGER.
                 This is defaulted in the function to UT_OPERATOR.
    :param restricted: The type of access for community, in Boolean format.  True means the community is restricted,
                       False means the community is unrestricted.
    :return: prints SNMP update status on screen
    """
    url = baseurl + 'snmp-server/communities/' + name
    headers = {'cookie': cookie_header}
    data = {
        "access_type": access_type,
        "community_name": name,
        "restricted": restricted
    }
    response = requests.put(url, verify=False, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        print("SNMP Community Update successful for {}".format(data['community_name']))
    else:
        print("SNMP Community Update Failed - " + str(response))


def delete_snmp_community(baseurl, cookie_header, name):
    """
    This function deletes a SNMP Community by the 'name' parameter.

    :param baseurl: The resource URL for the device, in String format.
    :param cookie_header: The login cookie for the session.
    :param name: The SNMP Community Name to be deleted, in String format
    :return: Print delete operation success or failure
    """
    url = baseurl + 'snmp-server/communities/' + name
    headers = {'cookie': cookie_header}
    data = {
        "community_name": name
    }
    response = requests.delete(url, verify=False, data=json.dumps(data), headers=headers)
    if response.status_code == 204:
        print("SNMP Community Deletion for {} successful.".format(data['community_name']))
    else:
        print("SNMP Community Deletion Failed - " + str(response))
