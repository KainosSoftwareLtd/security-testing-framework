#!/usr/bin/python3

import os

import firewall.firewall_attack as firewall_attack
import certificates.redirect_attack as redirect_attack
import certificates.forward_secrecy_attack as forward_secrecy_attack
import certificates.certificate_chain_attack as certificate_chain_attack
import certificates.hostname_attack as hostname_attack

import utils.reporting as reporting

# Read environment variables
results = []
root_dir = os.environ['ROOT_DIR']
hosts = os.environ['HOSTS'].split(',')


# Execute attacks
# firewall_attack.execute(results, hosts, [443])
redirect_attack.execute(results, hosts)
forward_secrecy_attack.execute(results, hosts)
certificate_chain_attack.execute(results, hosts)
hostname_attack.execute(results, hosts)

# Report result to console and html file
sorted_results = sorted(results, key=reporting.pass_fail)
reporting.console(sorted_results)
reporting.html(root_dir, sorted_results)