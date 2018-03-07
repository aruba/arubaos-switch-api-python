# coding=utf-8


"""
Modules Import
"""
import requests
import json
from src import common

"""
Functions which use LLDP APIs on AOS-Switch
"""


def get_tnconf(url, cookie):
    """
    Retrieve Tunneled Node's Configuration
    :param url: base url
    :param cookie: Cookie value
    :return: TN Configuration JSON
    :Example:

    result = get_tnconf(base_url, sessionid)
    """
    header = {'cookie': cookie}
    get_tn_config = requests.get(url + "tunneled_node_server", headers=header, verify=False, timeout=2)
    return get_tn_config.json()


def print_tnconfig(value):
    """
    Print Tunneled-Node Configuration
    :param value: value to display
    :return: display Tunneled-Node Configuration
    :Example:

    result = tn_configuration(base_url, sessionid)
    print_tnconfig(result)

    Tunneled-Node is configured
        Mode : Per-User Tunneled-Node
        Tunneled-Node Status : Enabled
        Remote Controller : 10.14.10.50
        Backup Remote Controller : 10.14.10.51
    """
    if value['is_tn_server_configured'] is True:
        print("Tunneled-Node is configured")
        if value['mode'] == "TNSM_ROLE_BASED":
            print("\tMode : Per-User Tunneled-Node")
        elif value['mode'] == "TNSM_PORT_BASED":
            print("\tMode : Per-Port Tunneled-Node")
        else:
            print("\tMode : Not Configured")
        if value['tn_server_status'] is True:
            print("\tTunneled-Node Status : Enabled")
        else:
            print("\tTunneled-Node Status : Disabled")
        if value['controller_ip'] is not None:
            print("\tRemote Controller : {}".format(value['controller_ip']['octets']))
        if value['backup_controller_ip'] is not None:
            print("\tBackup Remote Controller : {}".format(value['backup_controller_ip']['octets']))
    else:
        print("Tunneled-Node is not configured on this device")


def tn_configuration(url, values, cookie, **kwargs):
    """
    Configure TN globally
    :param url: base url
    :param values: TN Configuration values
    :param cookie: Cookie value
    :param kwargs:
        keyword ports: Tunneled Ports in case of PPTN implementation
    :return: Status Code
    :note: In case of PUTN, neither function is called
    :Example:

    result = tn_configuration(base_url, values, sessionid, port=ports_list)
    """
    header = {'cookie': cookie}
    ports = kwargs.get('ports', None)
    if values['mode'] == "ROLE":
        mode = "TNSM_ROLE_BASED"
    elif values['mode'] == "PORT":
        mode = "TNSM_PORT_BASED"
    print(mode)
    data = {
        "is_tn_server_configured": values['server_configured'],
        "controller_ip": {"version": "IAV_IP_V4", "octets": values['controller_ip']},
        "tn_server_status": values['server_status'],
        "mode": str(mode)
    }
    print(data)
    put_tn_config = requests.put(url + "tunneled_node_server", data=json.dumps(data), headers=header,
                                 verify=False, timeout=2)

    if values['mode'] == "PORT" and ports is not None:
        print("Deploy TN configuration on Access Ports")
        result = tn_ports_config(url, ports[0]['ports_list'], cookie)
        if result == 1:
            put_tn_config = 200
        else:
            put_tn_config = 401
        return put_tn_config
    else:
        print(put_tn_config.status_code)
        return put_tn_config.status_code


def tn_ports_config(url, values, cookie):
    """
    Configure Access Ports in case of Per-Port Tunneled Node
    :param url: base url
    :param cookie: Cookie value
    :param values: TN Ports Configuration values
    :return: Status Code
    :note: Calls the create ports list and pptn_configuration functions
    :Example:

    result = tn_ports_config(base_url, ports, sessionid)
    """
    header = {'cookie': cookie}
    ports_list = create_ports_list(values)
    result = 1
    for port in ports_list:
        data = {
            "port_id": port,
            "is_tn_server_applied": True,
            "is_fallback_local_switching": True
        }
        put_tn_config = requests.put(url + "tunneled_node_server/ports/" + port, data=json.dumps(data), headers=header,
                                     verify=False, timeout=2)
        if put_tn_config.status_code != 200:
            result = 0
    return result


def create_ports_list(values):
    """
    Create the ports list for PPTN configuration
    :param values: TN Ports Configuration values
    :return: the complete ports list in good format
    :Example:

    result = create_ports_lists(values)
    """
    ports_list = values.split(',')
    for port in ports_list:
        if "-" in port:
            lists = port.split('-')
            i = int(lists[0])
            while i <= int(lists[1]):
                ports_list.append(str(i))
                i += 1
            ports_list.remove(port)
    return ports_list


def pptn_configuration(url, port, cookie):
    """
    Applies TN configuration on specified port
    :param url: base url
    :param cookie: Cookie value
    :param port: Port where TN will be activated
    :return: Port configuration Status Code
    :Example:

    result = pptn_configuration(base_url, port, sessionid)
    """
    header = {'cookie': cookie}
    data = {
        "port_id": port,
        "is_tn_server_applied": True,
        "is_fallback_local_switching": True
    }
    put_pptn_config = requests.put(url + "tunneled_node_server/ports/" + port, data=json.dumps(data), headers=header,
                                   verify=False, timeout=2)
    return put_pptn_config.status_code


def get_tnstats(url, cookie):
    """
    Retrieve Tunneled Node's agregated statistics
    :param url: base url
    :param cookie: Cookie value
    :return: TN Statisctics JSON
    :Example:

    result = get_tnstats(base_url, sessionid)
    """
    header = {'cookie': cookie}
    get_tn_stats = requests.get(url + "tunneled_node_server/ports/aggregate_statistics", headers=header, verify=False,
                                timeout=2)
    return get_tn_stats.json()


def print_tnstats(values):
    """
    Print TN Agregated Statistics
    :param values: Agregated Statisctics Values
    :Example:

    result = print_tnstats(values)
    """
    print("Tunneled-Node Server - Aggregated Statistics")
    if values['heartbeat_packets_sent'] is not None:
        print("- Heartbeat Packets Sent : {}".format(values['heartbeat_packets_sent']))
    else:
        print("- Heartbeat Packets Sent : No values to display")
    if values['heartbeat_packets_received'] is not None:
        print("- Heartbeat Packets Received : {}".format(values['heartbeat_packets_received']))
    else:
        print("- Heartbeat Packets Received : No values to display")
    if values['heartbeat_packets_invalid'] is not None:
        print("- Invalid Heartbeat Packets : {}".format(values['heartbeat_packets_invalid']))
    else:
        print("- Invalid Heartbeat Packets : No values to display")
    if values['fragmented_packets_dropped'] is not None:
        print("- Fragmented Packets received : {}".format(values['fragmented_packets_dropped']))
    else:
        print("- Fragmented Packets received : No values to display")
    if values['packets_to_non_existent_tunnel'] is not None:
        print("- Packets to Non Existent Tunnel : {}".format(values['packets_to_non_existent_tunnel']))
    else:
        print("- Packets to Non Existent Tunnel : No values to display")
    if values['mtu_violation_drop'] is not None:
        print("- MTU Violation Drop : {}".format(values['mtu_violation_drop']))
    else:
        print("- MTU Violation Drop : No values to display")


def get_tn_users(url, cookie):
    """
    Retrieve Tunneled Node's connected users
    :param url: base url
    :param cookie: Cookie value
    :return: TN users JSON
    :note: This function will display the result of the "show tunneled-node-users all"
    :Example:

    result = get_tn_users(base_url, sessionid)
    """
    get_tunnel_users = common.anycli(url, "show tunneled-node-users all", cookie)
    status = common.decoded_anycli(value=get_tunnel_users)
    return status
