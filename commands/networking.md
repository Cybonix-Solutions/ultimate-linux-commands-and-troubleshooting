# Networking Commands

Diagnostic and maintenance commands for time synchronization, connectivity checks, and related network services.

[⬅ Back to Main Index](README.md)

## Command: curl

**Category:** HTTP client  
**Distros:** All  
**Summary:** Transfers data to and from URLs using HTTP(S), FTP, and many other protocols.

### Common usages

```bash
curl -o article.html https://developers.redhat.com/articles/2022/01/11/5-design-principles-microservices
curl -X POST -H "Content-Type: text/plain" -d @data.txt https://example.com/api/data
```

### Tips & troubleshooting

- Use `-L` to follow redirects and `-f` to make scripts fail fast on HTTP errors.
- Uploading form data? `-F 'field=@file'` automatically sets multipart boundaries.

## Command: ip

**Category:** Interface inspection  
**Distros:** All  
**Summary:** Replaces the older `ifconfig`/`route` tools with subcommands for addresses, links, and routing tables.

### Common usages

```bash
ip addr show                                  # List interfaces with IPv4/IPv6 details
ip route                                      # Display routing table entries
```

### Tips & troubleshooting

- `ip -brief addr` offers a concise view when skimming dozens of interfaces.
- Run `ip -s link` to see RX/TX error counters while chasing NIC drops.

## Command: netstat

**Category:** Socket inspection  
**Distros:** All (net-tools package)  
**Summary:** Reports listening sockets, active connections, and the owning processes.

### Common usages

```bash
sudo netstat -anp | grep tcp                   # Show TCP sockets plus owning PIDs
netstat -rn                                    # Dump the kernel routing table
```

### Tips & troubleshooting

- Install `net-tools` on minimal RHEL/Fedora boxes (`sudo yum -y install net-tools`) when it is missing.
- Prefer `ss` for modern systems, but `netstat -plnt` is still the quickest way to spot a process bound to a port.

## Command: ntpdate

**Category:** Time sync  
**Distros:** All  
**Summary:** Queries an NTP server for the correct time (or steps the local clock when run as root).

### Common usages

```bash
ntpdate -q <server>                # Query only; does not set the clock
sudo ntpdate <server>              # Force-sync local clock immediately
```

### Tips & troubleshooting

- Inspect `/etc/ntp.conf` to confirm the servers you expect are configured; `grep -v '^#' /etc/ntp.conf` strips comments for a quick read.
- Prefer `chronyc tracking` for modern chrony deployments, but `ntpdate -q` is still handy when debugging legacy nodes.

## Command: ssh

**Category:** Remote access  
**Distros:** All  
**Summary:** Establishes encrypted sessions for shell access, file copy, or port forwarding to Linux/Unix systems.

### Common usages

```bash
ssh 192.168.86.11                              # Interactive login using default key/credentials
ssh -L 8443:localhost:8443 user@bastion        # Forward a remote port for local debugging
```

### Tips & troubleshooting

- Add `-v` (or `-vvv`) when troubleshooting handshake issues.
- Pair with `ssh-copy-id user@host` to push your public key and disable password logins later.
- When older appliances only accept legacy Diffie-Hellman KEX, add a scoped override in `/etc/ssh/ssh_config`:

```sshconfig
Host legacy-host
  KexAlgorithms +diffie-hellman-group14-sha1
```

  Use this sparingly and only for the specific hosts that require weaker algorithms.

## Command: VPN debugging workflow

**Category:** Network diagnostics
**Distros:** All
**Summary:** Quick workflow to diagnose routing and DNS behavior while connected to a VPN.

### Common usages

```bash
# Find VPN interface name (commonly tun0, wg0, ppp0)
ip link show

# Test DNS resolution while connected to VPN
nslookup teams.microsoft.com

# Find which interface routes traffic to a specific IP
ip route get 13.107.64.1

# View full routing table
ip route show

# Monitor bandwidth on VPN interface
sudo iftop -i tun0
```

### Tips & troubleshooting

- VPN interface names vary: `tun0` (OpenVPN), `wg0` (WireGuard), `ppp0` (PPTP/L2TP), `tailscale0` (Tailscale).
- Use `traceroute -n <ip>` to verify traffic path with and without VPN.
- Check for split-tunnel configuration with `ip route show table all | grep -E "(default|10\.|192\.168\.)"`.

## Command: wget

**Category:** HTTP client
**Distros:** All
**Summary:** Non-interactive downloader that can recursively fetch websites or grab single artifacts via HTTP/HTTPS/FTP.

### Common usages

```bash
wget -O article.html https://developers.redhat.com/articles/2022/01/11/5-design-principles-microservices
wget -c https://example.com/image.iso                             # Resume an interrupted download
```

### Tips & troubleshooting

- Use `--mirror --convert-links` for simple offline mirrors; throttle with `--limit-rate`.
- Combine with `--user`/`--password` or `--header` when an endpoint requires authentication headers.

## Command: dig

**Category:** DNS lookup
**Distros:** All (dnsutils on Debian/Ubuntu, bind-utils on RHEL)
**Summary:** Queries DNS servers for records with detailed output showing the full resolution path.

### Common usages

```bash
dig example.com                    # A record lookup
dig example.com MX                 # Mail server records
dig @8.8.8.8 example.com           # Query specific DNS server
dig +short example.com             # Concise output (IP only)
dig +trace example.com             # Full resolution path from root
dig -x 192.168.1.1                 # Reverse DNS lookup
dig +noall +answer example.com     # Clean output, answers only
```

### Tips & troubleshooting

- Use `+trace` to identify where resolution breaks in the chain.
- `@server` is essential for testing internal vs external DNS.
- Install: `apt install dnsutils` (Ubuntu) or `dnf install bind-utils` (RHEL).

## Command: host

**Category:** DNS lookup
**Distros:** All (dnsutils on Debian/Ubuntu, bind-utils on RHEL)
**Summary:** Simple DNS lookup utility with cleaner output than dig.

### Common usages

```bash
host example.com                   # Forward lookup
host 192.168.1.1                   # Reverse lookup
host -t mx example.com             # Specific record type
host -a example.com                # All records (verbose)
host example.com ns1.example.com   # Query specific server
```

### Tips & troubleshooting

- Simpler output than dig; good for scripts that parse results.
- Part of `bind-utils` (RHEL) or `dnsutils` (Ubuntu) package.

## Command: nslookup

**Category:** DNS lookup
**Distros:** All (dnsutils on Debian/Ubuntu, bind-utils on RHEL)
**Summary:** Interactive/non-interactive DNS queries; works identically on Windows for cross-platform familiarity.

### Common usages

```bash
nslookup example.com               # Basic lookup
nslookup example.com 8.8.8.8       # Query specific server
nslookup -type=mx example.com      # MX records
nslookup -type=txt example.com     # TXT records (SPF, DKIM)
nslookup -type=ns example.com      # Nameserver records
```

### Tips & troubleshooting

- Prefer `dig` for scripting due to more consistent output format.
- Still useful for quick interactive checks and cross-platform work.

## Command: resolvectl

**Category:** DNS management
**Distros:** Ubuntu 18.04+, RHEL 8+ (systemd-resolved systems)
**Summary:** Modern systemd DNS client for querying and managing the resolver cache.

### Common usages

```bash
resolvectl status                  # Show DNS configuration per interface
resolvectl query example.com       # Query with caching info
resolvectl flush-caches            # Clear DNS cache
resolvectl statistics              # Cache hit/miss stats
systemd-resolve --flush-caches     # Legacy command (older systems)
```

### Tips & troubleshooting

- Essential on systemd systems where `/etc/resolv.conf` points to 127.0.0.53.
- Use `resolvectl status` to see which DNS servers are actually being used.
- Cache flush is critical after DNS changes or troubleshooting.

## Command: getent

**Category:** Name service lookup
**Distros:** All
**Summary:** Queries name service switch databases including DNS, passwd, hosts, and LDAP/SSSD.

### Common usages

```bash
getent hosts example.com           # Resolve using full system config
getent ahosts example.com          # All address types (IPv4 + IPv6)
getent passwd username             # User lookup (LDAP/SSSD aware)
getent group groupname             # Group lookup
```

### Tips & troubleshooting

- Shows what the system actually resolves (includes `/etc/hosts`, LDAP, SSSD).
- Critical for troubleshooting when `dig` works but apps fail.
- Respects `/etc/nsswitch.conf` order.

## Command: traceroute

**Category:** Network diagnostics
**Distros:** All (traceroute package)
**Summary:** Traces the packet route to a destination, showing each hop and latency.

### Common usages

```bash
traceroute example.com             # ICMP trace (may need root)
traceroute -n example.com          # No DNS resolution (faster)
traceroute -T example.com          # TCP SYN trace (bypasses ICMP blocks)
traceroute -p 443 example.com      # Specific port
tracepath example.com              # No root required, includes MTU discovery
```

### Tips & troubleshooting

- `* * *` indicates ICMP blocked at that hop, not necessarily a problem.
- Use `-T` (TCP mode) when standard traceroute shows timeouts.
- `tracepath` is preferred on modern systems (no root, MTU info included).

## Command: mtr

**Category:** Network diagnostics
**Distros:** All (mtr package)
**Summary:** Combines traceroute and ping for continuous network path monitoring.

### Common usages

```bash
mtr example.com                    # Interactive mode
mtr -r example.com                 # Report mode (10 packets, then exit)
mtr -r -c 100 example.com          # 100 packets for better statistics
mtr -n example.com                 # No DNS resolution (faster)
mtr --tcp -P 443 example.com       # TCP mode on specific port
```

### Tips & troubleshooting

- Look for packet loss % at specific hops to identify problem routers.
- High latency that persists to destination = real issue.
- High latency that disappears at later hops = router deprioritizing ICMP (normal).
- Install: `apt install mtr` (Ubuntu) or `dnf install mtr` (RHEL).

## Command: ss

**Category:** Socket inspection
**Distros:** All
**Summary:** Modern replacement for netstat; displays socket statistics faster and with more filtering options.

### Common usages

```bash
ss -tuln                           # TCP/UDP listening ports (numeric)
ss -tulnp                          # Include process names (needs root)
ss -t state established            # Active TCP connections
ss -o state time-wait              # TIME_WAIT sockets with timers
ss dst 192.168.1.100               # Connections to specific IP
ss sport = :22                     # Source port 22
ss '( dport = :443 or sport = :443 )'  # Complex filters
```

### Tips & troubleshooting

- Faster than netstat on systems with many connections.
- Filter syntax is powerful: `ss -t '( dport = :80 or dport = :443 )'`.
- Add `-e` for extended info (uid, inode, memory usage).

## Command: nc (netcat)

**Category:** Network utilities
**Distros:** All (netcat-openbsd or nmap-ncat package)
**Summary:** Swiss army knife for TCP/UDP connections, port scanning, and simple data transfer.

### Common usages

```bash
nc -zv example.com 80              # Test if port is open (verbose)
nc -zv example.com 20-25           # Scan port range
nc -l 8080                         # Listen on port
nc -l 8080 < file.txt              # Serve a file
nc example.com 80 < request.txt    # Send raw HTTP request
echo "test" | nc -u example.com 53 # UDP connection
nc -w 3 example.com 22             # Timeout after 3 seconds
```

### Tips & troubleshooting

- Use `ncat` (from nmap) for SSL support: `ncat --ssl example.com 443`.
- Quick connectivity test: `nc -zv host port`.
- Useful for testing firewall rules from inside a network.

## Command: tcpdump

**Category:** Packet capture
**Distros:** All
**Summary:** Command-line packet analyzer for capturing and inspecting network traffic.

### Common usages

```bash
tcpdump -i eth0                    # Capture on interface
tcpdump -i any                     # All interfaces
tcpdump -i eth0 port 80            # Filter by port
tcpdump -i eth0 host 192.168.1.1   # Filter by host
tcpdump -i eth0 -w capture.pcap    # Write to file for Wireshark
tcpdump -r capture.pcap            # Read from file
tcpdump -i eth0 -n                 # No DNS resolution
tcpdump -i eth0 -A                 # ASCII output (see HTTP content)
tcpdump -i eth0 -X                 # Hex + ASCII
tcpdump 'tcp[tcpflags] & tcp-syn != 0'  # SYN packets only
```

### Tips & troubleshooting

- Use `-w` and analyze in Wireshark for complex issues.
- Filter syntax: `tcpdump 'src host X and dst port Y'`.
- Add `-c 100` to stop after 100 packets.
- Requires root or CAP_NET_RAW capability.

## Command: ping

**Category:** Network diagnostics
**Distros:** All
**Summary:** Tests host reachability and measures round-trip latency using ICMP echo.

### Common usages

```bash
ping -c 4 example.com              # Send 4 packets then stop
ping -i 0.2 example.com            # 200ms interval (needs root for <200ms)
ping -s 1472 -M do example.com     # MTU testing (1472 + 28 header = 1500)
ping -W 2 example.com              # 2 second timeout per packet
ping -I eth0 example.com           # Use specific interface
ping6 example.com                  # IPv6 explicit
```

### Tips & troubleshooting

- `-M do` disables fragmentation for MTU path discovery.
- ICMP may be blocked; failed ping doesn't always mean host is down.
- Use `fping` for batch testing multiple hosts simultaneously.

## Command: iftop

**Category:** Bandwidth monitoring
**Distros:** All (iftop package)
**Summary:** Real-time bandwidth usage display showing connections sorted by traffic.

### Common usages

```bash
iftop -i eth0                      # Monitor specific interface
iftop -n                           # No DNS resolution (faster)
iftop -f "port 80"                 # Filter expression
iftop -P                           # Show ports
```

### Tips & troubleshooting

- Shows connection-level traffic (who's talking to whom).
- Requires root; install from EPEL (RHEL) or standard repos (Ubuntu).
- Press `h` for help, `q` to quit.

## Command: nethogs

**Category:** Bandwidth monitoring
**Distros:** All (nethogs package)
**Summary:** Groups bandwidth usage by process, showing which application is using the network.

### Common usages

```bash
nethogs                            # Monitor all interfaces
nethogs eth0                       # Specific interface
nethogs -d 2                       # Refresh every 2 seconds
```

### Tips & troubleshooting

- Shows process-level traffic (which app is consuming bandwidth).
- Requires root.
- Install: `apt install nethogs` (Ubuntu) or `dnf install nethogs` (RHEL).
