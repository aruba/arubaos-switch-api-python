"""
Module to GET and configure IP static routes.
"""

import requests
import json
from src import common


def get_ip_route(baseurl, cookie_header):
    """
    Get ip static route data
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :return: ip-route REST call response data
    """
    url = baseurl + 'ip-route'
    headers = {'cookie': cookie_header}
    rib = requests.get(url, verify=False, headers=headers)
    if rib.status_code == 200:
        return rib
    else:
        print("Get IP Route failed")


def print_static_route(rib):
    """
    Print IP static route data to screen
    :param rib: Data returned from get_static_route()
    :return: Print data to screen
    """
    print("Static Routes:")
    print("{0:20} {1:20} {2:20} {3:22} {4}".format("Destination", "Mask", "Gateway", "Distance/Metric", "ID"))
    for x in rib.json()['ip_route_element']:
        c0 = x['destination']['octets']
        c1 = x['mask']['octets']
        c2 = x['gateway']['octets']
        c3 = x['distance']
        c4 = x['metric']
        c5 = x['id']
        print("{0:20} {1:20} {2:20} {3}/{4:<20} {5}".format(c0, c1, c2, c3, c4, c5))


def configure_static_route(baseurl, cookie_header, destination, mask, gateway, mode='IRM_GATEWAY'):
    """
    Configure an IP static route.
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :param destination: Destination IP subnet. String.
    :param mask: IP subnet mask. String
    :param gateway: Next-hop IP address. String.
    :param mode: Static route mode, default to 'IRM_GATEWAY'. String.
    :return: POST call status code and print result to screen.
    """
    url = baseurl + 'ip-route'
    headers = {'cookie': cookie_header}
    static_route = {
        'destination': {'octets': destination, 'version': 'IAV_IP_V4'},
        'mask': {'octets': mask, 'version': 'IAV_IP_V4'},
        'gateway': {'octets': gateway, 'version': 'IAV_IP_V4'},
        'ip_route_mode': mode}
    conf_static = requests.post(url, verify=False, data=json.dumps(static_route), headers=headers)
    if conf_static.status_code == 201:
        print("Static route configuration OK - Code: {}".format(conf_static.status_code))
    else:
        print("Static route config ERROR - Code: {}".format(conf_static.status_code))


def print_gateway(echo_response, gateway):
    """
    Print a response to screen based upon icmp_response result to the static route next-hop
    :param echo_response: result of icmp_echo()
    :param gateway: IP address of IP destination gateway
    :return: Print result to screen
    """
    if echo_response['result'] == 'PR_OK':
        print("Static Next-Hop Gateway {} is reachable.".format(gateway))
    elif echo_response['result'] == 'PR_REQUEST_TIME_OUT':
        print("Static Next-Hop Gateway {} is unreachable, request timed out.".format(gateway))
    else:
        print("Ping failed: {}".format(echo_response['result']))


def gateway_check(baseurl, host, cookie_header):
    echo_response = common.icmp_echo(baseurl, host, cookie_header)
    print_gateway(echo_response, host)
