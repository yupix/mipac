import json
import os

from type import OpenAPI

PATHS: list[str] = []
PREFIX = "/api"
TOP_COMMENT = """\"\"\"
=======================
        WARNING
=======================
 This file is automatically generated by compiler/endpoints.py.
 If this file is modified and then auto-generated, the changes will be lost.
\"\"\"\n
"""
IMPORTS = "from typing import Literal\n\n"
TEMPLATES = "ENDPOINTS = "

with open("./datas/v13_api.json", mode="r", encoding="utf-8") as f:
    api: OpenAPI = json.load(f)
    for path in api["paths"]:
        PATHS.append(f"{PREFIX}{path}")


old_endpoints = []
if os.path.exists("./datas/endpoints.json"):
    with open("./datas/endpoints.json", mode="r", encoding="utf-8") as f:
        old_endpoints = json.load(f)

with open("./datas/endpoints.json", mode="w", encoding="utf-8") as f:
    removed_endpoints = []
    for i in old_endpoints:
        if i not in list(dict.fromkeys(PATHS)):
            removed_endpoints.append(i)
    with open("./datas/removed-endpoints.json", mode="w", encoding="utf-8") as removed_endpoints_f:
        json.dump(removed_endpoints, removed_endpoints_f, ensure_ascii=False, indent=4)

    old_endpoints.extend(PATHS)
    old_endpoints = list(dict.fromkeys(old_endpoints))
    json.dump(old_endpoints, f, ensure_ascii=False, indent=4)

with open("../mipac/types/endpoints.py", "w", encoding="utf-8") as f:
    data = json.dumps(old_endpoints, ensure_ascii=False, indent=4)
    f.write(f"{TOP_COMMENT}{IMPORTS}{TEMPLATES}Literal{data}\n")
