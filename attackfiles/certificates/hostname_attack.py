from sslyze.ssl_settings import TlsWrappedProtocolEnum
from sslyze.plugins.certificate_info_plugin import CertificateInfoPlugin, CertificateInfoScanCommand
from sslyze.server_connectivity_tester import ServerConnectivityTester, ServerConnectivityError
from utils.AttackResult import AttackResult

"""
This attack verifies that TLS certificates match hostname, are trusted and the chain order is valid.
"""


def execute(results, hosts):
    for host in hosts:
        attack(results, host)


def attack(results, host_name):
    print("Running 10.16 attack.py host name: {}".format(host_name))
    report = {}

    try:
        server_tester = ServerConnectivityTester(
            hostname=host_name,
            port=443,
            tls_wrapped_protocol=TlsWrappedProtocolEnum.HTTPS)

        server_info = server_tester.perform()
    except ServerConnectivityError as e:
        results.append(AttackResult('10.16', host_name, False,  e))
        return

    plugin = CertificateInfoPlugin()
    plugin_result = plugin.process_task(server_info, CertificateInfoScanCommand())

    # Valid host name
    certificate_matches_hostname = plugin_result.certificate_matches_hostname

    # Chain order is valid
    is_certificate_chain_order_valid = plugin_result.is_certificate_chain_order_valid

    # All certificates are trusted
    certificates_are_trusted = True
    for path_validation_result in plugin_result.path_validation_result_list:
        if not path_validation_result.is_certificate_trusted:
            certificates_are_trusted = False

    result = certificate_matches_hostname and is_certificate_chain_order_valid and certificates_are_trusted

    details = ''
    if not certificate_matches_hostname:
        details += ' Certificate does not match hostname'

    if not is_certificate_chain_order_valid:
        details += ' Certificate chain order is invalid'

    if not certificates_are_trusted:
        details += ' Certificates are not trusted.'

    attackResult = None
    if not result:
        attackResult = AttackResult('hostname', host_name, result, details)
    else:
        attackResult = AttackResult('hostname', host_name, result, 'TLS certificates match hostname, are trusted and the chain order is valid')

    results.append(attackResult)

#results = []
#attack(results, 'https://www.google.co.uk')