import requests
from utils.AttackResult import AttackResult

"""
This attack verifies that port 80 is always redirected to port 443.
"""


def execute(results, hosts):
    for host in hosts:
        attack_host(results, host)


def attack_host(results, host):
    print("Running redirect_attack.py host name: {}".format(host))
    url = 'http://{}'.format(host)

    try:
        r = requests.get(url)
        history_status_code = 0
        if r.history and r.history[0]:
            history_status_code = r.history[0].status_code

        result = AttackResult('redirect', url, history_status_code == 301, '301 redirect sent')
    except requests.exceptions.RequestException as ex:
        result = AttackResult('redirect', url, False, ex)

    results.append(result)
