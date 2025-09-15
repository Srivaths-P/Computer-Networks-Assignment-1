import os
from datetime import datetime
import socket
from scapy.all import rdpcap, DNS, DNSQR, UDP

# Some Constants: Server_ip, Server_port, input_pcap file, buffer_size
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000
PCAP_FILE = "9.pcap" 
BUFFER_SIZE = 1024

def run_client():
    """
    Reads a PCAP file, sends DNS queries to the DNS server.
    """
    log_data = []
    dns_query_id = 0

    try:
        # Read all packets from the PCAP file
        packets = rdpcap(PCAP_FILE)
    except Exception as e:
        print(f"Error: {e}")
        return

    # NOTE: Uncomment this for Debugging and basically figuring out the headers of the DNS only the queries
    # for p in packets:
    #     if (
    #         p.haslayer(DNS)
    #         and p[DNS].qr == 0
    #         and p.haslayer(UDP)
    #         and (p[UDP].sport == 53 or p[UDP].dport == 53)
    #     ):
    #         print("Packet Info: ", p)
    #         print("Packet DNS: ", p[DNS], " DNS qr: ", p[DNS].qr)

    # Filtering packets for DNS
    # Only DNS not mDNS 
    def filter_dns_only(p):
        if (
            p.haslayer(DNS)
            and p[DNS].qr == 0
            and p.haslayer(UDP)
            and (p[UDP].sport == 53 or p[UDP].dport == 53)
        ):
            return True
        return False

    dns_queries = [p for p in packets if filter_dns_only(p)]
    print(f"{len(dns_queries)} DNS queries found")

    # mDNS + DNS
    # dns_queries = [p for p in packets if p.haslayer(DNS) and p[DNS].qr == 0]
    # print(f"{len(dns_queries)} DNS queries found")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        for packet in dns_queries:
            # Creating the custom header in the formate: "HHMMSSID"
            # And adding it to the original packets

            # pick time slot (morning/afternoon/night) based on time of query
            now = datetime.now()
            time = now.strftime("%H%M%S")
            custom_header = f"{time}{dns_query_id:02d}"            
            payload = custom_header.encode('utf-8') + bytes(packet)

            # Sending the combined payload to the server
            client_socket.sendto(payload, (SERVER_IP, SERVER_PORT))

            # Waiting for a response from the server
            response, _ = client_socket.recvfrom(BUFFER_SIZE)
            ip_adrr = response.decode('utf-8')

            # Logging the data for the final report
            # qname is a byte string, so we decode it
            domain_name = packet[DNSQR].qname.decode()
            log_data.append((custom_header, domain_name, ip_adrr))
            
            print(f"DNS Query: '{domain_name}' IP Address: {ip_adrr}")
            dns_query_id += 1
    
    print(f"{'Custom Header (HHMMSSID)':<25} {'Domain Name':<35} {'Resolved IP Address':<20}")
    print("-" * 80)
    for header, domain, ip in log_data:
        print(f"{header:<25} {domain:<35} {ip:<20}")
run_client()
