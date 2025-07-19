from netmiko_module.ciscoSSH import ciscoSSH

def configDescription(connection):
   neighbor = connection.send_command("show cdp neighbor", use_textfsm=True)
   command = list()
   for port in neighbor:
      hostname = port['neighbor_name'].split(".")[0]
      command.extend([
            f"interface {port['local_interface']}", 
            f"description Connect to {port['platform'][0]}{port['neighbor_interface']} of {hostname}"
         ])
   connection.send_config_set(command);

def main():
   r1 = ciscoSSH('admin', '172.31.134.4')
   r2 = ciscoSSH('admin', '172.31.134.5')
   s1 = ciscoSSH('admin', '172.31.134.3')

   with r1.makeConnection() as ssh:
      configDescription(ssh)
      command = [
            f"interface G0/1", 
            f"description Connect to PC"
         ]
      ssh.send_config_set(command)
   
   with r2.makeConnection() as ssh:
      configDescription(ssh)
      command = [
            f"interface G0/3", 
            f"description Connect to WAN"
         ]
      ssh.send_config_set(command)

   with s1.makeConnection() as ssh:
      configDescription(ssh)
      command = [
            f"interface G1/1", 
            f"description Connect to PC"
         ]
      ssh.send_config_set(command)
      

if __name__ == "__main__":
   main()