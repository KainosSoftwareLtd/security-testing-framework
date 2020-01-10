from sslyze.ssl_settings import TlsWrappedProtocolEnum
from sslyze.server_connectivity_tester import ServerConnectivityTester, ServerConnectivityError
from sslyze.plugins.openssl_cipher_suites_plugin import Tlsv13ScanCommand, Tlsv12ScanCommand, \
    Tlsv11ScanCommand, Tlsv10ScanCommand, Sslv30ScanCommand, Sslv20ScanCommand
from sslyze.synchronous_scanner import SynchronousScanner
from utils.AttackResult import AttackResult


"""
This attack verifies the use of ciphers that use perfect forward secrecy.
This means that recorded historic TLS conversations cannot be decrypted, if the server's private key is discovered.
Elliptic Curve Diffie Hellman Ephemeral (ECDHE) supports perfect forward secrecy.
"""


def execute(results, hosts):
    for host in hosts:
        attack_host(results, host)


def cipher_list_to_string_list(cipher_list):
    cipher_names = []
    for cipher in cipher_list:
        cipher_names.append(cipher.name)
    return cipher_names


def list_equal(list1, list2):
    return set(list1) == set(list2)


def attack_host(results, host_name):
    print("Running forward_secrecy_attack.py host name: {}".format(host_name))
    expected_tls1_2_suites = ['TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384', 'TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256']

    try:
        server_tester = ServerConnectivityTester(
            hostname=host_name,
            port=443,
            tls_wrapped_protocol=TlsWrappedProtocolEnum.HTTPS)

        server_info = server_tester.perform()
    except ServerConnectivityError as e:
        results.append(AttackResult('10.13', host_name, False, e))
        return

    synchronous_scanner = SynchronousScanner()

    tls1_3_scan_result = synchronous_scanner.run_scan_command(server_info, Tlsv13ScanCommand())
    tls1_3_accepted_ciphers = tls1_3_scan_result.accepted_cipher_list

    tls1_2_scan_result = synchronous_scanner.run_scan_command(server_info, Tlsv12ScanCommand())
    tls1_2_accepted_ciphers = tls1_2_scan_result.accepted_cipher_list
    tls1_2_accepted_cipher_names = cipher_list_to_string_list(tls1_2_accepted_ciphers)

    tls1_1_scan_result = synchronous_scanner.run_scan_command(server_info, Tlsv11ScanCommand())
    tls1_1_accepted_ciphers = tls1_1_scan_result.accepted_cipher_list

    tls1_0_scan_result = synchronous_scanner.run_scan_command(server_info, Tlsv10ScanCommand())
    tls1_0_accepted_ciphers = tls1_0_scan_result.accepted_cipher_list

    ssl3_0_scan_result = synchronous_scanner.run_scan_command(server_info, Sslv30ScanCommand())
    ssl3_0_accepted_ciphers = ssl3_0_scan_result.accepted_cipher_list

    ssl2_0_scan_result = synchronous_scanner.run_scan_command(server_info, Sslv20ScanCommand())
    ssl2_0_accepted_ciphers = ssl2_0_scan_result.accepted_cipher_list

    # Determine result
    result = list_equal(tls1_2_accepted_cipher_names, expected_tls1_2_suites) and \
        len(tls1_3_accepted_ciphers) == 0 and \
        len(tls1_1_accepted_ciphers) == 0 and \
        len(tls1_0_accepted_ciphers) == 0 and \
        len(ssl3_0_accepted_ciphers) == 0 and \
        len(ssl3_0_accepted_ciphers) == 0

    # Build details
    details = ''
    if len(tls1_3_accepted_ciphers) != 0:
        details += 'TLS 1.3 should not be supported '

    if not list_equal(tls1_2_accepted_cipher_names, expected_tls1_2_suites):
        details += ' TLS 1.2 supporting ' + str(tls1_2_accepted_cipher_names) \
                   + ', should only be ' + str(expected_tls1_2_suites) + ' '

    if len(tls1_1_accepted_ciphers) != 0:
        details += 'TLS 1.1 should not be supported '

    if len(tls1_0_accepted_ciphers) != 0:
        details += 'TLS 1.0 should not be supported '

    if len(ssl3_0_accepted_ciphers) != 0:
        details += 'SSL 3.0 should not be supported '

    if len(ssl2_0_accepted_ciphers) != 0:
        details += 'SSL 2.0 should not be supported '

    if details == '':
        details = 'Cipher suites are correct'

    results.append(AttackResult('forward_secrecy', host_name, result, details))


# attack_host([], 'google.co.uk')