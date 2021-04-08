# Reservable sandbox
VMANAGE_NODE = {
    "host": "10.10.20.90",
    "username": "admin",
    "password": "C1sco12345",
    "verify": False
}

AUTH_DATA = {
        "j_username": VMANAGE_NODE["username"],
        "j_password": VMANAGE_NODE["password"]
    }

AUTH_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded"
}

BASE_URL = f"https://{VMANAGE_NODE['host']}"