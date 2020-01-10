from sslyze.ssl_settings import TlsWrappedProtocolEnum
from sslyze.plugins.certificate_info_plugin import CertificateInfoPlugin, CertificateInfoScanCommand
from sslyze.server_connectivity_tester import ServerConnectivityTester, ServerConnectivityError
from utils.AttackResult import AttackResult


"""
This attack verifies the hashing algorithms of the certificates in the certificate chain.
"""


def execute(results, hosts):
    for host in hosts:
        attack(results, host)


def certificate_common_name(certificate):
    subject = certificate.subject
    for relative_distinguished_name in subject.rdns:
        name_attribute = relative_distinguished_name
        for attribute in name_attribute:
            if attribute.oid._name == 'commonName':
                return attribute.value


def is_signing_signatures_valid(signatures):
    strong_signing_algorith = 'sha256WithRSAEncryption'
    for signature in signatures:
        if signature != strong_signing_algorith:
            return False

    return True


def attack(results, host_name):
    print("Running 10.15 attack.py host name: {}".format(host_name))
    report = {}

    try:
        server_tester = ServerConnectivityTester(
            hostname=host_name,
            port=443,
            tls_wrapped_protocol=TlsWrappedProtocolEnum.HTTPS)

        server_info = server_tester.perform()
    except ServerConnectivityError as e:
        results.append(AttackResult('10.15', host_name, False, e))
        return

    plugin = CertificateInfoPlugin()
    plugin_result = plugin.process_task(server_info, CertificateInfoScanCommand())

    error_strings = []
    signing_algorithms = []
    verified_certificate_chain = plugin_result.verified_certificate_chain
    for index, certificate in enumerate(verified_certificate_chain):
        signing_algorithms.append(certificate.signature_algorithm_oid._name)
        error_strings.append('Index: {} Name: {} Algorithm {}'
            .format(index, certificate_common_name(certificate), certificate.signature_algorithm_oid._name))

    result = None
    if not is_signing_signatures_valid(signing_algorithms):
        result = AttackResult('certificate_chain', host_name, False, 'The certificate chain is invalid ' + str(error_strings))
    else:
        result = AttackResult('certificate_chain', host_name, True, 'The certificate chain is valid')

    results.append(result)
    return
