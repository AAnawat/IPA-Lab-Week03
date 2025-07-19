from netmiko_module.ciscoSSH import ciscoSSH
from jinja2 import Environment, FileSystemLoader
import re
from pprint import pprint

def configVLAN101(env:  Environment):
    template = env.get_template("vlan-config.j2");
    data = {
        'vlanID': 101,
        'name': 'VLAN101',
        'ports': ["g0/1", "g1/1"]
    }
    return template.render(data).split("\n")

def configOSPF(env: Environment, ip_addresses, passive, default_route):
    template = env.get_template("ospf-config.j2")
    data = {
        "ip_addresses": ip_addresses,
        "passive": passive,
        "default_route": default_route
    }
    return template.render(data).split("\n")

def configInterfaceIP(env: Environment, interface, ip_address, subnet):
    template = env.get_template("ip-interface-config.j2")
    data = {
        "interface": interface,
        "ip": ip_address,
        "subnet": subnet
    }
    return template.render(data).split("\n")


def configPat(env: Environment, insidePorts, outsidePorts, connection):
    template = env.get_template("pat-config.j2")
    
    permitList = list()
    for port in insidePorts:
        output = connection.send_command(f"sh ip interface {port} | inc Internet")
        ip, subnet = re.search("(?:\d{1,3}.?){4}/\d{1,2}", output).group().split("/")

        permitList.append({"ip": ip, "subnet": subnet})
    
    ospf_route = connection.send_command("sh ip route vrf control-data ospf | inc O   ")
    ip_addresses = re.findall("(?:\d{1,3}.?){4}/\d{1,2}", ospf_route)
    for ip_subnet in ip_addresses:
        ip, subnet = ip_subnet.split("/")
        permitList.append({"ip": ip, "subnet": subnet})

    data = {
        "inside": insidePorts,
        "outside": outsidePorts,
        "permits": permitList
    }
    return template.render(data).split("\n")

def configAccessList(env: Environment, connection):
    template = env.get_template("accessList-config.j2")
    ip_int = connection.send_command("sh ip int br")
    ip_addresses = re.findall("((?:\d{1,3}\.?){4})", ip_int)
    ip_addresses = [ip for ip in ip_addresses if ip[0:3] != "172"]

    ports = re.findall("(\w+\d{1,2}/\d{1,2}).*up\s+up", ip_int)
    
    data = {
        "ip_addresses": ip_addresses,
        "ports": ports
    }
    return template.render(data).split("\n")


def configLab():
    env = Environment(
        loader=FileSystemLoader("./jinja2_template"),
        trim_blocks=True,
        lstrip_blocks=True
        )

    s1: ciscoSSH = ciscoSSH("admin", "172.31.134.3")
    r1: ciscoSSH = ciscoSSH('admin', '172.31.134.4')
    r2: ciscoSSH = ciscoSSH('admin', '172.31.134.5')

    with s1.makeConnection() as ssh:
        ssh.send_config_set(configVLAN101(env))
        ssh.send_config_set(configAccessList(env, ssh))
    
    with r1.makeConnection() as ssh:
        ssh.send_config_set(configInterfaceIP(env, "loo0", "1.1.1.1", "255.255.255.255"))
        ssh.send_config_set(configOSPF(env, [
            "192.168.100.1",
            "192.168.1.1"
        ], ["g0/1"], False))
        ssh.send_config_set(configAccessList(env, ssh))
    
    with r2.makeConnection() as ssh:
        ssh.send_config_set(configInterfaceIP(env, "loo0", "2.2.2.2", "255.255.255.255"))
        ssh.send_config_set(configOSPF(env, [
            "192.168.101.1",
            "192.168.1.2"
        ], ["g0/2"], True))
        ssh.send_config_set(configPat(env, ["g0/1", "g0/2"], ["g0/3"], ssh))
        ssh.send_config_set(configAccessList(env, ssh))
        
if __name__ == "__main__":
    configLab();