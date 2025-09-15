# Task 1: DNS Client-Serer Model

This project demonstrates a DNS client–server system using Python sockets and `scapy`.  

The client reads DNS queries from a PCAP file, adds a custom header, and sends them to the server.  

The server acts as a load-balancer and responds with an IP address chosen from a predefined pool of IP addresses.

## How to Run

### 1. Prerequisites
* Python 3 installed
* `pip` installed

### 2. Clone the Repository
```bash
git clone https://github.com/Srivaths-P/Computer-Networks-Assignment-1.git
cd Computer-Networks-Assignment-1
```

### 3. Create & Activate a Virtual Environment (Recommended)
Create a virtual environment named .venv:

Windows
```bash
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
```

Linux / macOS
``` bash
    python3 -m venv .venv
    source .venv/bin/activate
```


You should now see (.venv) in your terminal prompt.

### 4. Install Dependencies
Inside the activated environment:

```bash
pip install scapy
```

### 5. Place the PCAP File
Copy your PCAP file (e.g., 9.pcap) into the project directory so that client.py can read it.

### 6. Run the Server and Client
Open two terminal windows/tabs.

Terminal 1 – Start the server

```bash
python server.py
```

You should see:

```nginx
DNS Server listening on 127.0.0.1:5000
```

Terminal 2 – Run the client

```bash
python client.py
```

The client reads the PCAP, sends DNS queries to the server, and displays a summary table. (This may take a few minutes so please be patient)

### 7. Deactivate the Virtual Environment
When finished:

```bash
deactivate
```
