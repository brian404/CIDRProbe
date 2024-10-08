from libc.stdlib cimport malloc, free
import socket
import ssl
import smtplib
import paramiko
import dns.resolver
import pymysql

def scan_ssh(char* ip_address, int port, char* username, char* password):
    cdef paramiko.SSHClient ssh
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip_address, port=port, username=username, password=password)
        print(f"SSH server found at {ip_address}:{port}")
    except Exception as e:
        print(f"SSH scan failed: {e}")
    finally:
        ssh.close()

def scan_ftp(char* ip_address, int port):
    cdef socket.socket ftp_socket
    ftp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ftp_socket.connect((ip_address, port))
        print(f"FTP server found at {ip_address}:{port}")
    except socket.error as e:
        print(f"FTP scan failed: {e}")
    finally:
        ftp_socket.close()

def scan_smtp(char* ip_address, int port):
    try:
        server = smtplib.SMTP(ip_address, port)
        server.ehlo()
        print(f"SMTP server found at {ip_address}:{port}")
        server.quit()
    except Exception as e:
        print(f"SMTP scan failed: {e}")

def scan_dns(char* domain):
    try:
        result = dns.resolver.resolve(domain)
        for ipval in result:
            print(f"Resolved {domain} to {ipval}")
    except Exception as e:
        print(f"DNS scan failed: {e}")

def scan_mysql(char* ip_address, int port, char* username, char* password):
    try:
        connection = pymysql.connect(host=ip_address, port=port, user=username, password=password)
        print(f"MySQL server found at {ip_address}:{port}")
        connection.close()
    except Exception as e:
        print(f"MySQL scan failed: {e}")

def scan_ntp(char* ip_address, int port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        sock.sendto(b'\x1b' + 47 * b'\0', (ip_address, port))
        data, _ = sock.recvfrom(1024)
        print(f"NTP server found at {ip_address}:{port}")
    except socket.error as e:
        print(f"NTP scan failed: {e}")
    finally:
        sock.close()

def scan_snmp(char* ip_address, int port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(b'\x30\x26\x02\x01\x01\x04\x06public\xa0\x19\x02\x04', (ip_address, port))
        data, _ = sock.recvfrom(1024)
        print(f"SNMP server found at {ip_address}:{port}")
    except socket.error as e:
        print(f"SNMP scan failed: {e}")
    finally:
        sock.close()
