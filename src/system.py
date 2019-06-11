import requests
import json


def get_device_users(baseurl, cookie_header):
    """
    This function gets all of the users from the device and returns their info in JSON format

    :param baseurl: The resource URL for the device, in String format
    :param cookie_header: The login cookie for the session
    :return: JSON data containing all of the users on the switch
    """
    url = baseurl + 'management-user'
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()


def create_device_user(baseurl, cookie_header, name, password, auth_type="UT_OPERATOR", password_type="PET_PLAIN_TEXT"):
    """
    This function creates a user with the associated 'name' and 'password' parameters.  Note that the 'type' parameter
    is the Key value for the schema, and is defaulted to UT_OPERATOR.

    :param baseurl: The resource URL for the device, in String format
    :param cookie_header: The login cookie for the session
    :param name: The username to be created, 1-64 digits, in String format
    :param password: The password for the user being created, 1-64 digits, in String format.
    :param auth_type: The authority level of the user being created.  The options are UT_OPERATOR and UT_MANAGER.
    This is a key value for the schema, and is defaulted in the function to UT_OPERATOR.
    :param password_type: The password encryption type to be used.  The options are PET_PLAIN_TEXT and PET_SHA1.  The
                          default value for this function is PET_PLAIN_TEXT.
    :return: N/A
    """
    url = baseurl + 'management-user'
    headers = {'cookie': cookie_header}
    data = {
        "type": auth_type,
        "name": name,
        "password": password,
        "password_type": password_type
    }
    # print(data)
    response = requests.put(url, verify=False, data=json.dumps(data), headers=headers)
    # print("response status is", response.status_code)
    if response.status_code == 201:
        print("User Update successful for {}".format(data['name']))
    else:
        print("User Update Failed - " + str(response))


def update_device_user(baseurl, cookie_header, password, user):
    """
    This function updates a user by the 'name' parameter and updates its password.  Note that the 'type' parameter is
    the Key value for the schema, and is defaulted to UT_OPERATOR.

    :param baseurl: The resource URL for the device, in String format
    :param cookie_header: The login cookie for the session
    :param password: The new password for the user being updated, 1-64 digits, in String format.
    :param user:  The JSON containing the user data
    :return: N/A
    """
    url = baseurl + 'management-user/' + user['type']
    # print(url)
    headers = {'cookie': cookie_header}
    data = {
        "type": user['type'],
        "name": user['name'],
        "password": password,
        "password_type": user['password_type']
    }
    print(data)
    response = requests.put(url, verify=False, data=json.dumps(data), headers=headers)
    print("response status is", response.status_code)
    if response.status_code == 200:
        print("User Update successful for {}".format(data['name']))
        return response.status_code
    else:
        print("User Update Failed - " + str(response))


def upload_tacert(baseurl, cookie_header, cert_name, cert_file):
    """
    This function uploads the tacert to the switches.

    :param baseurl: The resource URL for the device, in String format
    :param cookie_header: The login cookie for the session
    :param cert_name: Name of the TA cert
    :param cert_file: Path of teh cert file
    :return: N/A
    """
    url = baseurl + 'ta_profiles'
    # print(url)
    headers = {'cookie': cookie_header}
    with open(cert_file, 'rb') as file:
        cert_base64 = base64.b64encode(file.read()).decode('utf-8')

    data = {
        "ta_name" : cert_name,
        "ta_certificate_base64_encoded_pem" : cert_base64
    }
    response = requests.post(url, verify=False, data=json.dumps(data), headers=headers)
    print("response status is", response.status_code)
    if response.status_code == 201:
        print("TA cert upload is successful")
        return response.status_code
    else:
        print("TA cert upload failed, status code:" + str(response))


def get_system_time(baseurl, cookie_header):
    """"
    This function returns the host system time configuration

    :param baseurl: The resource URL for the device, in String format
    :param cookie_header: the login cookie for the session
    :return Json data containing the system time configuration
    """
    url = baseurl + 'system/time'
    headers = {'cookie': cookie_header}
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def print_system_time_config(values):
    """
    Function to print the system time configuration
    :param values: json response from GET call containing the values to be displayed
    :return N/A
            prints to the screen the configuration in list form
    """
    print('Local UTC Offset: ' + str(values['local_utc_offset_in_seconds']))
    if values['auto_adjust_dst']:
         print('Automatically adjust DST changes: Yes')
    else:
         print('Automatically adjust DST changes: No')
    print('DST Begins on Day: ' + str(values['custom_dst_begins_rule']['day_of_month']))
    print('Of Month: ' + str(values['custom_dst_begins_rule']['month']))
    print('DST Ends on Day: ' + str(values['custom_dst_end_rule']['day_of_month']))
    print('Of Month: ' + str(values['custom_dst_end_rule']['month']))
    if values['time_servers']:
        print(values['time_servers'])
    if values['use_sntp_unicast']:
        print('Using SNTP unicast')
    else:
        print('Not using SNTP unicast')
    print('Time Server Protocol: ' + str(values['time_server_protocol']))
    print('\n\n')
