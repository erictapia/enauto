import requests

device = {
    'host': 'sandbox-iosxe-latest-1.cisco.com',
    'username': 'developer',
    'password': 'C1sco12345',
    'port': '443'
}

# Globals
BASE_URL = f"https://{device['host']}:{device['port']}/restconf/data"
AUTH = device['username'], device['password']
HEADERS = {
    'Accept': 'application/yang-data+json',
    'Content-Type': 'application/yang-data+json'
}

def get_url(base_url, module, container, resource=None):
    # Returns the RESTCONF URL
    return f'{base_url}/{module}:{container}/{resource}'

def get_shipintbr_cli(interfaces):
    # Returns a string representation of a cli sh ip int br
    cli_mimic_output = "{:<24}{:<16}{:<22}{:<9}\n".format(
        'Interfaces',
        'IP-Address',
        'Status',
        'Protocol'
    )

    for key in interfaces.keys():
        try:
            cli_mimic_output += "{:<24}{:<16}{:<22}{:<9}\n".format(
                interfaces[key]['name'],
                interfaces[key]['ip'],
                interfaces[key]['admin-status'],
                interfaces[key]['oper-status']
            )
        except:
            continue

    return cli_mimic_output


# Disabling warnings due to not verifying certification.  IOS-XE sandbox uses
# a self-signed certification so not verifying removes warning messages.
requests.packages.urllib3.disable_warnings()


# ============================================================================
# Using IETF's YANG data model to simulate a "show ip int br"
#
# Requires two requests:
# - 1st will get the interface name, and statuses
# - 2nd will get the ip
# ============================================================================

# 1st request
#
# ietf-interfaces:interfaces-state/interface
#
# Sample return data
# {
#   "ietf-interfaces:interface": [
#     {
#       "name": "GigabitEthernet1",
#       "type": "iana-if-type:ethernetCsmacd",
#       "admin-status": "up",
#       "oper-status": "up",
#       ... OMMITTED

url = get_url(BASE_URL, 'ietf-interfaces', 'interfaces-state', 'interface')

print()
print(f'HTTP URL: {url}')

response = requests.get(url, auth=AUTH, headers=HEADERS, verify=False)

print(f'Response code: {response.status_code}')

interfaces = response.json()['ietf-interfaces:interface']

# Dictionary to store each interface config or state data
interface_dict = {}

for interface in interfaces:

    interface_dict[interface['name']] = {
                                            'name': interface['name'],
                                            'admin-status': interface['admin-status'],
                                            'oper-status': interface['oper-status'] 
                                        }


# 2nd request
#
# ietf-interfaces:interfaces/interface
#
# Sample return data
# {
#   "ietf-interfaces:interface": [
#     {
#       "name": "GigabitEthernet1",
#       ... OMITTED
#       "ietf-ip:ipv4": {
#         "address": [
#           {
#              "ip": "10.10.20.48",
#              ... OMMITTED

url = get_url(BASE_URL, 'ietf-interfaces', 'interfaces', 'interface')

print()
print(f'HTTP URL: {url}')

response = requests.get(url, auth=AUTH, headers=HEADERS, verify=False)

print(f'Response code: {response.status_code}')
print()

interfaces = response.json()['ietf-interfaces:interface']

for interface in interfaces:
    try:
        interface_dict[interface['name']]['ip'] = interface['ietf-ip:ipv4']['address'][0]['ip']
    except:
        # Not all interfaces have an address, setting as unassigned
        if not 'address' in interface['ietf-ip:ipv4'].keys():
            interface_dict[interface['name']]['ip'] = 'unassigned'
        continue

print("Data from both request will be used for show ip interface brief")
print()
print(get_shipintbr_cli(interface_dict))



# ============================================================================
#  Using Cisco's native YANG data model to simulate a "sh ip int br"
#  Requires 1 request
# ============================================================================

# Request
#
# Cisco-IOS-XE-interfaces-oper:interfaces/interface
#
# Sample return data
#
# {
#   "Cisco-IOS-XE-interfaces-oper:interface": [
#     {
#       "name": "GigabitEthernet1",
#       "interface-type": "iana-iftype-ethernet-csmacd",
#       "admin-status": "if-state-up",
#       "oper-status": "if-oper-state-ready",
#       "last-change": "2020-12-06T16:47:35.000395+00:00",
# ... OMITTED

url = get_url(BASE_URL, 'Cisco-IOS-XE-interfaces-oper', 'interfaces', 'interface')

print(f'HTTP URL: {url}')

response = requests.get(url, auth=AUTH, headers=HEADERS, verify=False)

print(f'Response code: {response.status_code}')

interfaces = response.json()['Cisco-IOS-XE-interfaces-oper:interface']

interface_dict = {}

for interface in interfaces:
    try:
        interface_dict[interface['name']] = {
                                     'name': interface['name'],
                                     'ip': interface['ipv4'],
                                     'admin-status': interface['admin-status'],
                                     'oper-status': interface['oper-status']
                                 }
    except:
        # Not all interfaces have an address, setting to unassigned
        if not 'ipv4' in interface.keys():

            interface_dict[interface['name']] = {
                                         'name': interface['name'],
                                         'ip': 'unassigned',
                                         'admin-status': interface['admin-status'],
                                         'oper-status': interface['oper-status']
                                     }

        continue

print()
print("Data from both request will be used for show ip interface brief")
print()
print(get_shipintbr_cli(interface_dict))


# ===========================================================================
#  Using OpenConfig's YANG data model to simulate a "sh ip int br"
# ============================================================================

# Requires 1 request
#
# openconfig-interfaces:interfaces/interface
#
# Sample return data
# {
#   "openconfig-interfaces:interface": [
#     {
#       "name": "GigabitEthernet1",
#       "config": {
#         "name": "GigabitEthernet1",
#         ... OMITTED
#       },
#       "state": {
#         "name": "GigabitEthernet1",
#         ... OMITTED
#         "admin-status": "UP",
#         "oper-status": "UP",
#         ... OMITTED
#       },
#       "subinterfaces": {
#         "subinterface": [
#           {
#             ...OMITTED
#             "openconfig-if-ip:ipv4": {
#               "addresses": {
#                 "address": [
#                   {
#                     "ip": "10.10.20.48",
# ... OMITTED

url = get_url(BASE_URL, 'openconfig-interfaces', 'interfaces', 'interface')

print(f'HTTP URL: {url}')

response = requests.get(url, auth=AUTH, headers=HEADERS, verify=False)

print(f'Response code: {response.status_code}')

interfaces = response.json()['openconfig-interfaces:interface']

interface_dict = {}

for interface in interfaces:
    try:
        interface_dict[interface['name']] = {
                                                'name': interface['name'],
                                                'ip': interface['subinterfaces']['subinterface'][0]['openconfig-if-ip:ipv4']['addresses']['address'][0]['ip'],
                                                'admin-status': interface['state']['admin-status'],
                                                'oper-status': interface['state']['oper-status']
                                            }
    except:
        # Not all IP have an address, setting to unassigned
        interface_dict[interface['name']] = {
                                                'name': interface['name'],
                                                'ip': 'unassigned',
                                                'admin-status': interface['state']['admin-status'],
                                                'oper-status': interface['state']['oper-status']
                                            }
        continue

print()
print("Data from both request will be used for show ip interface brief")
print()
print(get_shipintbr_cli(interface_dict))
