import requests


# Getters, functions to request data
def get_global_config(baseurl, cookie_header):
    """"
    Fetch the global configuration of the VSF stack.
    :param baseurl: imported base url
    :param cookie_header: parse cookie resulting from successful loginOS.login_os(baseurl)
    :return VSF global configuration and members' status
    """
    url = baseurl + 'stacking/vsf/global_config'
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code


def get_vsf_info(baseurl, cookie_header):
    """"
    Fetch the VSF information.
    :param baseurl: imported base url variable
    :param cookie_header: parse cookie resulting from successful loginOS.login_os(baseurl)
    :return VSF stack information
    """
    url = baseurl + 'stacking/vsf/info'
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code


def get_vsf_members(baseurl, cookie_header):
    """"
    Fetch the VSF members' information.
    :param baseurl: imported base url variable
    :param cookie_header: parse cookie resulting from successful loginOS.login_os(baseurl)
    :return VSF members' information
    """
    url = baseurl + 'stacking/vsf/members'
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code


def get_system_info(baseurl, cookie_header):
    """"
    Fetch the VSF system information.
    :param baseurl: imported base url variable
    :param cookie_header: parse cookie resulting from successful loginOS.login_os(baseurl)
    :return List of VSF member information
    """
    url = baseurl + 'stacking/vsf/members/system_info'
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code


def get_members_links_ports(baseurl, cookie_header):
    """"
    Fetch the VSF links and ports information.
    :param baseurl: imported base url variable
    :param cookie_header: parse cookie resulting from successful loginOS.login_os(baseurl)
    :return VSF links and ports information
    """
    url = baseurl + 'stacking/vsf/members_links_ports'
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code


def print_show_vsf(values1, values2, values3):
    """"
    Function to Print the Information of the specific Stack Members
    :param values1: contains the json from get_vsf_info call
    :param values2: contains the json from get_vsf_members call
    :param values3: contains the json from get_global_config call
    :return: none
             prints to the screen a similar output to that of cli command show vsf
    """
    print('VSF Domain ID    :    %13d' % (values1['domain_id']))
    print('MAC Address      :    %10s' % (values1['mac_address']['octets']))
    print('VSF Topology     :    %13s' % (values1['topology']))
    print('VSF Status       :    %13s' % (values1['status']))
    print('Uptime           :   %d d %2d h %2d m' % (values1['uptime']['days'],
                                                     values1['uptime']['hours'],
                                                     values1['uptime']['minutes']))
    if values3['is_oobm_mad_enabled']:
        print('VSF MAD          : OOBM MAD enabled')
    elif values3['is_lldp_mad_enabled']:
        print('VSF MAD          : LLDP MAD enabled')
    else:
        print('VSF MAD          :  MAD not enabled')
    print('VSF Port Speed   :    %13s' % (values1['port_speed']))
    print('Software Version :    %13s' % (values1['software_version']))
    print('\nMember ')
    print('ID\tMAC Address\t\tModel\t\t\t\tPriority\tStatus')
    print('----------------------------------------------------------------')
    for member in range(len(values2['vsf_member_element'])):
        print('%d %3s %5s %4d    %5s' % (values2['vsf_member_element'][member]['member_id'],
                                         values2['vsf_member_element'][member]['mac_address']['octets'],
                                         values2['vsf_member_element'][member]['model'],
                                         values2['vsf_member_element'][member]['priority'],
                                         values2['vsf_member_element'][member]['status']), end='\n\n')


def get_member_config(baseurl, cookie_header):
    """"
    Fetch the VSF individual member configuration.
    :param baseurl: imported base url variable
    :param cookie_header: parse cookie resulting from successful loginOS.login_os(baseurl)
    :return: specified VSF member information
    """
    member_id = int(input('\nEnter Member ID: '))
    if member_id <= 0:
        print('Member IDs are positive integers, please check your ID')
        exit(1)
    url = baseurl + 'stacking/vsf/members/%i' % member_id
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code


def get_link_info(baseurl, cookie_header, member_id):
    """
    Fetch the information on the links matching the link ID
    :param baseurl: imported base url variable
    :param cookie_header: parse cookie resulting from successful loginOS.login_os(baseurl)
    :param member_id: data imported from yaml file specifying the member ID
    :return: json with the list of VSF links matching the link ID
    """
    url = baseurl + 'stacking/vsf/members/{}/links'.format(member_id)
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code


def get_member_link_info(baseurl, cookie_header, member_id, link_id):
    """
    Fetch the information on the link of the matching member ID and link ID
    :param baseurl: imported base url variable
    :param cookie_header: parse cookie resulting from successful loginOS.login_os(baseurl)
    :param member_id: data imported from yaml file specifying the member ID
    :param link_id: data imported from yaml file specifying the link ID
    :return: json detailing the link configuration matching the set link and member ID
    """
    url = baseurl + 'stacking/vsf/members/{}/links/{}'.format(member_id, link_id)
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code


def get_vsf_ports(baseurl, cookie_header, member_id, link_id):
    """
    Fetch the information on the link of the matching member ID and link ID
    :param baseurl: imported base url variable
    :param cookie_header: parse cookie resulting from successful loginOS.login_os(baseurl)
    :param member_id: data imported from yaml file specifying the member ID
    :param link_id: data imported from yaml file specifying the link ID
    :return: json detailing the Port configuration matching the set link and member ID
    """
    url = baseurl + 'stacking/vsf/members/{}/links/{}/ports'.format(member_id, link_id)
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code


def get_member_system_info(baseurl, cookie_header, member_id):
    """
    Fetch the specified vsf member information
    :param baseurl: imported base url variable
    :param cookie_header: parse cookie resulting from successful loginOS.login_os(baseurl)
    :param member_id: data imported from yaml file specifying the member ID
    :return: json detailing the information matching the set member ID
    """
    url = baseurl + 'stacking/vsf/members/system_info/{}'.format(member_id)
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code
