from netmiko_re import getInterfacesInfo

def test_getInterfacesInfo():
    r1, r2 = getInterfacesInfo()
    assert r1['name'] == "R1"
    assert r1['interfaces'] == ['GigabitEthernet0/0', 'GigabitEthernet0/1', 'GigabitEthernet0/2', 'Loopback0']
    assert r1['uptime'] != ""
    assert r2['name'] == "R2"
    assert r2['interfaces'] == ['GigabitEthernet0/0', 'GigabitEthernet0/1', 'GigabitEthernet0/2', 'GigabitEthernet0/3', 'Loopback0', 'NVI0']
    assert r2['uptime'] != ""