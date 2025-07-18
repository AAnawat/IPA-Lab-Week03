from paramiko_module.paraSSH import paraSSH

def makeConnection(*ip_addresses) -> str:
    USER: str = "admin"
    KEY_PATH = "./keys/id_rsa"

    try:
        for ip in ip_addresses:
            connection: paraSSH = paraSSH(username=USER, host=ip, keyPath=KEY_PATH);
            with connection as ssh:
                _, _, _ = ssh.exec_command(" ");
        return "Run success"
    except Exception as e:
        print(e)
        return "Can't connect to host"

if __name__ == "__main__":
    output = makeConnection(
        "172.31.134.1",
        "172.31.134.2",
        "172.31.134.3",
        "172.31.134.4",
        "172.31.134.5",
    )
    print(output);