# DNS Resolution Troubleshooting - Suggested Addition

**Target:** troubleshooting/networking.md (new file)
**Priority:** Critical

---

## Scenario: DNS Resolution Fails

**Symptoms:**
- `ping: unknown host example.com`
- `Could not resolve host`
- `Name or service not known`
- `Temporary failure in name resolution`
- Apps fail but IP addresses work

**Applies to:** All distros

### Investigation

1. **Verify DNS is the problem (not connectivity)**

```bash
# Test with IP - if this works, it's DNS
ping -c 2 8.8.8.8

# Test DNS resolution
dig example.com
nslookup example.com
host example.com
```

2. **Check system DNS configuration**

```bash
# Traditional systems
cat /etc/resolv.conf

# systemd-resolved systems (Ubuntu 18+, etc.)
resolvectl status

# Which DNS is actually being queried?
# If resolv.conf shows 127.0.0.53, use resolvectl
```

3. **Test against different DNS servers**

```bash
# Test system resolver
getent hosts example.com

# Test specific external DNS
dig @8.8.8.8 example.com
dig @1.1.1.1 example.com

# Test internal DNS server
dig @192.168.1.1 example.com
```

If external works but internal doesn't → internal DNS issue.
If external doesn't work → firewall or connectivity issue.

4. **Check if it's a specific domain**

```bash
# Test multiple domains
dig google.com +short
dig internal.corp.example +short

# Check for NXDOMAIN vs SERVFAIL
dig failing.domain
# NXDOMAIN = domain doesn't exist
# SERVFAIL = DNS server error
```

5. **Check for firewall blocking DNS**

```bash
# DNS uses UDP/TCP port 53
sudo iptables -L -n | grep 53
sudo ss -ulnp | grep :53
sudo ss -tlnp | grep :53

# Test if port 53 is reachable
nc -zvu 8.8.8.8 53
```

6. **Check systemd-resolved status**

```bash
# If using systemd-resolved
systemctl status systemd-resolved
resolvectl statistics
resolvectl flush-caches
journalctl -u systemd-resolved -n 50
```

7. **Check /etc/nsswitch.conf**

```bash
grep hosts /etc/nsswitch.conf
# Should show: hosts: files dns (or similar)
# If myhostname or mdns before dns, that could affect resolution
```

### Resolution

**Temporary fix - use specific DNS:**

```bash
# Add working DNS server temporarily
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```

**Permanent fix (systemd-resolved):**

```bash
# Edit resolved.conf
sudo nano /etc/systemd/resolved.conf
# Add:
# [Resolve]
# DNS=8.8.8.8 1.1.1.1
# FallbackDNS=8.8.4.4 1.0.0.1

sudo systemctl restart systemd-resolved
```

**Permanent fix (NetworkManager):**

```bash
# Edit connection
nmcli con modify "Connection Name" ipv4.dns "8.8.8.8 1.1.1.1"
nmcli con modify "Connection Name" ipv4.ignore-auto-dns yes
nmcli con down "Connection Name" && nmcli con up "Connection Name"
```

**If /etc/resolv.conf keeps being overwritten:**

```bash
# Check what manages it
ls -la /etc/resolv.conf

# If symlink to ../run/systemd/resolve/stub-resolv.conf
# → managed by systemd-resolved, edit resolved.conf

# If symlink to ../run/NetworkManager/resolv.conf
# → managed by NM, use nmcli

# To make manual changes stick (not recommended):
sudo chattr +i /etc/resolv.conf  # Make immutable
```

---

## Scenario: Intermittent DNS Timeouts

**Symptoms:**
- DNS works sometimes, fails other times
- `connection timed out; no servers could be reached`
- Slow name resolution

**Applies to:** All distros

### Investigation

```bash
# Test multiple times
for i in {1..10}; do dig example.com +short; sleep 1; done

# Check DNS response time
dig example.com | grep "Query time"

# Check if primary DNS is slow/unreliable
dig @$(grep nameserver /etc/resolv.conf | head -1 | awk '{print $2}') example.com

# Monitor for packet loss to DNS
mtr -rw -c 20 8.8.8.8
```

### Resolution

- Add multiple DNS servers for redundancy
- Lower timeout values in resolv.conf
- Check for network congestion to DNS server
- Consider local caching (dnsmasq, systemd-resolved)

---

## Scenario: DNS Works on CLI, Apps Fail

**Symptoms:**
- `dig` and `nslookup` work
- Applications (curl, browsers) still fail to resolve

**Applies to:** All distros

### Investigation

```bash
# Check what apps actually see
getent hosts example.com

# If getent fails but dig works → nsswitch.conf issue
# If getent works but app fails → app-specific issue

# Check nsswitch
grep hosts /etc/nsswitch.conf

# Check for /etc/hosts issues
grep example.com /etc/hosts

# Check for IPv6 issues (some apps try AAAA first)
dig example.com AAAA
```

### Resolution

- Check nsswitch.conf ordering
- Check /etc/hosts for bad entries
- Disable IPv6 if AAAA lookups are problematic:
  ```bash
  # In /etc/gai.conf, uncomment:
  precedence ::ffff:0:0/96  100
  ```
