#Ayala Aftergut
import sys
from scapy.layers.inet import IP, UDP
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.all import *


def dns_a_query(domain_name):
    """MAKE A DNS A QUERY"""
    return IP(dst="8.8.8.8") / UDP(sport=24601, dport=53) / DNS(qdcount=1, rd=1, qd=DNSQR(qname=domain_name))


def dns_ptr_query(ip_address):
    """MAKE A DNS PTR QUERY"""
    return IP(dst="8.8.8.8") / UDP(sport=24601, dport=53) / DNS(rd=1, opcode=0, qd=DNSQR(qname=(ip_address + ".in-addr.arpa"),  qtype="PTR", qclass="IN"))


def reverse_ip(ip):
    """REVERSE AN IP ADDRESS"""
    ip = ip.split(".")
    ip.reverse()
    ip = ".".join(ip)
    return ip


def main():
    if len(sys.argv) != 4 or sys.argv[1] != "nslookup":
        print("ILLEGAL COMMAND")
        return
    if sys.argv[2] == "-type=PTR":
        """PTR"""
        response_packet = sr1(dns_ptr_query(reverse_ip(sys.argv[3])), verbose=0)
        if response_packet.aa == 0:
            print("Non-authoritative answer:")
        else:
            print("An-authoritative answer:")
        if response_packet and DNS in response_packet and response_packet[DNS].ancount > 0:
            for x in range(response_packet[DNS].ancount):
                if response_packet[DNSRR][x].type == 12:
                    print(reverse_ip(sys.argv[3]) + ".in-addr.arpa              "+"DOMAIN NAME: " + str(response_packet[DNSRR][x].rdata.decode()))
    elif sys.argv[2] == "-type=A":
        """A"""
        response_packet = sr1(dns_a_query(sys.argv[3]), verbose=0)
        if response_packet.aa == 0:
            print("Non-authoritative answer:")
        else:
            print("An-authoritative answer:")

        print("Addresses:")
        if response_packet and DNS in response_packet and response_packet[DNS].ancount > 0:
            for x in range(response_packet[DNS].ancount):
                if response_packet[DNSRR][x].type == 1:  # Check if the record type is A
                    print("IP: " + str(response_packet[DNSRR][x].rdata))
                if response_packet[DNSRR][x].type == 5:  # Check if the record type is CNAME
                    print("Name: " + str(response_packet[DNSRR][x].rdata.decode()))
                    print("Aliases " + str(response_packet[DNSRR][x].rrname.decode()))
    else:
        print("ILLEGAL COMMAND")
        return


if __name__ == '__main__':
    main()
