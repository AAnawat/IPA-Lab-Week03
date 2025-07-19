from netmiko_module.ciscoSSH import ciscoSSH

def test_router1():
    r1 = ciscoSSH('admin', '172.31.134.4')
    with r1.makeConnection() as ssh:
        interfaces = ssh.send_command("sh int des", use_textfsm=True)
    for port in interfaces:
        match port['port']:
            case "Gi0/0":
                assert port['description'] == 'Connect to G0/1 of S0'
                continue
            case "Gi0/1":
                assert port['description'] == 'Connect to PC'
                continue
            case "Gi0/2":
                assert port['description'] == 'Connect to G0/1 of R2'
                continue
            case _:
                continue

def test_router2():
    r2 = ciscoSSH('admin', '172.31.134.5')
    with r2.makeConnection() as ssh:
        interfaces = ssh.send_command("sh int des", use_textfsm=True)
    for port in interfaces:
        match port['port']:
            case "Gi0/0":
                assert port['description'] == 'Connect to G0/2 of S0'
                continue
            case "Gi0/1":
                assert port['description'] == 'Connect to G0/2 of R1'
                continue
            case "Gi0/2":
                assert port['description'] == 'Connect to G0/1 of S1'
                continue
            case "Gi0/3":
                assert port['description'] == 'Connect to NAT'
            case _:
                continue

def test_switch1():
    s1 = ciscoSSH('admin', '172.31.134.3')
    with s1.makeConnection() as ssh:
        interfaces = ssh.send_command("sh int des", use_textfsm=True)
    for port in interfaces:
        match port['port']:
            case "Gi0/0":
                assert port['description'] == 'Connect to G0/3 of S0'
                continue
            case "Gi0/1":
                assert port['description'] == 'Connect to G0/2 of R2'
                continue
            case "Gi1/1":
                assert port['description'] == 'Connect to PC'
                continue
            case _:
                continue