from sampledata import getyaml
from src import loginOS, ip_static_route
from requests.exceptions import ConnectTimeout
from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
disable_warnings(InsecureRequestWarning)

data = getyaml.readyaml('data_static_route.yaml')
destination = data['destination']
mask = data['mask']
gateway = data['gateway']

for x in data['ipadd']:
    baseurl = "https://{}/rest/v4/".format(x)
    try:
        # Login
        cookie_header = loginOS.login_os(data, baseurl)
    except ConnectTimeout as error:
        print('Ran into exception: {}'.format(error))
    else:
        try:
            # Configure static route
            ip_static_route.configure_static_route(baseurl, cookie_header, destination, mask, gateway)
            # Get routing table
            static_data = ip_static_route.get_ip_route(baseurl, cookie_header)
            # Print RIB to screen
            ip_static_route.print_static_route(static_data)
            # Ping static gateway and print result to screen
            ip_static_route.gateway_check(baseurl, gateway, cookie_header)
        except Exception as error:
            print('Ran into exception: {}'.format(error))
        finally:
            loginOS.logout(baseurl, cookie_header)
