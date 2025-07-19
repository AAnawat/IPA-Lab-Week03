from netmiko import ConnectHandler

class ciscoSSH():
    def __init__(self, user: str, host: str, keyPath: str = "./keys/id_rsa"):
        self.user: str = user
        self.host: str = host
        self.keyPath: str = keyPath
    
    def makeConnection(self):
        option = {
            'device_type': 'cisco_ios',
            'host': self.host,
            'username': self.user,
            'allow_agent': False,
            'use_keys': True,
            'key_file': self.keyPath,
            'disabled_algorithms': {
                'pubkeys': ['rsa-sha2-512', 'rsa-sha2-256']
            }
        }
        
        connection = ConnectHandler(**option)
        return connection