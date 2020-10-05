import json
# from typing import Final

LIFE_TIME = 60 * 60 * 10
CACHE_TIME = 60 * 60 * 20
OK = json.dumps({"state": True})
FAIL = json.dumps({"state": False})
SERVER_PORT = 5001
TOKEN = 60 * 10
