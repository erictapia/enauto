import requests

device = {
    'host': 'ios-xe-mgmt.cisco.com',
    'username': 'developer',
    'password': 'C1sco12345',
    'port': '9443'
}


# Globals
BASE_URL = f"https://{['device[host']}:{device['port']}/restconf/data"


def url(base_url, module, container, resource=None):
    # Returns the RESTCONF URL
    return f'{BASE_URL}{module}:{container}/{resource}'


# Using IETF's YANG data model
# ============================================================================
# Interface Status: ietf-interfaces:interfaces-state
# - Interface = interface['name']
# - Status = interface['admin-status']
# - Protocol = interface['oper-status']
#
# Sample return data
# {
#   "ietf-interfaces:interface": [
#     {
#       "name": "GigabitEthernet1",
#       "type": "iana-if-type:ethernetCsmacd",
#       "admin-status": "up",
#       "oper-status": "up",
# ... OMMITTED

url = (BASE_URL, 'ietf-interfaces', 'interfaces-state', 'interface')





# Interface IP Address: ietf-interfaces:interfaces
# - Interface = interface['name']
# - IP-Address = interface['ietf-ip:ipv4']['address']['ip']
#     There can be more than one IP Address TODO
#
# Sample return data
# {
#   "ietf-interfaces:interface": [
#     {
#       "name": "GigabitEthernet1",
#       "description": "MANAGEMENT INTERFACE - DON'T TOUCH ME",
#       "type": "iana-if-type:ethernetCsmacd",
#       "enabled": true,
#       "ietf-ip:ipv4": {
#         "address": [
#           {
#             "ip": "10.10.20.48",
#             "netmask": "255.255.255.0"
#           }
#         ]
#       },
# ... OMMITTED

url = (BASE_URL, 'ietf-interfaces', 'interfaces', 'interface')






#  Using Cisco's native YANG data model
# ============================================================================
# Interface Status: Cisco-IOS-XE-interfaces-oper:interfaces/interface
# - Interface = interface['name']
# - Status = interface['admin-status']
# - Protocol = interface['oper-status']
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

url = (BASE_URL, 'Cisco-IOS-XE-interfaces-oper', 'interfaces', 'interface')



# Interface IP Address: Cisco-IOS-XE-native:native/interface
# - Interface = f'{key}{interface['name']}
# - IP-Address = interface['ip']['address']['primary']['address']
#     There can be more than one IP Address TODO
#
# Sample return data
# {
#   "Cisco-IOS-XE-native:interface": {
#     "GigabitEthernet": [
#       {
#         "name": "1",
#         "description": "MANAGEMENT INTERFACE - DON'T TOUCH ME",
#         "ip": {
#           "address": {
#             "primary": {
#               "address": "10.10.20.48",
#               "mask": "255.255.255.0"
#             }
#           }

url = (BASE_URL, 'Cisco-IOS-XE-native', 'native', 'interface')









#  Using OpenConfig's YANG data model
# ============================================================================
# Interface Status: openconfig-interfaces:interfaces/interface
# - Interface = interface['name']
# - Status = interface['state']['admin-status']
# - Protocol = interface['state']['oper-status']
# - IP-Address = interface['subinterfaces']['subinterface']
#                  ['openconfig-if-ip:ipv4']['addresses']['address']['ip'] 
#     There can be more than one IP Address TODO
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
#         "type": "iana-if-type:ethernetCsmacd",
#         "enabled": true,
#         "ifindex": 1,
#         "admin-status": "UP",
#         "oper-status": "UP",
#         ... OMITTED
#       },
#       "subinterfaces": {
#         "subinterface": [
#           {
#             ...OMITTED
#             "state": {
#               "enabled": true,
#               "name": "GigabitEthernet1",
#               "ifindex": 1,
#               "admin-status": "UP",
#               "oper-status": "UP",
#               ... OMITTED
#             },
#             "openconfig-if-ip:ipv4": {
#               "addresses": {
#                 "address": [
#                   {
#                     "ip": "10.10.20.48",
#                     "config": {
#                       "ip": "10.10.20.48",
#                       "prefix-length": 24
#                     },
# ... OMITTED

url = (BASE_URL, 'openconfig-interfaces', 'interfaces', 'interface')