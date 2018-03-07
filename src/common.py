import requests
import json
import base64


def anycli(baseurl, cmd, cookie_header):
    """
    Send cli commands supported on ArubaOS switch via REST API.
    All configuration and execution commands in non-interactive mode are supported.
    This is not supported for : crypto, copy, process-tracking, recopy, redo, repeat, session, end, print,
    terminal, logout, menu, page, restore, update, upgrade-software, return,  setup, screen-length,
    vlan range and help commands.
    Testmode commands are not supported. All show commands are supported except show tech and show history.
    Output of show command is encoded in base64.
    :param baseurl: imported baseurl variable
    :param cookie_header: Parse cookie resulting from successful loginOS.login_os(baseurl)
    :param cmd: cli command to be executed
    :return Return base64 encoded data for show command, also return success or failure status
    :Example:

    result = cli(url=base_url, auth=s, command="show vlan")
    print_anycli(result)
    """
    url = baseurl + 'cli'
    headers = {'cookie': cookie_header}
    command = {"cmd": cmd}
    response = requests.post(url, verify=False, data=json.dumps(command), headers=headers)
    if response.status_code == 200:
        print("Executing the command '{}' is successful" .format(cmd))
        return response.json()


def print_anycli(**kwargs):
    """
    List the number of deployed scripts on remote device
    :param kwargs:
        keyword value: value to display
    :return: display the result of AnyCLI
    :Example:

    result = cli(url=base_url, auth=s, command="show vlan")
    print_anycli(result)
    """
    value = kwargs.get('value', None)
    print(base64.b64decode(value['result_base64_encoded']).decode('utf-8'))
    return base64.b64decode(value['result_base64_encoded']).decode('utf-8')


def decoded_anycli(**kwargs):
    """
    Return the decoded return from AnyCLI request - Do not print anything
    :param kwargs:
        keyword value: value to display
    :return: return the result of AnyCLI in UTF-8
    :Example:

    result = cli(url=base_url, auth=s, command="show vlan")
    decoded_anycli(result)
    """
    value = kwargs.get('value', None)
    return base64.b64decode(value['result_base64_encoded']).decode('utf-8')


def batchcli(cookie, **kwargs):
    """
    Send a set of commands to the remote device through the Batch_CLI API
    :param cookie: Cookie value
    :param kwargs:
        keyword url: base url
        keyword commands_set: set of commands which has to be applied on remote device
    :return: Batch_CLI status code
    :Example:

    result = anycli(url=base_url, auth=s, commands="show vlan")
    or
    result = anycli(url=base_url, header=aoss_header, commands="show vlan")
    """
    header = {'cookie': cookie}
    commands_set = kwargs.get('commands', None)
    encoded_data = base64.b64encode(commands_set.encode('utf-8'))
    data = {
        "cli_batch_base64_encoded": encoded_data.decode('utf-8')
    }
    post_batchcli = requests.post(kwargs["url"] + "cli_batch", data=json.dumps(data), headers=header, verify=False,
                                  timeout=2)
    return post_batchcli.status_code


def icmp_echo(baseurl, host, cookie_header):
    """
    Test IP connectivity to a given host
    :param baseurl: Imported from yaml
    :param host: IP address of destination
    :param cookie_header: Object created by loginOS.login_os()
    :return: REST call response JSON
    """
    url = baseurl + 'ping'
    headers = {'cookie': cookie_header}
    ip = {'destination': {'ip_address': {'version': 'IAV_IP_V4', 'octets': host}}}
    response = requests.post(url, headers=headers, json=ip, verify=False)
    return response.json()


def print_ping(echo_response, host):
    """
    Print a response to screen based upon icmp_response result
    :param echo_response: result of icmp_echo()
    :param host: IP address of IP destination
    :return: Print result to screen
    """
    if echo_response['result'] == 'PR_OK':
        print("IP address {} is reachable.".format(host))
    elif echo_response['result'] == 'PR_REQUEST_TIME_OUT':
        print("ERROR! IP address {} is unreachable, request timed out.".format(host))
    else:
        print("Ping failed: {}".format(echo_response['result']))


def ping(baseurl, host, cookie_header):
    """
    Combine icmp_echo and print_ping functions
    :param baseurl: Imported from yaml
    :param host: IP address of destination
    :param cookie_header: Object created by loginOS.login_os()
    :return: Prints to screen via print_ping()
    """
    echo_response = icmp_echo(baseurl, host, cookie_header)
    print_ping(echo_response, host)
