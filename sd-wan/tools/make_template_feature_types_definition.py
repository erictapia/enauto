import json
import os

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from sdwan_reserve import VMANAGE_NODE, AUTH_DATA, AUTH_HEADERS, BASE_URL

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


TYPE_DIR = "./template/feature/types/definition"
vmanage_session = requests.session()


def authenticate():
    url = f"{BASE_URL}/j_security_check"

    response = vmanage_session.post(url=url, data=AUTH_DATA, headers=AUTH_HEADERS, verify=VMANAGE_NODE.get("verify"))

    if response.status_code != 200 or "html" in response.text:
        print(f"Could not authenticate: {response.status_code}\nExiting")
        exit()


def create_directory(dir):
    # Create directory if does not exist
    if not os.path.isdir(dir):
        os.makedirs(dir)


def get_request(url):
    
    response = vmanage_session.get(url=url)

    if response.status_code != 200 or "html" in response.text:
        print(f"Request failed:\n\n{url}\n\n{response.status_code}\n\nExiting")
        exit()
    
    return response.json()


if __name__ == "__main__":

    authenticate()
    
    # Get template feature types
    url = f"{BASE_URL}/dataservice/template/feature/types"
    response = get_request(url)
    
    feature_types = response.get("data")

    for feature_type in feature_types:
        feature_type_name = feature_type.get("name")
        software_versions = [software_version for software_version in feature_type.get("softwareVersions")]

        # build dir for each software version
        if software_versions:
            for software_version in software_versions:

                # Get feature type schema
                url = f"{BASE_URL}/dataservice/template/feature/types/definition/{feature_type_name}/{software_version['name']}"
                response = get_request(url)
                
                fields = response.get("fields")

                if fields:
                    dir = f"{TYPE_DIR}/{feature_type_name}/{software_version['name']}" 

                    create_directory(dir)

                    # Write definition to file
                    with open(dir + "/" + feature_type_name +  ".json", "w") as writer:
                        json.dump(fields, writer, indent=2)
