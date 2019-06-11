from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from sampledata import getyaml
from src import loginOS
from src import vsf


disable_warnings(InsecureRequestWarning)

data = getyaml.readyaml('data.yaml')
for ip in (data['ipadd']):
    baseurl = "https://{}/rest/v6/".format(ip)
    try:
        cookie_header = loginOS.login_os(data, baseurl)

        # This workflow shows all the information that can be seen
        # from the "show vsf" command in CLI.
        print('\n\nVSF Global configuration: \n')
        vsf_config = vsf.get_global_config(baseurl, cookie_header)

        vsf_info = vsf.get_vsf_info(baseurl, cookie_header)

        vsf_members = vsf.get_vsf_members(baseurl, cookie_header)

        # Prints only the desired information not the json file.
        vsf.print_show_vsf(vsf_info, vsf_members, vsf_config)

    except Exception as error:
        print('Ran into exception: {}. Logging out..'.format(error))
    finally:
        loginOS.logout(baseurl, cookie_header)
