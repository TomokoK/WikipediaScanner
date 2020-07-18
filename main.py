#
# Script that checks supplied IP addresses with Wikipedia for contributions
# 2020-03-28
# contact: TomokoK @ github
# TODO: eventually convert manual ip entering to scanning through bulk WHOIS data using organization
#
import ipaddress
import sys
import requests
from datetime import datetime

inputCIDR = input("Enter the IPv4 CIDR (you can find this by looking up your organization at https://ipinfo.io/): ")

try:
    ipCast = ipaddress.IPv4Network(inputCIDR)
except ValueError:
    print("ERROR: invalid IPv4 CIDR")
    sys.exit(1)

ipList = list(ipCast)
session = requests.Session()
apiURL = "https://en.wikipedia.org/w/api.php"

for i in ipList:
    PARAMS = {
        "action":   "query",
        "format":   "json",
        "list": "usercontribs",
        "ucuser":   i
    }
    retrieve = session.get(url=apiURL, params=PARAMS)
    apiData = retrieve.json()
    userContribs = apiData["query"]["usercontribs"]

    print(i)
    if not userContribs:
        print("No contribs")
    else:
        for uc in userContribs:
            userContribTitle = uc["title"]
            userContribDate = str(uc["timestamp"]).split("T")[0]
            print(userContribTitle + " - " + userContribDate)
