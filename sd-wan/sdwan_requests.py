import requests
import json

# Cisco SD-WAN 19.2 Always On 
#
# host: https://sandbox-sdwan-1.cisco.com
# username: devnetuser
# password: RG!_Yw919_83

controller = {
    "host": "sandbox-sdwan-1.cisco.com",
    "username": "devnetuser",
    "password": "RG!_Yw919_83"
}


# Global constants

BASE_URL = f"https://{controller['host']}"

# TODO:
# 	- API requests using Device Intentory API, retrieve and display data
# 	- API requests using Administration API
#	- API requests using Configuration API, modify fabric configuration
#	- API requests using Monitoring API including real-time
#	- API requests using Troubleshoot API

# Instantiate a requests session
host_session = requests.session()

# Authenticate to get a j_session_id
resource = "j_security_check"
headers = {
    "Content-type": "application/x-www-form-urlencoded" 
}

#body = f"j_username={controller["username"]}&j_password={controller["password"]}"
body = {
    "j_username": controller["username"],
    "j_password": controller["password"]
}


host_session.headers = headers

try:
    # Authenticate
    response = host_session.post(f"{BASE_URL}/{resource}", data=body, verify=True)
    print()
    print(response)
    print(response.text)
    print(response.headers)
    print()

    # CLI like HTTP get requests
    while True:
        resource = input("Enter resource: ")

        if resource == "exit":
            break
        
        if resource == "":
            continue
        print(f"Request: {BASE_URL}/{resource}", end="\n\n")

        response = host_session.get(f"{BASE_URL}/{resource}", data=None, verify=True)

        if response.status_code == 200:
            
            print()
            print(response)
            print()
            print(response.headers)
            print("Body:")
            print("="*79)
            print(json.dumps(response.json()["data"], indent=2))

        else:
            print(f"Response code: {response.status_code}")

        print()
finally:
    print("EXIT")
    host_session.close()