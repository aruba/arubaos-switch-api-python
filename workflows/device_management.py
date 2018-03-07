from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from sampledata import getyaml
from src import loginOS, snmp, system

disable_warnings(InsecureRequestWarning)

# Login to Switch
data = getyaml.readyaml('data-device-mgmt.yaml')

# Iterate through the devices in data-device-mgmt.yaml file to update User password and create new SNMP Communities
for device in data['devices']:
    baseurl = "https://{}/rest/v4/".format(device["ip_address"])
    cookie_header = loginOS.login_os(device, baseurl)

    try:
        userFound = False
        communityFound = False
        communities = snmp.get_snmp_communities(baseurl, cookie_header)
        print(communities['snmp_server_community_element'])
        for community in communities['snmp_server_community_element']:
            if community['community_name'] == device["past_snmp"]:
                communityFound = True
                print("Creating SNMP community string: {} in switch: {}.".format(
                    device["past_snmp"], device["ip_address"]))
                result = snmp.create_snmp_community(baseurl, cookie_header, device["new_snmp"], community)
                if result == 201:
                    snmp.delete_snmp_community(baseurl, cookie_header, device["past_snmp"])
        if not communityFound:
            print("SNMP community string: {} not found in switch: {}".format(device["past_snmp"], device["ip_address"]))
        users = system.get_device_users(baseurl, cookie_header)
        for current_user in users['device_management_user_element']:
            if current_user['name'] == device['change_user']:
                userFound = True
                print("User {} found on {}.  Updating user info".format(device['change_user'], device['ip_address']))

                resp = system.update_device_user(baseurl, cookie_header, device['change_pass'], current_user)
                new_user = device
                if resp == 200:
                    print("User update successful, Validating new password by logging in.")
                    device1 = {"user": device['change_user'], "password": device['change_pass']}
                    test_cookie = loginOS.login_os(device1, baseurl)
                    loginOS.logout(baseurl, test_cookie)

        if not userFound:
            print("User {} not found on {}.".format(device["user"], device["ip_address"]))

    except Exception as error:
        print('Ran into exception: {}. Logging out..'.format(error))

    # Logout from switch
    loginOS.logout(baseurl, cookie_header)
