from src import loginOS, poe, ports, snmp
from sampledata import getyaml
from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)

data = getyaml.readyaml()
for ip in data['ipadd']:
    baseurl = "https://{}/rest/v4/".format(ip)
    try:
        cookie_header = loginOS.login_os(data, baseurl)

        # --------------- Write all POE stats into Excel MonitorPOE.xlsx --------------- #
        poe.monitor_poe(baseurl, cookie_header)

        # --------------- Write all Port statistics to an Excel - PortStats.xlsx--------------- #
        ports.get_ports_stats_to_excel(baseurl, cookie_header)

        # --------------- Monitor a Port and if the TX rate increases, dynamically configure rate limit for the port  #
        port = data['ratelimitport']
        ports.monitor_port(baseurl, cookie_header, port)

        # --------------- Monitor Transceivers  --------------- #
        transceivers = ports.get_transceivers(baseurl, cookie_header)
        transceivers_serials = []
        if len(transceivers['transceiver_element']) > 0:
            for serial in transceivers['transceiver_element']:
                transceivers_serials.append(serial['serial_number'])

                # print transceivers port number, type and serial number
                for transceiver in transceivers_serials:
                    transceiver_detail = ports.get_transceiver_detail(baseurl, cookie_header, transceiver)
                    print("Transceiver on port {} is Type: {} Serial Number: {}"
                          .format(transceiver_detail['port_id'], transceiver_detail['type'],
                                  transceiver_detail['serial_number']))
                    transceiver_diag = ports.get_transceiver_diagnostics(baseurl, cookie_header, transceiver)

                    # Print the temperature and electricity usage of transceivers, if type is DOM
                    if transceiver_diag['diagnoistic_support_type'] == 'TDS_DOM':
                        print(
                            "Temperature in Celsius: {}, Voltage: {}, Tx bias(mA), Tx Power(dbm): {}, Rx Power(dbm): {}"
                            .format(transceiver_diag['dom_diagnostics']['temperature_in_degree_celsius'],
                                    transceiver_diag['dom_diagnostics']['voltage_in_volts'],
                                    transceiver_diag['dom_diagnostics']['tx_bias_in_milliampere'],
                                    transceiver_diag['dom_diagnostics']['tx_power_in_dbm'],
                                    transceiver_diag['dom_diagnostics']['rx_power_in_dbm']
                                    ))

        # --------------- Get Port id of the given client mac address --------------- #
        macaddress = data['macaddress']
        mactable = ports.get_mac_table(baseurl, cookie_header)
        for i in mactable['mac_table_entry_element']:
            if i['mac_address'] == macaddress:
                portid = i['port_id']
                print("Port ID for the mac address {} is: {}".format(macaddress, portid))
                # --------------- Enable/Disable SNMP trap for the device port depends on OUI --------------- #
                snmp.config_snmp_hosts(baseurl, data['snmphosts'], cookie_header)
                snmp.snmp_linktrap_enable(data['linkport'], baseurl, cookie_header)
    except Exception as error:
        print('Ran into exception: {}. Logging out..'.format(error))
    finally:
        loginOS.logout(baseurl, cookie_header)
