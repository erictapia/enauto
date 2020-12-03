from netmiko import Netmiko


# DevNet IOS XE on CSR 16.9.3 always on sandbox
device = {
    'device_type': 'cisco_xe',
    'ip': 'ios-xe-mgmt.cisco.com',
    'username': 'developer',
    'password': 'C1sco12345',
    'port': '8181',
}


def main():
    device_connection = Netmiko(**device)


    # Had to add the following to users ssh config file ~/.ssh/config:
    #
    #    Host ios-xe-mgmt.cisco.com
    #    KexAlgorithms=+diffie-hellman-group-exchange-sha1,diffie-hellman-group14-sha1
    #
    # otherwise the connection would fail due to no matching key exchanged method found.

    cli_output = device_connection.send_command('show ip interface brief')

    print(cli_output)

    device_connection.disconnect()



if __name__ == '__main__':
    main()

