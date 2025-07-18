import paramiko

class paraSSH():
    def __init__(self, username: str, host: str, keyPath: str = None):
        self.username: str = username
        self.host: str = host
        self.keyPath: str = keyPath
        
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    def __enter__(self):
        if self.keyPath == None:
            self.client.connect(
                hostname=self.host,
                username=self.username,
                look_for_keys=True,
                allow_agent=False,
                disabled_algorithms={
                    'pubkeys': ['rsa-sha2-512', 'rsa-sha2-256']
                }
            )
        else:
            self.client.connect(
                hostname=self.host,
                username=self.username,
                key_filename=self.keyPath,
                allow_agent=False,
                disabled_algorithms={
                    'pubkeys': ['rsa-sha2-512', 'rsa-sha2-256']
                }
            )
        return self.client
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()