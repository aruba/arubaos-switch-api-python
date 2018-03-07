# coding=utf-8


"""
Modules Import
"""
from sampledata import getjinja
from src import common

"""
Functions used to configure/manage VXLAN on AOS-S
"""


def vxlan_status(url, cookie):
    """
    Return VXLAN global status - "Enabled" or "Disabled"
    :param url: base url
    :param cookie: Cookie value
    :return: Return keyword "Enabled" or "Disabled"
    :Example:

    result = vxlan_status(base_url, sessionid)
    """
    get_vxlan_status = common.anycli(url, "show vxlan", cookie)
    status = common.decoded_anycli(value=get_vxlan_status)
    if "Disabled" in status:
        return "disabled"
    else:
        return "enabled"


def tunnel_status(url, cookie):
    """
    Return VXLAN tunnels status
    :param url: base url
    :param cookie: Cookie value
    :return: CLI Ouput, in UTF-8
    :example:

    result = tunnel_status(base_url, sessionid)
    """
    get_tunnel_status = common.anycli(url, "show interface tunnel type vxlan", cookie)
    status = common.decoded_anycli(value=get_tunnel_status)
    return status


def configure_vxlan(url, values, cookie):
    """
    Configure a VXLAN tunnel
    :param url: base url
    :param values: List of Informations needed for VXLAN configuration
    :param cookie: Cookie value
    :return: Request Status Code
    .. note: A configuration template in Jinja2 format needs to be used.
    :Example:

    result = configure_vxlan(base_url, values_list, sessionid)
    """
    template = getjinja.readjinja('vxlan.j2')
    conf = template.render(values=values)
    result = common.batchcli(cookie, url=url, commands=conf)
    return result


def print_vxlandeploy(value, device):
    """
    Print VXLAN deployment status
    :param value: Request Status Code
    :param device: Targeted device
    :Example:

    result = configure_vxlan(base_url, values_list, sessionid)
    print_vxlandeploy(base_url, device)
    VXLAN has been successfully deployed on device 192.168.1.10
    """
    if value == 202:
        print("VXLAN has been successfully deployed on device {}".format(device))
    else:
        print("An error occurred")
