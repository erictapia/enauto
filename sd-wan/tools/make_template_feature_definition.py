import json
import os

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from sdwan_reserve import VMANAGE_NODE, AUTH_DATA, AUTH_HEADERS, BASE_URL

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


DEF_DIR = "./template/feature/definition"
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

    # Get template feature
    url = f"{BASE_URL}/dataservice/template/feature"
    response = get_request(url)

    features = response.get("data")

    for feature in features:
        is_default = feature.get("factoryDefault")
        feature_name = feature.get("templateName")

        # Assign Directory
        dir = None
        if feature_name:
            for feature_type in feature_types:
                type_name = feature_type.get("name")

                if type_name and (type_name == feature.get("templateType")):
                    parent = feature_type.get("parent")

                    if parent:
                        dir = f"{DEF_DIR}/{parent}"
                    else:
                        dir = f"{DEF_DIR}/undefined"
                    
                    if is_default:
                        dir += f"/factory_default"
                    else:
                        dir += "/non_default"

                    break
        
        if dir:
            create_directory(dir)
            d = json.loads(feature.get('templateDefinition'))

            # Write definition to file
            with open(dir + "/" + feature.get('templateName') + ".json", "w") as writer:
                json.dump(d, writer, indent=2)
