from ncclient import manager


device = {
    'host': '10.10.20.175',
    'port': '830',
    'username': 'cisco',
    'password': 'cisco',
    'hostkey_verify': False,
    'device_params': {'name': 'iosxe'}
}

# TODO:
# configuration = [
#     'no call-home',
#     'logging buffered 900000',
#     'netconf-yang', <== not possible 
#     'no license smart enable',

#  how to push file with ncclient?
#     'tclsh',
#     'puts [open "bootflash:ztp.py" w+] { test }',
#     'tclquit', 
# ]

hostname = 'HUB'
interface_id = 2
ipv4 = '10.1.2.1'
mask = '255.255.255.0'
src_file = 'bootflash:ztp.py'
src_alias = 'ztp.py'

conf = f'''
<config>
    <native 
        xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <service>
            <call-home/>
        </service>
        <hostname>{hostname}</hostname>
        <ip>
            <domain>
                <lookup>false</lookup>
                <name>devnet.engineer</name>
            </domain>
            <dns>
                <server></server>
            </dns>
            <dhcp>
                <excluded-address xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-dhcp">
                    <low-high-address-list>
                        <low-address>203.0.113.0</low-address>
                        <high-address>203.0.113.10</high-address>
                    </low-high-address-list>
                </excluded-address>
                <pool xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-dhcp">
                    <id>ZTP</id>
                    <option>
                        <option-range>
                            <option-range>67</option-range>
                            <ascii>ztp.py</ascii>
                        </option-range>
                        <option-range>
                            <option-range>150</option-range>
                            <ip>203.0.113.1</ip>
                        </option-range>
                    </option>
                    <default-router>
                        <default-router-list>203.0.113.1</default-router-list>
                    </default-router>
                    <dns-server>
                        <dns-server-list>203.0.113.1</dns-server-list>
                    </dns-server>
                    <domain-name>devnet.engineer</domain-name>
                    <network>
                        <primary-network>
                            <number>203.0.113.0</number>
                            <mask>255.255.255.0</mask>
                        </primary-network>
                    </network>
                </pool>
            </dhcp>
            <host>
                <host-list>
                    <name>connect.devnet.engineer</name>
                    <ip-list>203.0.113.1</ip-list>
                </host-list>
                <host-list>
                    <name>hub.devnet.engineer</name>
                    <ip-list>10.0.0.1</ip-list>
                </host-list>
                <host-list>
                    <name>site1.devnet.engineer</name>
                    <ip-list>10.0.0.2</ip-list>
                </host-list>
                <host-list>
                    <name>site2.devnet.engineer</name>
                    <ip-list>10.0.0.3</ip-list>
                </host-list>
            </host>
            <scp>
                <server>
                    <enable/>
                </server>
            </scp>
            <ssh>
                <version>2</version>
            </ssh>
            <http xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-http">
                <server>false</server>
                <secure-server>true</secure-server>
            </http>
        </ip>
        <cdp>
            <run xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-cdp"/>
        </cdp>
        <interface>
            <GigabitEthernet>
                <name>{interface_id}</name>
                <ip>
                    <address>
                        <primary>
                            <address>{ipv4}</address>
                            <mask>{mask}</mask>
                        </primary>
                    </address>
                </ip>
            </GigabitEthernet>
        </interface>
        <login>
            <on-success>
                <log></log>
            </on-success>
        </login>
        <tftp-server>
            <name>{src_file}</name>
            <alias>{src_alias}</alias>
        </tftp-server>
    </native>
</config>
'''

with manager.connect(**device) as conn:

    reply = conn.edit_config(conf, target='running')
    print(reply)
