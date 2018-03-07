from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from sampledata import getyaml
from src import loginOS, vlan

disable_warnings(InsecureRequestWarning)

data = getyaml.readyaml()
for ip in (data['ipadd']):
    baseurl = "https://{}/rest/v4/".format(ip)
    try:
        cookie_header = loginOS.login_os(data, baseurl)
        ''' Here the workflow goes!
            import required modules from the src folder and call the required functions
            You could use sampledata.yaml file to declare all your sampledata points
    
            For example below lines gets all vlans from switch and print it
        '''
        vlans = vlan.get_vlan(baseurl, cookie_header)
        print('Vlans in the system are:')
        for i in range(len(vlans['vlan_element'])):
            print("Vlan ID: {} and Vlan Name: {}".format(vlans['vlan_element'][i]['vlan_id'],
                                                         vlans['vlan_element'][i]['name']))
    except Exception as error:
        print('Ran into exception: {}. Logging out..'.format(error))
    finally:
        loginOS.logout(baseurl, cookie_header)
