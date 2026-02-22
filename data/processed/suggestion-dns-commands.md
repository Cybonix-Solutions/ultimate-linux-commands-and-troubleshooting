# DNS Commands - Suggested Addition

**Target:** commands/networking.md
**Priority:** Critical (DNS troubleshooting is daily work)

---

## dig

Query DNS records with detailed output.

```bash
dig example.com                    # A record lookup
dig example.com MX                 # Mail server records
dig @8.8.8.8 example.com           # Query specific DNS server
dig +short example.com             # Concise output (IP only)
dig +trace example.com             # Full resolution path from root
dig -x 192.168.1.1                 # Reverse DNS lookup
dig example.com ANY                # All record types (often blocked)
dig +noall +answer example.com     # Clean output, answers only
```

**Tips:**
- Use `+trace` to identify where resolution breaks in the chain
- `@server` is essential for testing internal vs external DNS
- Install via `dnsutils` (Debian) or `bind-utils` (RHEL)

---

## nslookup

Interactive/non-interactive DNS queries (legacy but ubiquitous).

```bash
nslookup example.com               # Basic lookup
nslookup example.com 8.8.8.8       # Query specific server
nslookup -type=mx example.com      # MX records
nslookup -type=txt example.com     # TXT records (SPF, DKIM)
nslookup -type=ns example.com      # Nameserver records
```

**Tips:**
- Prefer `dig` for scripting (more consistent output)
- Still useful for quick interactive checks
- Works identically on Windows (cross-platform skill)

---

## host

Simple DNS lookup utility.

```bash
host example.com                   # Forward lookup
host 192.168.1.1                   # Reverse lookup
host -t mx example.com             # Specific record type
host -a example.com                # All records (verbose)
host example.com ns1.example.com   # Query specific server
```

**Tips:**
- Simpler output than dig, good for scripts
- Part of `bind-utils` / `dnsutils` package

---

## resolvectl / systemd-resolve

Modern systemd DNS client and cache management.

```bash
resolvectl status                  # Show DNS configuration per interface
resolvectl query example.com       # Query with caching info
resolvectl flush-caches            # Clear DNS cache
resolvectl statistics              # Cache hit/miss stats
systemd-resolve --flush-caches     # Legacy command (older systems)
```

**Tips:**
- Essential on systemd systems where /etc/resolv.conf points to 127.0.0.53
- Use `resolvectl status` to see which DNS servers are actually being used
- Cache flush is critical after DNS changes

---

## getent

Query name service switch databases (DNS, passwd, hosts, etc.).

```bash
getent hosts example.com           # Resolve using system config (not just DNS)
getent ahosts example.com          # All address types (IPv4 + IPv6)
getent passwd username             # User lookup (LDAP/SSSD aware)
getent group groupname             # Group lookup
```

**Tips:**
- Shows what the system actually resolves (includes /etc/hosts, LDAP, etc.)
- Critical for troubleshooting when `dig` works but apps fail
- Respects nsswitch.conf order
