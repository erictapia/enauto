from netmiko import Netmiko
from netmiko import file_transfer


# DevNet Cisco Modeling Labs Enterprise reserve sandbox 
# - Multi Platform Network lab has a bridge between lab and vpn
# - See topology ./images/topology.png
device = {
    'device_type': 'cisco_ios',
    'ip': '10.10.20.175',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco',
    'port': '22'
}

configuration = [
    'hostname HUB',
    'cdp run',
    'ip host connect.devnet.engineer 203.0.113.1',
    'ip host hub.devnet.engineer 10.0.0.1',
    'ip host site1.devnet.engineer 10.0.0.2',
    'ip host site2.devnet.engineer 10.0.0.3',
    'ip domain name devnet.engineer',
    'ip dhcp excluded-address 203.0.113.0 203.0.113.10',
    'ip dhcp pool ZTP',
    'network 203.0.113.0 255.255.255.0',
    'default-router 203.0.113.1',
    'domain-name devnet.engineer',
    'dns-server 203.0.113.1',
    'option 150 ip 203.0.113.1',
    'option 67 ascii ztp.py',
    'interface GigabitEthernet2',
    'ip address 203.0.113.1 255.255.255.0',
    'no shutdown',
    'tftp-server bootflash:ztp.py alias ztp.py',
    'ip scp server enable',
    'ip dns server',
    'no ip http secure-server',
    'ip ssh version 2',
    'no license smart enable',
    'end',
    'tclsh',
    'puts [open "bootflash:ztp.py" w+] { test }',
    'tclquit', 
]

ztp_script = 'ztp_script/ztp.py'

def main():
    device_connection = Netmiko(**device)


    # Had to add the following to users ssh config file ~/.ssh/config:
    #
    #    Host ios-xe-mgmt.cisco.com
    #    KexAlgorithms=+diffie-hellman-group-exchange-sha1,diffie-hellman-group14-sha1
    #
    # otherwise the connection would fail due to no matching key exchanged method found.

    cli_output = device_connection.send_config_set(configuration)

    print(cli_output)

    # Transfer ZTP script file
    transfer_dict = file_transfer(device_connection,
                                    source_file=ztp_script, dest_file=ztp_script,
                                      file_system='bootflash:',
                                        direction='put',
                                          overwrite_file=True)
    
    print(transfer_dict)

    device_connection.disconnect()



if __name__ == '__main__':
    main()

