# Task 2

Wireshark was used on both Windows and Linux and we used traceroute/tracert for www.google.com.

On Windows, we filtered using `(udp and not quic and not dns) or icmp`.
On Linux, we filtered using `icmp`.


## **1. What protocol does Windows tracert use by default, and what protocol does Linux traceroute use by default?**

### Linux

Linux (`traceroute`) by default uses UDP for its outgoing probe packets and receives ICMP messages in response.

The packet capture shows the source (`10.7.18.102`) sending UDP packets. The replies from the intermediate routers are ICMP Time-to-live exceeded messages.

```
No.  Time        Source          Destination     Protocol Length Info
--------------------------------------------------------------------------------------------------
7    0.532204100   10.7.18.102     142.251.42.228  UDP      74     52502 → 33434 Len=32  <-- Outgoing UDP Probe
...
23   0.535223592   172.16.4.7      10.7.18.102     ICMP     102    Time-to-live exceeded <-- Incoming ICMP Reply
```

The outgoing packets are identified as UDP and the responses are ICMP.

### Windows

Windows (`tracert`) by default uses ICMP for its outgoing probe packets and receives ICMP messages in response.

The packet capture shows the source (`10.7.18.102`) sending ICMP Echo (ping) request packets. The replies from intermediate routers are also ICMP Time-to-live exceeded messages.

```
No.  Time        Source          Destination     Protocol Length Info
--------------------------------------------------------------------------------------------------
4    2.996132    10.7.18.102     142.250.71.100  ICMP     106    Echo (ping) request ... ttl=1 <-- Outgoing ICMP Probe
5    2.997731    10.7.0.5        10.7.18.102     ICMP     70     Time-to-live exceeded         <-- Incoming ICMP Reply
```

Both the outgoing probe and the incoming replies are ICMP packets.

## **2. Some hops in your traceroute output may show `* * *`. Provide at least two reasons why a router might not reply.**

The `* * *` indicates that no reply was received for a probe within the timeout period.

1. Firewall / Access Control List (ACL): The router may be explicitly configured to drop the incoming probe packets (UDP for Linux, ICMP for Windows). It may also be configured to not generate or send the `ICMP Time-to-live exceeded` error message as a security measure to prevent network reconnaissance.

2. ICMP Rate Limiting: A router's main job is to forward traffic, not generate error messages. To protect its CPU from being overwhelmed (e.g., during a denial-of-service attack), a router will often limit the rate at which it sends ICMP error messages. If `traceroute` sends probes too quickly or if the router is busy, it may simply drop the packet instead of sending a reply, resulting in a timeout.

## **3. In Linux traceroute, which field in the probe packets changes between successive probes sent to the destination?**

When using `traceroute`, the **UDP Destination Port** number is incremented for each successive probe packet.

```
No.  Time        Source          Destination     Protocol Length Info
--------------------------------------------------------------------------------------------------
7    0.532204100   10.7.18.102     142.251.42.228  UDP      74     52502 → 33434 Len=32
8    0.532220723   10.7.18.102     142.251.42.228  UDP      74     51841 → 33435 Len=32
9    0.532229769   10.7.18.102     142.251.42.228  UDP      74     50390 → 33436 Len=32
...
```

The destination port starts at 33434 and is incremented by one each time.

## **4. At the final hop, how is the response different compared to the intermediate hop?**

#### Linux:

Intermediate hops reply with an **ICMP "Time-to-live exceeded"** message. The final destination host replies with an **ICMP "Destination unreachable (Port unreachable)"** message.

*   Intermediate Hop Reply:
    ```
    No.  Time        Source          Destination     Protocol Length Info
    --------------------------------------------------------------------------------------------------
    68   0.555401023   72.14.204.62     10.7.18.102     ICMP     102    Time-to-live exceeded (Time to live exceeded in transit)
    ```
*   Final Hop Reply:
    ```
    No.  Time        Source          Destination     Protocol Length Info
    --------------------------------------------------------------------------------------------------
    102  0.594741855   142.251.42.228  10.7.18.102     ICMP     70     Destination unreachable (Port unreachable)
    ```

#### **Windows**

Intermediate hops reply with an **ICMP "Time-to-live exceeded"** message. The final destination host, upon receiving the ICMP Echo Request, successfully processes it and replies with a corresponding **ICMP "Echo (ping) reply"** message.

*   Intermediate Hop Reply:
    ```
    No.  Time        Source          Destination     Protocol Length Info
    --------------------------------------------------------------------------------------------------
    126  14.515126   14.139.98.1     10.7.18.102     ICMP     70     Time-to-live exceeded (Time to live exceeded in transit)
    ```
*   Final Hop Reply:
    ```
    No.  Time        Source          Destination     Protocol Length Info
    --------------------------------------------------------------------------------------------------
    845  59.207813   142.250.71.100  10.7.18.102     ICMP     106    Echo (ping) reply    id=0x0001, seq=64/16384
    ```

***

## **5. Suppose a firewall blocks UDP traffic but allows ICMP. How would this affect the results of Linux traceroute vs. Windows tracert?**

*   Linux `traceroute`: It would stop working. The outgoing UDP probe packets would be dropped by the firewall. The `traceroute` command would not be able to go beyond the firewall and would time out, showing `* * *` for all subsequent hops.

*   Windows `tracert`: Nothing would be affected. Since `tracert` uses ICMP Echo Requests for its probes, and the firewall allows ICMP, the probes would pass through. The incoming ICMP `Time-to-live exceeded` and `Echo reply` messages would also be allowed, so the entire route to the destination would be mapped successfully.

NOTE: Linux `traceroute` can be forced to use ICMP probes with the `-I` flag (e.g., `traceroute -I www.google.com`).
