# Ayala Aftergut
from scapy.layers.inet import IP, UDP
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.all import *

DNS_DIG = "1.1.1.1"


def dns_caa_query(domain_name, dns_server = DNS_DIG):
    """
     Creates a DNS query packet of type CAA for the specified domain.

     Parameters:
         domain_name (str): The domain name being queried.

     Returns:
         DNS query packet of type CAA.
     """
    return IP(dst=dns_server) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=domain_name, qtype="CAA"))


def dig_caa(domain, dns_server = DNS_DIG):
    """
       Send a DNS query to retrieve CAA records for a domain and print the response.

       Parameters:
           domain (str): The domain for which CAA records are to be retrieved.
           dns_server (str): The DNS server to send the query to. Default is "8.8.8.8".

       Returns:
           list: List of CAA records found in the DNS response.
       """
    start_time = datetime.now().timestamp() * 1000  # Combine into one call

    # Create a new DNS request packet
    # Send the packet and get the response
    response = sr1(dns_caa_query(domain,dns_server), timeout=5,verbose=0)

    if response and response.haslayer(DNS):
        print_dns_response(response, dns_server, start_time)

        # Extract and return the CAA records
        caa_records = [answer for answer in response[DNS].an if answer.type == 257]
        return caa_records


def print_dns_response(response, dns_server, start_time):
    """
    Print the DNS response packet details.

    Parameters:
        response (scapy.packet): DNS response packet.
        dns_server (str): The DNS server that responded to the query.
        start_time (float): Timestamp when the query was initiated.
    """
    # Opcode dictionary and name retrieval
    opcode_names = {
        0: "QUERY",
        1: "IQUERY",
        2: "STATUS",
        4: "NOTIFY",
        5: "UPDATE"
    }
    opcode_name = opcode_names.get(response.opcode, f"Unknown ({response.opcode})")

    # Calculate query time
    end_time = datetime.now().timestamp() * 1000
    query_time = int(end_time - start_time)

    # Print the header
    print(";; Got answer:\n")

    print(";; ->>HEADER<<- opcode:", opcode_name, ", status:", response.rcode, ", id:", response.id)
    print(";; flags:", " qr:", response.qr, " rd:", response.rd, " ad:", response.ad)
    print(";; QUERY:", response.qdcount, ", ANSWER:", response.ancount, ", AUTHORITY:", response.nscount, ", "
                                                                                                          "ADDITIONAL:", response.arcount)
    if not response.rd and response.ra:
        print(";; WARNING: recursion requested but not available")

    # Print the question section
    print(f"\n;; QUESTION SECTION:")
    print(f"; {response.qd.qname.decode()} \t\t IN \t {response.qd.qtype}")

    # Print the answer section
    print("\n;; ANSWER SECTION:")
    for ans in range(response[DNS].ancount):
        answer = response[DNSRR][ans]
        if answer.type == 257:
            rrname = answer.rrname.decode("utf-8")
            ttl = answer.ttl
            type_str = str(answer.type)

            # Decode rdata, handle potential empty or malformed data
            try:
                # Extract flags and issuer
                flag1 = answer.rdata[0]
                flag2 = answer.rdata[1]
                issuer = answer.rdata[2:].decode("utf-8")

                # Convert flags to binary string
                decimal_value1 = int(str(flag1), 16)
                decimal_value2 = int(str(flag2), 16)
                isu = issuer[0:decimal_value2]
                ca = issuer[decimal_value2:]

                # Print flags and issuer
                print(f"{rrname}\t\t{ttl}\tIN\t\t{type_str}\t\t{decimal_value1 }\t{isu}  {ca}")

            except (IndexError, UnicodeDecodeError):
                # Default to "N/A" if decoding or splitting fails
                print(f"{rrname}\t\t{ttl}\tIN\t\t{type_str}\t\tN/A")

    # Print the remaining information
    print("\n;; Query time:", query_time, "msec")
    print(";; SERVER:", dns_server, "#53(", dns_server, ") (UDP)")
    print(";; WHEN:", datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y"))
    print(";; MSG SIZE  rcvd:", len(response))


def main():
    """
        Main function to execute the DNS mapping.
        """
    if len(sys.argv) != 2 or sys.argv[0] != "dig_caa.py":
        print("ILLEGAL COMMAND")
        return

    domain = sys.argv[1]
    dig_caa(domain,DNS_DIG)
    #domain = "github.com"
    # domain = "jct.ac.il"


if __name__ == "__main__":
    main()

