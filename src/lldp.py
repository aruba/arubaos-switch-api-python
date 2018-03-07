# coding=utf-8


"""
Modules Import
"""
import requests
import json

"""
Functions which use LLDP APIs on AOS-Switch
"""


def lldp_status(url, cookie):
    """
    Retrieve Device's LLDP Global Status
    :param url: base url
    :param cookie: Cookie Value
    :return: LLDP Global Status JSON
    :Example:

    result = lldp_status(base_url, sessionid)
    """
    header = {'cookie': cookie}
    get_lldp_status = requests.get(url + "lldp", headers=header, verify=False, timeout=2)
    return get_lldp_status.json()


def print_lldpstatus(value):
    """
    Print LLDP Global Status
    :param value: value to display
    :return: display the LLDP Remote Devices Information
    """
    if value['admin_status'] == 'LLAS_ENABLED':
        print("\n LLDP is globally enabled")
    else:
        print("\n LLDP is globally disabled")


def lldp_local(url, cookie):
    """
    Retrieve LLDP Local Information
    :param url: base url
    :param cookie: Cookie Value
    :return: LLDP per local port information
    :Example:

    result = lldp_local(base_url, sessionid)
    """
    header = {'cookie': cookie}
    get_lldp_local = requests.get(url + "lldp/local-port", headers=header, verify=False, timeout=2)
    return get_lldp_local.json()


def lldp_remote(url, cookie):
    """
    Retrieve LLDP Remote Information
    :param url: base url
    :param cookie: Cookie Value
    :return: LLDP Remote Devices Information
    :Example:

    result = lldp_remote(base_url, sessionid)
    """
    header = {'cookie': cookie}
    get_remote = requests.get(url + "lldp/remote-device", headers=header, verify=False, timeout=2)
    return get_remote.json()


def print_lldpremote(values):
    """
    Print LLDP Remote Information
    :param values: value to display
    :return: display the LLDP Remote Devices Information
    :Example:

    result = lldp_remote(base_url, sessionid)
    for device in result:
     print_lldpremote(result)

    Device's Name : Aruba-Stack-3810M
    Device's IP : 10.105.100.6
    Device's Description : Aruba JL073A 3810M-24G-PoE+-1-slot Switch
    Device's Description :  revision KB.16.04.0008
    Device's Description :  ROM KB.16.01.0008 (/ws/swbuildm/rel_ukiah_qaoff/code/build/bom
                                              (swbuildm_rel_ukiah_qaoff_rel_ukiah))
    Device's PVID : 100
    """
    for value in values['lldp_remote_device_element']:
        if 'system_name' in value and value['system_name'] != '':
            print("\n Device's Name : {} - Connected on local port {}".format(value['system_name'],
                                                                              value['local_port']))
        else:
            print("\n Connected on local port {}".format(value['local_port']))
        if 'remote_management_address' in value:
            print("\tDevice's IP : {}".format(value['remote_management_address']['address']))
        sys_desc = value['system_description'].split(',')
        for info in sys_desc:
            print("\tDevice's Description : {}".format(info))
        print("\tDevice's PVID : {}".format(value['pvid']))


def lldp_renameport(url, device, cookie):
    """
    Rename port based on given information
    :param url: Base URL
    :param device: Device's Information List
    :param cookie: Cookie Value
    :return: Requests Status Code
    """
    header = {'cookie': cookie}
    data = {
            "id": device['local_port'],
            "name": "Remote_Device:{}_-_Remote_Port:{}".format(device['system_name'], device['port_description'])
            }
    put_port_name = requests.put(url + "ports/" + device['local_port'], data=json.dumps(data), headers=header,
                                 verify=False, timeout=2)
    if put_port_name.status_code == 200:
        print('Changing port {} with name \"{}\" is successful' .format(device['local_port'], data['name']))
    else:
        print("An error occured - Status Code : {} - Content {}".format(put_port_name.status_code,
                                                                        put_port_name.content))
    return put_port_name.status_code


def lldp(url, cookie, **kwargs):
    """
    LLDP general function
    :param url: Base URL
    :param cookie: Cookie Value
    :param kwargs:
        keyword info: Type of Info which has to be retrieve - "local", "remote" or "global" values are supported
    :return: return the sub-function result
    :Example:

    result = cli(base_url, sessionid, info="local")
    or
    result = cli(base_url, sessionid, info="remote")
    or
    result = cli(base_url, sessionid)
    """
    info = kwargs.get('info', None)
    if info is not None and info == "local":
        result = lldp_local(url, cookie)
        to_return = result
    elif info is not None and info == "remote":
        result = lldp_remote(url, cookie)
        to_return = result
    else:
        result = lldp_status(url, cookie)
        to_return = result
    return to_return
