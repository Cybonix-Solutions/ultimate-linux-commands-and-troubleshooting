# Network Diagnostic Commands - Suggested Addition

**Target:** commands/networking.md
**Priority:** Critical

---

## traceroute / tracepath

Trace packet route to destination.

```bash
traceroute example.com             # ICMP trace (may need root)
traceroute -n example.com          # No DNS resolution (faster)
traceroute -T example.com          # TCP SYN trace (bypasses ICMP blocks)
traceroute -p 443 example.com      # Specific port
tracepath example.com              # No root required, MTU discovery
```

**Tips:**
- `* * *` indicates ICMP blocked, not necessarily a problem
- Use `-T` when standard traceroute shows timeouts
- `tracepath` is preferred on modern systems (no root, MTU info)

---

## mtr

Combines traceroute + ping for continuous monitoring.

```bash
mtr example.com                    # Interactive mode
mtr -r example.com                 # Report mode (10 packets, then exit)
mtr -r -c 100 example.com          # 100 packets for better stats
mtr -n example.com                 # No DNS (faster)
mtr --tcp -P 443 example.com       # TCP mode on specific port
```

**Tips:**
- Look for packet loss % at specific hops to identify problem routers
- High latency that persists to destination = real issue
- High latency that disappears = router deprioritizing ICMP (normal)

---

## ss

Modern socket statistics (replaces netstat).

```bash
ss -tuln                           # TCP/UDP listening ports (numeric)
ss -tulnp                          # Include process names (needs root)
ss -t state established            # Active TCP connections
ss -o state time-wait              # TIME_WAIT sockets with timers
ss dst 192.168.1.100               # Connections to specific IP
ss sport = :22                     # Source port 22
ss '( dport = :443 or sport = :443 )' # Complex filters
```

**Tips:**
- Faster than netstat on systems with many connections
- Filter syntax is powerful: `ss -t '( dport = :80 or dport = :443 )'`
- Add `-e` for extended info (uid, inode)

---

## nc / netcat

Swiss army knife for TCP/UDP connections.

```bash
nc -zv example.com 80              # Port scan (verbose)
nc -zv example.com 20-25           # Port range
nc -l 8080                         # Listen on port
nc -l 8080 < file.txt              # Serve a file
nc example.com 80 < request.txt    # Send raw HTTP
echo "test" | nc -u example.com 53 # UDP connection
nc -w 3 example.com 22             # Timeout after 3 seconds
```

**Tips:**
- Use `ncat` (from nmap) for SSL support: `ncat --ssl example.com 443`
- Quick connectivity test: `nc -zv host port`
- Useful for testing firewall rules

---

## tcpdump

Packet capture and analysis.

```bash
tcpdump -i eth0                    # Capture on interface
tcpdump -i any                     # All interfaces
tcpdump -i eth0 port 80            # Filter by port
tcpdump -i eth0 host 192.168.1.1   # Filter by host
tcpdump -i eth0 -w capture.pcap    # Write to file
tcpdump -r capture.pcap            # Read from file
tcpdump -i eth0 -n                 # No DNS resolution
tcpdump -i eth0 -A                 # ASCII output (see HTTP)
tcpdump -i eth0 -X                 # Hex + ASCII
tcpdump 'tcp[tcpflags] & tcp-syn != 0' # SYN packets only
```

**Tips:**
- Use `-w` and analyze in Wireshark for complex issues
- Filter syntax: `tcpdump 'src host X and dst port Y'`
- Add `-c 100` to stop after 100 packets

---

## ping

Test host reachability and latency.

```bash
ping -c 4 example.com              # 4 packets then stop
ping -i 0.2 example.com            # 200ms interval (needs root for <200ms)
ping -s 1472 -M do example.com     # MTU testing (1472 + 28 = 1500)
ping -W 2 example.com              # 2 second timeout
ping -I eth0 example.com           # Specific interface
ping6 example.com                  # IPv6 explicit
```

**Tips:**
- `-M do` disables fragmentation for MTU discovery
- ICMP may be blocked; failed ping doesn't mean host is down
- Use `fping` for batch testing multiple hosts

---

## iftop / nethogs

Real-time bandwidth monitoring.

```bash
iftop -i eth0                      # Bandwidth by connection
iftop -n                           # No DNS resolution
iftop -f "port 80"                 # Filter expression
nethogs                            # Bandwidth by process
nethogs eth0                       # Specific interface
```

**Tips:**
- `iftop` shows connection-level traffic (who's talking to whom)
- `nethogs` shows process-level traffic (which app is using bandwidth)
- Both need root; install from EPEL (RHEL) or standard repos (Debian)
