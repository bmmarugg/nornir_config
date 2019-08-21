import urllib3
from napalm import get_network_driver

urllib3.disable_warnings()

with open("path/to/nexus_device_list.txt") as f:
    device_line = f.read().splitlines()
while("" in device_line):
    device_line.remove("")
device_list = device_line


def main():
    driver = get_network_driver('nxos')
    port_arg = {'port': 'NX-API PORT'}
    device_conn = driver(device, 'USERNAME', 'PASSWORD', optional_args=port_arg)
    device_conn.open()

    checkpoint = device_conn._get_checkpoint_file()

    device_checkpoint = open("path/to/{}-checkpoint.txt"
                             .format(device), 'w')
    device_checkpoint.write(checkpoint)

    device_conn.close()


for device in device_list:
    main()
