from netmiko import Netmiko
import json

# DevNet IOS XE on CSR 16.9.3 always on sandbox
device = {
    'device_type': 'cisco_ios',
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


    # Using an environmental variable to define the path of the NTC templates containing
    # all the textfsm templates. In my environment it will be set with the following:
    #
    #    export NET_TEXTFSM=~/dev/enauto/venv/lib/python3.8/site-packages/ntc_templates/templates
    #

    cli_output = device_connection.send_command('show ip int brief', use_textfsm=True)

    print(json.dumps(cli_output, indent=4))

    device_connection.disconnect()



if __name__ == '__main__':
    main()

