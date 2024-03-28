
## Description:
This repository contains various Python scripts implementing different networking functionalities.

### 1. DNS Toolkit:
- **Overview**: A toolkit for DNS research and enumeration.
- **Features**:
  1. Querying CAA records.
  2. DNS enumeration using dnsmap.
  3. WHOIS protocol query.(Will be added in the near future)
- **Usage**:
  - Execute `dns_toolkit.py <domain>` to perform DNS toolkit operations.
    
### 2. Secure Socket Implementation:
- **Overview**: Implements encryption, key exchange, hashing, and message authentication using Python.
- **Encryption Mechanisms**:
  1. Symmetric encryption based on XOR.
  2. Diffie-Hellman key exchange for shared encryption key.
  3. Hashing function for message integrity.
  4. RSA for creating MAC using public key.
- **Usage**:
  - Execute `server.py` & `client.py` to establish encrypted communication between server and client.
 
### 3. Multiclient Chat Application:
- **Overview**: Provides a client-server chat system supporting multiple users. Includes server, client, and protocol files.
- **Commands Supported**:
  - `NAME <name>`: Set client name.
  - `GET_NAMES`: Get all connected client names.
  - `MSG <NAME> <message>`: Send message to a specific client.
  - `EXIT`: Close the client.
- **Usage**:
  - Run `chat_server.py` to start the server.
  - Run `chat_client1.py` to connect as the first client.
  - Run `chat_client2.py` to connect as the second client(optional).

### 4. NSLOOKUP Implementation:
- **Overview**: Implements NSLOOKUP functionality using Scapy, providing DNS resolution capabilities.
- **Features**:
  - Resolves domain name to IP address.
  - Supports both forward and reverse mapping.
- **Usage**:
  - Execute `nslookup.py nslookup -type=A <domain>` to resolve the IP address of the specified domain.
  - Execute`nslookup.py nslookup -type=PTR <IP Addr>`  for reverse mapping.

    
### 5. SMTP Client and Server Implementation:
- **Overview**: Implements an SMTP client and server system using only socket and base64 libraries, adhering to the SMTP protocol.
- **Features**:
  - Follows SMTP protocol as recorded in Wireshark record.
- **Usage**: 
  - Execute `smtp_server.py` to run the server.
  - Execute `smtp_client.py` to run the client.
### 



## Instructions:
1. Clone this repository to your local machine.
2. Navigate to the directory of each project.
3. Follow the specific instructions provided in each project's README file.

Feel free to contribute or report any issues encountered with the scripts.
