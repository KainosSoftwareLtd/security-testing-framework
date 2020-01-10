import subprocess
import xml.etree.ElementTree as et
from utils.AttackResult import AttackResult


def execute(results, hosts, expected_open_ports):
    for host in hosts:
        attack(results, host, expected_open_ports)


def validate(expected_open_ports, host_name):
    found_open = []
    root = et.parse(host_name + '.xml').getroot()
    for port in root.findall('.//port'):
        port_id = port.get('portid')
        state_element = port.find('state')
        state = state_element.get('state')
        if state == 'open':
            found_open.append(int(port_id))
    return list(set(found_open) - set(expected_open_ports))


def attack(results, host_name, expected_open_ports):
    print("Running firewall/firewall_attack.py host name: {} expected open ports".format(host_name, expected_open_ports))

    # '-p1-65535'
    subprocess.call(['nmap', '-oX', host_name + '.xml', host_name])
    illegal_open = validate(expected_open_ports, host_name)
    print(illegal_open)
    if len(illegal_open) > 0:
        results.append(AttackResult('firewall', host_name, False, 'Firewall ingress rules are incorrect.  The following ports are open: ' + str(illegal_open)))
    else:
        results.append(AttackResult('firewall', host_name, True, 'Firewall ingress rules are set correctly'))

# results = []
# attack(results, 'google.co.uk')
# print(results)