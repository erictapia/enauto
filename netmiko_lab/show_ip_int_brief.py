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

    #device_connection = Netmiko(host=device['ip'], username=device['username'], password=['password'], port=device['port'], device_type=device['device_type'])

    cli_output = device_connection.send_command('show ip interface brief')

    print(cli_output)

    device_connection.disconnect()



if __name__ == '__main__':
    main()

