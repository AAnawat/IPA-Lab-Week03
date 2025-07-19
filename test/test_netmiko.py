from netmiko_module.ciscoSSH import ciscoSSH
import re

def test_vlanCreation():
    s1 = ciscoSSH(user='admin', host='172.31.134.3')
    with s1.makeConnection() as ssh:
        output = ssh.send_command("sh vlan br")
    vlanLine = re.search("^101.*", output, flags=re.MULTILINE);
    match = re.findall("(\w{1,2}\d{1,2}/\d{1,2})", vlanLine.group() if (vlanLine != None) else " ");
    assert match == ['Gi0/1', 'Gi1/1']

def test_loopbackCreation():
    r1 = ciscoSSH(user='admin', host='172.31.134.4')
    r2 = ciscoSSH(user='admin', host='172.31.134.5')

    with r1.makeConnection() as ssh:
        r1_output = ssh.send_command("sh ip int br | inc Loopback")
    with r2.makeConnection() as ssh:
        r2_output = ssh.send_command("sh ip int br | inc Loopback")

    assert r1_output != ""
    assert r2_output != ""

def test_ospfConfig():
    r1 = ciscoSSH(user='admin', host='172.31.134.4')
    r2 = ciscoSSH(user='admin', host='172.31.134.5')

    for router in [r1, r2]:
        with router.makeConnection() as ssh:
            assert ssh.send_command("sh ip ospf 1") != "%OSPF: No router process 1"
            assert re.search("(?:\d{1,3}.?){4}", ssh.send_command('sh ip ospf neighbor'), flags=re.MULTILINE) != None