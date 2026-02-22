# Network Troubleshooting Runbooks

Investigations for DNS resolution, connectivity issues, and network diagnostics.

[⬅ Back to Main Index](README.md)

## Scenario: DNS Resolution Fails

**Symptoms:** `ping: unknown host`, `Could not resolve host`, `Name or service not known`, `Temporary failure in name resolution`, apps fail but IP addresses work.
**Applies to:** Ubuntu, RHEL, Debian, all systemd-based distros.

### Investigation

1. Verify DNS is the problem (not connectivity):

```bash
ping -c 2 8.8.8.8                  # If this works, it's DNS
dig example.com
nslookup example.com
host example.com
```

2. Check system DNS configuration:

```bash
# Traditional systems
cat /etc/resolv.conf

# systemd-resolved systems (Ubuntu 18+, RHEL 8+)
resolvectl status

# If resolv.conf shows 127.0.0.53, system uses systemd-resolved
```

3. Test against different DNS servers:

```bash
# Test system resolver
getent hosts example.com

# Test external DNS directly
dig @8.8.8.8 example.com
dig @1.1.1.1 example.com

# Test internal DNS
dig @192.168.1.1 example.com
```

If external works but internal doesn't → internal DNS server issue.
If external doesn't work → firewall or connectivity issue.

4. Check for firewall blocking DNS (port 53):

```bash
# Check firewall rules
sudo iptables -L -n | grep 53
ss -ulnp | grep :53

# Test if port 53 is reachable
nc -zvu 8.8.8.8 53
```

5. Check systemd-resolved status:

```bash
systemctl status systemd-resolved
resolvectl statistics
resolvectl flush-caches
journalctl -u systemd-resolved -n 50
```

6. Check nsswitch configuration:

```bash
grep hosts /etc/nsswitch.conf
# Should show: hosts: files dns (or similar)
```

### Resolution

**Temporary fix - use specific DNS:**

```bash
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```

**Permanent fix (systemd-resolved on Ubuntu/RHEL 8+):**

```bash
sudo nano /etc/systemd/resolved.conf
# Add:
# [Resolve]
# DNS=8.8.8.8 1.1.1.1
# FallbackDNS=8.8.4.4 1.0.0.1

sudo systemctl restart systemd-resolved
```

**Permanent fix (NetworkManager on RHEL/Ubuntu):**

```bash
nmcli con modify "Connection Name" ipv4.dns "8.8.8.8 1.1.1.1"
nmcli con modify "Connection Name" ipv4.ignore-auto-dns yes
nmcli con down "Connection Name" && nmcli con up "Connection Name"
```

**If /etc/resolv.conf keeps being overwritten:**

```bash
ls -la /etc/resolv.conf
# Symlink to ../run/systemd/resolve/stub-resolv.conf → edit resolved.conf
# Symlink to ../run/NetworkManager/resolv.conf → use nmcli
```

## Scenario: Intermittent DNS Timeouts

**Symptoms:** DNS works sometimes, fails other times; `connection timed out; no servers could be reached`; slow name resolution.
**Applies to:** All distros.

### Investigation

```bash
# Test multiple times
for i in {1..10}; do dig example.com +short; sleep 1; done

# Check DNS response time
dig example.com | grep "Query time"

# Monitor for packet loss to DNS
mtr -rw -c 20 8.8.8.8
```

### Resolution

- Add multiple DNS servers for redundancy.
- Check for network congestion to DNS server.
- Consider local caching (systemd-resolved, dnsmasq).

## Scenario: DNS Works in CLI But Apps Fail

**Symptoms:** `dig` and `nslookup` work; applications (curl, browsers) fail to resolve.
**Applies to:** All distros.

### Investigation

```bash
# Check what apps actually see
getent hosts example.com

# If getent fails but dig works → nsswitch.conf issue
# If getent works but app fails → app-specific issue

# Check nsswitch order
grep hosts /etc/nsswitch.conf

# Check /etc/hosts for bad entries
grep example.com /etc/hosts

# Check for IPv6 issues (some apps try AAAA first)
dig example.com AAAA
```

### Resolution

- Check nsswitch.conf ordering (`files dns` is typical).
- Check `/etc/hosts` for incorrect entries.
- Disable IPv6 preference if AAAA lookups are problematic:

```bash
# In /etc/gai.conf, uncomment:
precedence ::ffff:0:0/96  100
```
