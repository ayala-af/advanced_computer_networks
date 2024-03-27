# Ayala Aftergut
import sys
from scapy.layers.inet import IP, UDP
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.all import *
DNS_MAP = "1.1.1.1"


def dns_a_query(domain_name, dns_server = DNS_MAP):
    """
     Creates a DNS query packet of type A for the specified domain.

     Parameters:
         domain_name (str): The domain name being queried.

     Returns:
         DNS query packet of type A.
     """
    return IP(dst=dns_server) / UDP(sport=24601, dport=53) / DNS(qdcount=1, rd=1, qd=DNSQR(qname=domain_name))


def dns_map(domain,dns_server = DNS_MAP):
    """
     Performs mapping of subdomains for a given domain and searches for the corresponding IP addresses using DNS queries.

     Parameters:
         domain (str): The domain for which the mapping of subdomains is performed.

     Prints:
         - IP addresses found for each subdomain.
         - Total number of subdomains.
         - Total number of IP addresses found.
     """
    with open(r'C:\Users\User\Downloads\wordlist_TLAs.txt', 'r') as source_file:
        line = source_file.readline().split("\n")[0]
        sum_sub_domain = 0
        sum_ip = 0
        while line:
            new_domain = line.strip() + "." + domain
            line = source_file.readline()

            response_packet = sr1(dns_a_query(new_domain,dns_server),  timeout=5,verbose=0)

            if response_packet and DNS in response_packet and response_packet[DNS].ancount > 0:
                print(new_domain)
                sum_sub_domain = sum_sub_domain+1
                index = 1
                for x in range(response_packet[DNS].ancount):
                    if response_packet[DNSRR][x].type == 1:  # Check if the record type is A
                        print("IP address #"+str(index)+":" + str(response_packet[DNSRR][x].rdata))
                        index = index + 1
                        sum_ip = sum_ip + 1
                    if response_packet[DNSRR][x].type == 28:
                        print(response_packet.show())
                        index = index + 1
                       # sum_ip = sum_ip + 1

        print("\n" + str(sum_sub_domain) + "(sub)domains")
        print("and" + str(sum_ip) + "IP address(es) found")


def main():
    """
     Main function to execute the DNS mapping.
     """
    if len(sys.argv) != 2 or sys.argv[0] != "dns_map.py":
        print("ILLEGAL COMMAND")
        return
    domain = sys.argv[1]
    #domain = "jct.ac.il"
    dns_map(domain,DNS_MAP)

    print("\n end")


if __name__ == '__main__':
    main()
