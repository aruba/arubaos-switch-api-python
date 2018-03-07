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
