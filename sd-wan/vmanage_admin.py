import json

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


vmanage_session = requests.session()

# Reserved sandbox
vmanage_node = {
    "host": "10.10.20.90",
    "username": "admin",
    "password": "C1sco12345",
    "verify": False
}

data = {
        "j_username": vmanage_node["username"],
        "j_password": vmanage_node["password"]
    }

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

URI = f"https://{vmanage_node['host']}"



def authenticate():
    response = vmanage_session.post(url=f"{URI}/j_security_check", data=data, headers=headers, verify=vmanage_node.get("verify"))

    if response.status_code != 200 or "html" in response.text:
        print(f"Could not authenticate: {response.status_code}\nExiting")
        exit()
    
    # Get XSRF TOKEN
    response = vmanage_session.get(f"{URI}/dataservice/client/token")

    if response.status_code != 200 or "html" in response.text:
        print(f"Could not get token: {response.status_code}\nExiting")
        exit()
    else:
        vmanage_session.headers["X-XSRF-TOKEN"] = response.text


# TODO: User and Group
def get_admin_user():
    response = vmanage_session.get(f"{URI}/dataservice/admin/user")
    
    if response.status_code != 200 or "html" in response.text:
        print(f"Could not get admin users: {response.status_code}")
        return None
    
    return response.json()["data"]


def post_admin_user(username: str, fullname: str, group: list, password: str):
    data = {
        "userName": username,
        "description": fullname,
        "group": group,
        "password": password
    }
    
    headers = {"Content-Type": "application/json"}

    response = vmanage_session.post(f"{URI}/dataservice/admin/user", data=json.dumps(data), headers=headers)

    if response.status_code != 200 or "html" in response.text:
        print(f"Could not add user: {response.status_code}")


def delete_admin_user(username: str):
    response = vmanage_session.delete(f"{URI}/dataservice/admin/user/{username}")

    if response.status_code != 200 or "html" in response.text:
        print(f"Could not delete user: {response.status_code}")
        print(response.text)
    


def get_admin_user_activeSessions():
    # TODO: Response code is 403, why?
    response = vmanage_session.get(f"{URI}/dataservice/admin/user/activeSessions")
    
    if response.status_code != 200 or "html" in response.text:
        print(f"Could not get admin users active sessions: {response.status_code}")
        return None
    
    return response.json()["data"]


def get_admin_user_role():
    response = vmanage_session.get(f"{URI}/dataservice/admin/user/role")

    if response.status_code != 200 or "html" in response.text:
        print(f"Could not get admin user role: {response.status_code}")
        return None
    
    return response.json()


def get_admin_usergroup():
    response = vmanage_session.get(f"{URI}/dataservice/admin/usergroup")

    if response.status_code != 200 or "html" in response.text:
        print(f"Could not get admin usergroup: {response.status_code}")
        return None
    
    return response.json()["data"]


# TODO: Audit Log

# TODO: Tenant Management

# TODO: Tenant Backup Restore

# TODO: Utility - Logging

# TODO: Utility - Security

if __name__ == "__main__":
    
    authenticate()

    ###### GET ADMIN USERS AND PRINT THEM
    print("=" * 80)
    print("----- USERS")
    print("=" * 80)

    users = get_admin_user()

    for user in users:
        print(f"     Username: {user['userName']}")
        print(f"     Full name: {user.get('description')}")

        # Each user can be in multiple groups
        print("     Groups: ", end="")

        for group in user["group"]:
            print(group, end=" ")
        
        print()
        print("     " + "=" * 75)

    print()

    ##### GET ADMIN USER ACTIVE SESSIONS
    print("=" * 80)
    print("----- ACTIVE USER SESSIONS")
    print("=" * 80)

    user_sessions = get_admin_user_activeSessions()

    print(f"     {user_sessions}")
    print()

    ##### CHECK IF THIS USER SESSION HAS ADMIN PRIVILEGES
    print("=" * 80)
    print("----- USER ADMIN ROLE")
    print("=" * 80)

    user_role = get_admin_user_role()

    print(f"     Username: {vmanage_node['username']} is admin: {user_role['isAdmin']}")
    print()
    
    ##### GET USERGROUPS AND PRINT PRIVILEGES
    print("=" * 80)
    print("----- USERGROUP PRIVILEGES")
    print("=" * 80)

    usergroups = get_admin_usergroup()

    for group in usergroups:
        print("     " + "=" * 75)
        print(f"     Group: {group['groupName']}")
        print("     " + "=" * 75)
        print("          Tasks")
        print("          " + "=" * 70)

        for task in group["tasks"]:
            if task.get("enabled"):
                print(f"          {task['feature']}:", end=" ")
                
                if task.get("read"):
                    print("r", end="")
                
                if task.get("write"):
                    print("w", end="")

                print()

        print()

    ##### ADD ADMIN USER
    username = "pythonuser"

    print("=" * 80)
    print(f"ADDING USER: {username}")
    print("=" * 80)
    
    post_admin_user(username, "Python Automation", ["netadmin"], "cisco")
    
    ##### VERIFY
    print("=" * 80)
    print(f"VERIFYING {username} EXISTS")
    print("=" * 80)
    users = get_admin_user()

    found = None
    for user in users:
        if user["userName"] == username:
            print(f"     Found user: {username}")
            found = True
            break
    
    ##### DELETE USER
    if found:
        print("=" * 80)
        print(f"DELETING USER: {username}")
        delete_admin_user(username)
    
    ##### VERIFY
    print("=" * 80)
    print(f"VERIFYING {username} DOESN'T EXISTS")
    print("=" * 80)
    users = get_admin_user()

    found = None
    for user in users:
        if user["userName"] == username:
            print(f"     Found user: {username}")
            found = True
            break
    
    if not found:
        print(f"     {username} not found")

    vmanage_session.close()
