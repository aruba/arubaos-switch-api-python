import requests
import json
import pprint
import xlsxwriter
from src import common


def name_ports(baseurl, cookie_header, portname):
    """
    Change port names to a given value
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :param portname: data imported from yaml file
    :return: Print status of port name update success/failure on screen
    """
    url = baseurl + 'ports/' + portname['id']
    headers = {'cookie': cookie_header}
    response = requests.put(url, verify=False, data=json.dumps(portname), headers=headers)
    if response.status_code == 200:
        print('Changing port {} with name {} is successful'.format(portname['id'], portname['name']))


def create_lacp_port(baseurl, cookie_header, lacpport):
    """
    Create LACP ports
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :param lacpport: data imported from yaml file specified which port associated with which trunk profile
    :return: Print status of lacp port update success/failure on screen
    """
    url = baseurl + 'lacp/port'
    headers = {'cookie': cookie_header}
    response = requests.post(url, verify=False, data=json.dumps(lacpport), headers=headers)
    if response.status_code == 201:
        print("LACP port {} association to Trunk profile {} is Successful".format((lacpport['port_id']),
                                                                                  lacpport['trunk_group']))
    else:
        print("LACP port Association to Trunk is not Successful, status code: {}".format(response.status_code))


def get_lacp_port(baseurl, cookie_header):
    """
    Get LACP ports on switch
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :return: retun all LACP ports configured on the switch
    """
    url = baseurl + 'lacp/port'
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()


def get_cable_diagnostics(baseurl, cookie_header):
    """
    Get Cable diagnostics results from the switch
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :return: return cable diagnostics results for each ports in the switch
    """
    url = baseurl + 'cable_diagnostics/status'
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        pprint.pprint(response.json())


def test_cable_diagnosticsrange(baseurl, cookie_header, portlist):
    """
    Execute cable diagnostics tests for a given list of ports
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :param portlist: imported data from yaml specifying list of ports where cable diagnostics tests needs to run
    :return: Print execution of cable diagnostics tests on given port(s) successful or not on screen
    """
    for i in range(len(portlist)):
        port = {}
        url = baseurl + 'cable_diagnostics/port'
        headers = {'cookie': cookie_header}
        port['port_id'] = portlist[i]
        response = requests.post(url, verify=False, data=json.dumps(port), headers=headers)
        if response.status_code == 204:
            print("Cable Diagnostics Test for port {} initiated".format(portlist[i]))
        else:
            print("Cable Diagnostics test didn't start")


def clear_cable_diagnostics(baseurl, cookie_header):
    """
    Clear previous cable diagnostics test results on the switch
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :return: Print execution status of resetting cable diagnostics tests on screen
    """
    url = baseurl + 'cable_diagnostics/clear'
    headers = {'cookie': cookie_header}
    response = requests.post(url, verify=False, data=json.dumps({}), headers=headers)
    print("Clear cable Diagnostics Status code", response.status_code)
    if response.status_code == 204:
        print("Cable Diagnostics Test is cleared")
    else:
        print("Clear Cable Diagnostics test didn't go through")


def get_ports_stats_to_excel(baseurl, cookie_header):
    """
    Write port statistics to an excel sheet - PortStats.xlsx in the same folder
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :return: Write below port statistics of each port to excel  PortStats.xlsx if exits,
     otherwise create a new excel with same name:
    Total Bytes
    Total Packets
    Tx Drops
    Rx Error
    """
    workbook = xlsxwriter.Workbook('PortStats.xlsx')
    worksheet = workbook.add_worksheet('Port Statistics')
    url = baseurl + 'port-statistics'
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        row = 0
        column = 0
        heading = ['Port ID', 'Total Bytes', 'Total Packets', 'Tx Drops', 'Rx Error']
        for i in range(len(heading)):
            worksheet.write(row, column + i, heading[i])
        row = 1
        column = 0
        portstats = response.json()['port_statistics_element']
        for i in range(len(portstats)):
            stats = [portstats[i]['id'],
                     (portstats[i]['bytes_rx'] + portstats[i]['bytes_tx']),
                     (portstats[i]['packets_rx'] + portstats[i]['packets_tx']),
                     portstats[i]['error_tx'],
                     portstats[i]['error_rx']
                     ]

            print(stats)
            for x in range(len(stats)):
                worksheet.write(row, column, stats[x])
                column += 1
            row = row + 1
            column = 0


def conf_rate_limit(baseurl, cookie_header, ratelimitport):
    """
    Configure rate-limit to the port
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :param ratelimitport: imported from yaml file for the port id
    """
    cmd1 = "configure terminal"
    cmd2 = "interface " + ratelimitport["port_id"]
    cmd3 = "rate-limit all in percent 1"
    cmd4 = "rate-limit all out percent 1"
    common.anycli(baseurl, cmd1, cookie_header)
    common.anycli(baseurl, cmd2, cookie_header)
    common.anycli(baseurl, cmd3, cookie_header)
    common.anycli(baseurl, cmd4, cookie_header)


def monitor_port(baseurl, cookie_header, port):
    """
    Monitor a specific port for its statistics. If the rate goes above 2000 rate limit gets applied
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :return Prints on screen when port reaches a threshold .
    conf_rate_limit function is called to configure rate limit the port.
    """
    url = baseurl + 'port-statistics/' + port['port_id']
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        txpkts = response.json()['packets_tx']
        print("Tx packets: {}".format(txpkts))
        if txpkts > 2000:
            print("Configuring rate limit on port {} as the TX rate gone above the threshold".format(port['port_id']))
            conf_rate_limit(baseurl, cookie_header, port)


def get_mac_table(baseurl, cookie_header):
    """
    Get all users in the switch
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :return Returns all users in the switch - equivalent to 'show mac-address' in switch
    """
    url = baseurl + 'mac-table'
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()


def port_update(baseurl, cookie_header, port):
    """
    Configure a port admin status to go UP or Down
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :param port: imported data from yaml file to update a port admin status
    :return Prints the status of port status in case of success update
    """
    url = baseurl + 'ports/' + port['id']
    headers = {'cookie': cookie_header}
    response = requests.put(url, verify=False, data=json.dumps(port), headers=headers)
    if response.status_code == 200:
        print("Port {} UP status updated as {}".format(port['id'], port['is_port_up']))


def get_transceivers(baseurl, cookie_header):
    """
    Get all transceivers in the switch
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :return return all transceivers information in json format
    """
    url = baseurl + 'transceivers'
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()


def get_transceiver_detail(baseurl, cookie_header, transceiver):
    """
    Get details of a given transceivers in the switch
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :param transceiver: data parsed to specify a transceiver in switch
    :return return transceiver's detailed information in json format
    """
    url = baseurl + 'transceivers/' + transceiver
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()


def get_transceiver_diagnostics(baseurl, cookie_header, transceiver):
    """
    Get the diagnostics of a given transceivers in the switch
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :param transceiver: data parsed to specify a transceiver in switch
    :return return transceiver's diagnostics information in json format
    """
    url = baseurl + 'transceivers/' + transceiver + '/diagnostics'
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()
