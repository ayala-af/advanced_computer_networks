import sys
from dig_caa import dig_caa
from dns_map import dns_map
DNS_TOOLKIT = "1.1.1.1"


def main():
    """
     Main function to execute the DNS mapping.
     """
    if len(sys.argv) != 2 or sys.argv[0] != "dnstoolkit.py":
        print("ILLEGAL COMMAND")
        return
    domain = sys.argv[1]
    print("DIG-CAA\n")
    dig_caa(domain,DNS_TOOLKIT)

    print("\nDNS_MAP\n")
    dns_map(domain,DNS_TOOLKIT)


if __name__ == '__main__':
    main()