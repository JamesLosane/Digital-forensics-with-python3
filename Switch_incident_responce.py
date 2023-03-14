import paramiko
import re
import pandas as pd

# establish an SSH connection to the switch
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('switch_ip_address', username='username', password='password')

# retrieve the CAM table data
stdin, stdout, stderr = ssh.exec_command('show mac address-table')

# parse the CAM table data
data = stdout.read().decode()
pattern = re.compile(r'(\d+)\s+(\w+\.\w+\.\w+)\s+([A-Z]+)\s+(\d+)\s+(\S+)')
matches = pattern.findall(data)
df = pd.DataFrame(matches, columns=['vlan', 'mac', 'type', 'port', 'age'])

# detect MAC flooding
def detect_mac_flooding(df):
    """
    Detect MAC flooding by identifying MAC addresses that appear on multiple interfaces.
    """
    # group by MAC address
    grouped = df.groupby('mac')
    
    # identify MAC addresses that appear on multiple interfaces
    mac_flood = grouped.filter(lambda x: len(x) > 1)
    
    return mac_flood

mac_flood = detect_mac_flooding(df)
print('\nMAC flooding:')
print(mac_flood)

# analyze the CAM table data
duplicate_macs = df[df.duplicated(subset='mac', keep=False)]
print('\nDuplicate MAC addresses:')
print(duplicate_macs)

unknown_macs = df[df['type'] == 'U']
print('\nUnknown MAC addresses:')
print(unknown_macs)

aging_macs = df[df['age'].astype(int) > 300]
print('\nAging MAC addresses (age > 300 seconds):')
print(aging_macs)

vlan_count = df['vlan'].value_counts()
print('\nNumber of MAC addresses per VLAN:')
print(vlan_count)

interface_count = df['port'].value_counts()
print('\nNumber of MAC addresses per interface:')
print(interface_count)

# close the SSH connection
ssh.close()
