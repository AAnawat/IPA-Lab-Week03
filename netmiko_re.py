from netmiko_module.ciscoSSH import ciscoSSH
from pprint import pprint
import re

def getActiveInterfaces(connection):
    output = connection.send_command("sh ip int br")
    interfaces = re.findall("^(\S+\d).*up\s+up", output, flags=re.MULTILINE)
    return interfaces

def getUpTime(connection):
    output = connection.send_command("sh version")
    up_time = re.search("uptime is (\d{1,2}) hours, (\d{1,2}) minutes", output);
    return f"{up_time[0]}h {up_time[1]}m."

def getInterfacesInfo():
    r1 = ciscoSSH('admin', '172.31.134.4')
    r2 = ciscoSSH('admin', '172.31.134.5')

    router1 = { "name": "R1" }
    with r1.makeConnection() as ssh:
        router1['interfaces'] = getActiveInterfaces(ssh)
        router1['uptime'] = getUpTime(ssh)

    router2 = { "name": "R2" }
    with r2.makeConnection() as ssh:
        router2['interfaces'] = getActiveInterfaces(ssh)
        router2['uptime'] = getUpTime(ssh)
    return router1, router2
        
if __name__ == "__main__":
    r1, r2 = getInterfacesInfo()
    pprint(r1)
    print("============================================================================")
    pprint(r2)