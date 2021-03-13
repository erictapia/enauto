import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Cisco SD-WAN 19.2 Always On 
#
# host: https://sandbox-sdwan-1.cisco.com
# username: devnetuser
# password: RG!_Yw919_83

# vmanage_node = {
#     "host": "sandbox-sdwan-1.cisco.com",
#     "username": "devnetuser",
#     "password": "RG!_Yw919_83"
# }


vmanage_node = {
    "host": "10.10.20.90",
    "username": "admin",
    "password": "C1sco12345",
    "verify": False
}


URL = f"https://{vmanage_node['host']}"

vmanage_session = requests.session()


def authenticate():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "j_username": vmanage_node["username"],
        "j_password": vmanage_node["password"]
    }

    response = vmanage_session.post(url=f"{URL}/j_security_check", headers=headers, data=data, verify=vmanage_node["verify"])

    if response.status_code != 200:
        print(f"Status code: {response.status_code}\n\nExiting")
        exit()
    
    if "<html>" in response.text:
        print("Credentials were not accepted.\n\nExiting")
        exit()

# TODO - When session expires, all request may have a response code of 200
#        but response is html page asking to authenticate
def get_devices(device_type = "vedge"):

    response = vmanage_session.get(url=f"{URL}/dataservice/system/device/{device_type}")
    #response = vmanage_session.get(url=f"{URL}/dataservice/device")

    if response.status_code != 200:
        print(f"Status code: {response.status_code}")
    
    return response.json()


def get_device_template(template_id):
    
    response = vmanage_session.get(url=f"{URL}/dataservice/template/device/object/{template_id}")

    if response.status_code != 200:
        print(f"Status code: {response.status_code}")
    
    return response.json()


def get_template_feature():
    response = vmanage_session.get(url=f"{URL}/dataservice/template/feature")

    if response.status_code != 200:
        print(f"Status code: {response.status_code}")
        return None
    
    return response.json()


if __name__ == "__main__":
    authenticate()
    
    devices = get_devices()["data"]

    features = dict()
    features = { feature["templateId"] : feature for feature in get_template_feature()["data"]}

    for device in devices:

        # Getting template to look up features
        device_features = None

        if device.get("templateId"):
            device_features = get_device_template(device["templateId"])

        
        prefix = " " * 5
        
        if device.get("vedgeCertificateState") == "certinstalled":
            print("=" * 80)
            print(f"Device")
            print(f"{prefix}Hostname: {device.get('host-name')}")
            print(f"{prefix}NCS Device Name: {device.get('ncsDeviceName')}")
            print(f"{prefix}IP: {device.get('deviceIP')}")
            print(f"{prefix}Site ID: {device.get('site-id')}")
            print("=" * 80)
            print(f"{prefix}Serial # {device.get('serialNumber')}")
            print(f"{prefix}Chassis Number: {device.get('chasisNumber')}")
            print(f"{prefix}Device Model: {device.get('deviceModel')}")
            print(f"{prefix}Version: {device.get('defaultVersion')}")
            print()
            print(f"{prefix}Template: {device.get('template')}")
            print(f"{prefix}" + "=" * (80 - len(prefix)))

            print(f"{prefix * 2}Features")
            if device_features:
                for device_feature in device_features["generalTemplates"]:
                    print(f"{prefix * 3}- {device_feature['templateType']} : {features[device_feature['templateId']].get('templateDescription')}")

                    if device_feature.get("subTemplates"):
                        for sub_template in device_feature["subTemplates"]:
                            print(f"{prefix * 4}- {sub_template['templateType']} : {features[sub_template['templateId']]['templateName']}")

            print(f"{prefix}" + "=" * (80 - len(prefix)))
            print("\n\n")
        
        else:
            print("=" * 80)
            print(f"{prefix}Device Model: {device.get('deviceModel')}")
            print("=" * 80)
            print(f"{prefix}Token # {device.get('serialNumber')}")
            print(f"{prefix}Chassis Number: {device.get('chasisNumber')}")
            print("\n\n")

    vmanage_session.close()

