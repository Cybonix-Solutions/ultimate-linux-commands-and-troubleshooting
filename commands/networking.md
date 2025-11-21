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
