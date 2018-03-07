import logging
import requests
from src import common
from tools import ExcelOps


def monitor_poe(baseurl, cookie_header):
    """
    Write POE details to an excel sheet - MonitorPOE.xlsx in teh same folder
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :return: Write below POE details of each port to excel MonitorPOE.xlsx if exits,
    otherwise create a new excel with same name:
    Allocated Power(w)
    POE Enabled
    POE Allocation Method
    POE Priority
    Pre-Standard Dectect Enabled
    Actual Power(w)
    MPS Absent Count
    Over Current Count
    POE Detection Status
    Port Voltage(v)
    Power ClassPower Denied Count
    Power Short Count
    """
    ports = get_ports(baseurl, cookie_header)
    poedata = [["Port ID", "Allocated Power(w)", "POE Enabled", "POE Allocation Method",
                "POE Priority", "Pre-Standard Dectect Enabled", "Actual Power(w)", "MPS Absent Count",
                "Over Current Count", "POE Detection Status", "Port Voltage(v)", "Power Class"
                                                                                 "Power Denied Count",
                "Power Short Count"]]
    excelname = "MonitorPOE.xlsx"
    sheet = "POEstats"
    for i in range(len(ports)):
        url = baseurl + 'ports/' + ports[i] + '/poe'
        headers = {'cookie': cookie_header}
        response = requests.get(url, verify=False, headers=headers)
        if response.status_code == 200:
            poeconf = response.json()

        url = baseurl + 'ports/' + ports[i] + '/poe/stats'
        headers = {'cookie': cookie_header}
        response = requests.get(url, verify=False, headers=headers)
        print("POE Statistics for port {} collected successfully".format(ports[i]))
        if response.status_code == 200:
            poestats = response.json()
            if poestats['poe_detection_status'] == 'Fault':
                print("POE dection shows Faulty for port {}".format(ports[i]))
                poe_recycle(baseurl, cookie_header, ports[i])

        '''Create Main list to write to excel'''
        poei = [poeconf['port_id'], poeconf['allocated_power_in_watts'], poeconf['is_poe_enabled'],
                poeconf['poe_allocation_method'],
                poeconf['poe_priority'], poeconf['pre_standard_detect_enabled'], poestats['actual_power_in_watts'],
                poestats['mps_absent_count'],
                poestats['over_current_count'], poestats['poe_detection_status'], poestats['port_voltage_in_volts'],
                poestats['power_class'],
                poestats['power_denied_count'], poestats['short_count']]
        poedata.append(poei)
    ExcelOps.writetoexecl(excelname, sheet, poedata)


def get_ports(baseurl, cookie_header):
    """
    Get all ports ids from the switches - works for standalone and stacked switches
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :return: Return all ports for a given standalone switch or stacked switch.
    """
    url = baseurl + 'ports'
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    ports = []
    if response.status_code == 200:
        portslist = response.json()['port_element']
        for i in (range(len(portslist))):
            portid = (portslist[i]['id'])
            ports.append(portid)
    return ports


def poe_recycle(baseurl, cookie_header, port):
    """
    Bounce power on any given port on switch
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :return: Disable and enable POE on any given port. Print the status on screen
    """
    logging.info("Starting Power recycle for Port {}".format(port))
    cmd = "configure terminal"
    common.anycli(baseurl, cmd, cookie_header)
    cmd = "interface " + port
    common.anycli(baseurl, cmd, cookie_header)
    cmd = "no power-over-ethernet"
    common.anycli(baseurl, cmd, cookie_header)
    logging.info("Power disabled for Port {}".format(port))
    cmd = "power-over-ethernet"
    common.anycli(baseurl, cmd, cookie_header)
    logging.info("Power enabled for Port {}".format(port))
