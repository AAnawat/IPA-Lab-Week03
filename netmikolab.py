from netmiko_module.ciscoSSH import ciscoSSH
import re, math

def configVLAN101():
    command = [
        "vlan 101",
        "name VLAN101",
        "int range G0/1, G1/1",
        "sw access vlan 101"
    ]
    return command

def configOSPF(networks, default_route, passive = None):
    command = [
        "router ospf 1 vrf control-data"
    ]

    for network in networks:
        command.append(f"network {network} 0.0.0.0 area 0");
    
    if (passive != None):
        command.append(f"passive {passive}")
    
    if (default_route):
        command.append("default-information originate")

    return command

def configInterfaceIP(interface, ip_address, subnet):
    command = [
        f"int {interface}",
        f"ip add {ip_address} {subnet}",
        "no sh"
    ]
    return command

def configPat(insidePorts, outsidePorts, connection):
    command = list()
    for port in insidePorts:
        command.extend([f"int {port}", "ip nat inside"])
    for port in outsidePorts:
        command.extend([f"int {port}", "ip nat outside"])
    
    for port in insidePorts:
        output = connection.send_command(f"sh ip interface {port} | inc Internet")
        ip, subnet = re.search("(?:\d{1,3}.?){4}/\d{1,2}", output).group().split("/")
        subnet = ("/" + subnet)

        command.append(f"access-list 1 permit {ip} {subnet}")
    
    ospf_route = connection.send_command("sh ip route vrf control-data ospf | inc O   ")
    ip_addresses = re.findall("(?:\d{1,3}.?){4}/\d{1,2}", ospf_route)
    for ip_subnet in ip_addresses:
        ip, subnet = ip_subnet.split("/")
        subnet = "/" + subnet
        command.append(f"access-list 1 permit {ip} {subnet}")
    
    for port in outsidePorts:
        command.append(f"ip nat inside source list 1 interface {port} vrf control-data overload")

    return command

def configAccessList(connection):
    ip_int = connection.send_command("sh ip int br")
    ip_addresses = re.findall("((?:\d{1,3}\.?){4})", ip_int)
    ip_addresses = [ip for ip in ip_addresses if ip[0:3] != "172"]

    ports = re.findall("(\w+\d{1,2}/\d{1,2}).*up\s+up", ip_int)
    
    command = [
        "access-list 101 permit tcp 10.30.6.0 0.0.0.255 any eq 22"
    ]
    for ip in ip_addresses:
        command.append(f"access-list 101 deny tcp any host {ip} eq 22")
    command.append("access-list 101 permit ip any any")

    for port in ports:
        command.extend([f"int {port}", "ip access-group 101 in"])
    
    return command

 
def configLab():
    USER = "admin"

    s1 = ciscoSSH(user=USER, host="172.31.134.3")
    r1 = ciscoSSH(user=USER, host="172.31.134.4")
    r2 = ciscoSSH(user=USER, host="172.31.134.5")

    with s1.makeConnection() as ssh:
        ssh.send_config_set(configVLAN101())
        ssh.send_config_set(configAccessList(ssh))
    
    with r1.makeConnection() as ssh:
        ssh.send_config_set(configInterfaceIP("loo0", "1.1.1.1", "255.255.255.255"))
        ssh.send_config_set(configOSPF([
            "192.168.100.1",
            "192.168.1.1"
        ], False, "g0/1"))
        ssh.send_config_set(configAccessList(ssh))

    with r2.makeConnection() as ssh:
        ssh.send_config_set(configInterfaceIP("loo0", "2.2.2.2", "255.255.255.255"))
        ssh.send_config_set(configOSPF([
            "192.168.101.1",
            "192.168.1.2"
        ], True, "g0/2"))
        ssh.send_config_set(configPat(["g0/1", "g0/2"], ["g0/3"], ssh))
        ssh.send_config_set(configAccessList(ssh))

if __name__ == "__main__":
    configLab()