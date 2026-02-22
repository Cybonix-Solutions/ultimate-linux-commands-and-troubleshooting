# Firewall Commands - Suggested Addition

**Target:** commands/networking.md or commands/firewall.md (new file)
**Priority:** Critical (essential for both RHEL and Ubuntu)

---

## firewalld (RHEL/CentOS/Fedora)

Default firewall on RHEL 7+ and Fedora.

```bash
# Service control
systemctl status firewalld
systemctl start firewalld
systemctl enable firewalld

# Check status
firewall-cmd --state
firewall-cmd --get-active-zones
firewall-cmd --list-all                    # Current zone config
firewall-cmd --list-all --zone=public

# Allow service (predefined)
firewall-cmd --add-service=http --permanent
firewall-cmd --add-service=https --permanent
firewall-cmd --list-services

# Allow port
firewall-cmd --add-port=8080/tcp --permanent
firewall-cmd --add-port=5000-5100/tcp --permanent
firewall-cmd --list-ports

# Remove rules
firewall-cmd --remove-service=http --permanent
firewall-cmd --remove-port=8080/tcp --permanent

# Apply changes
firewall-cmd --reload

# Rich rules (complex rules)
firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" accept' --permanent
firewall-cmd --add-rich-rule='rule family="ipv4" source address="10.0.0.1" port port="22" protocol="tcp" accept' --permanent

# Port forwarding
firewall-cmd --add-forward-port=port=80:proto=tcp:toport=8080 --permanent

# Zone management
firewall-cmd --get-zones
firewall-cmd --set-default-zone=work
firewall-cmd --zone=internal --add-interface=eth1 --permanent

# Debug/troubleshoot
firewall-cmd --get-default-zone
firewall-cmd --info-zone=public
```

**Tips:**
- Always use `--permanent` then `--reload`, or rule is lost on reboot
- Without `--permanent`, changes are temporary (good for testing)
- Default zone is `public`; use `firewall-cmd --list-all` to see what's allowed

**Distros:** RHEL 7+, CentOS 7+, Fedora, Rocky, AlmaLinux

---

## ufw (Ubuntu/Debian)

Uncomplicated Firewall - default on Ubuntu.

```bash
# Service control
sudo ufw status
sudo ufw status verbose
sudo ufw status numbered
sudo ufw enable
sudo ufw disable

# Allow services
sudo ufw allow ssh                          # Allows 22/tcp
sudo ufw allow http                         # Allows 80/tcp
sudo ufw allow https                        # Allows 443/tcp
sudo ufw allow 'Nginx Full'                 # App profile

# Allow ports
sudo ufw allow 8080/tcp
sudo ufw allow 8080                         # Both TCP and UDP
sudo ufw allow 5000:5100/tcp                # Port range

# Allow from specific IP
sudo ufw allow from 192.168.1.0/24
sudo ufw allow from 192.168.1.100 to any port 22
sudo ufw allow from 10.0.0.0/8 to any port 3306

# Deny rules
sudo ufw deny 23                            # Deny telnet
sudo ufw deny from 10.0.0.5

# Delete rules
sudo ufw delete allow 8080/tcp
sudo ufw delete 3                           # Delete by number (use status numbered)

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Logging
sudo ufw logging on
sudo ufw logging medium                     # low/medium/high/full

# Reset all rules
sudo ufw reset

# App profiles
sudo ufw app list
sudo ufw app info 'OpenSSH'
```

**Tips:**
- Run `ufw enable` after setting rules; it persists across reboots
- Use `ufw status numbered` to see rule numbers for deletion
- Check `/etc/ufw/applications.d/` for app profiles

**Distros:** Ubuntu, Debian, Linux Mint

---

## iptables (All distros - legacy/advanced)

Low-level netfilter interface. Works everywhere but complex.

```bash
# List rules
iptables -L -n -v                           # Verbose with numbers
iptables -L -n --line-numbers               # With rule numbers
iptables -t nat -L -n -v                    # NAT table

# Allow incoming port
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow from specific IP
iptables -A INPUT -s 192.168.1.0/24 -j ACCEPT
iptables -A INPUT -s 10.0.0.100 -p tcp --dport 22 -j ACCEPT

# Allow established connections (important!)
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT

# Drop all other incoming
iptables -A INPUT -j DROP

# Delete rule by number
iptables -D INPUT 3

# Delete rule by specification
iptables -D INPUT -p tcp --dport 8080 -j ACCEPT

# Flush all rules (danger!)
iptables -F

# Save rules
# RHEL/CentOS:
service iptables save
# Or:
iptables-save > /etc/sysconfig/iptables

# Ubuntu/Debian:
iptables-save > /etc/iptables/rules.v4
# Install iptables-persistent for auto-restore

# Restore rules
iptables-restore < /etc/sysconfig/iptables
```

**Tips:**
- Rules are processed in order; first match wins
- Always allow ESTABLISHED,RELATED before restrictive rules
- iptables rules don't persist by default; must save explicitly
- Use `iptables -I INPUT 1` to insert at top instead of append

**Distros:** All (but prefer firewalld on RHEL, ufw on Ubuntu)

---

## nftables (Modern replacement)

Successor to iptables, default on newer systems.

```bash
# List rules
nft list ruleset
nft list tables
nft list table inet filter

# Add table and chain
nft add table inet filter
nft add chain inet filter input { type filter hook input priority 0 \; }

# Add rules
nft add rule inet filter input tcp dport 80 accept
nft add rule inet filter input tcp dport 443 accept
nft add rule inet filter input ct state established,related accept

# Delete rule (by handle)
nft -a list ruleset                          # Show handles
nft delete rule inet filter input handle 5

# Save/restore
nft list ruleset > /etc/nftables.conf
nft -f /etc/nftables.conf

# Flush
nft flush ruleset
```

**Tips:**
- Syntax is more consistent than iptables
- firewalld uses nftables as backend on modern RHEL
- Check `/etc/nftables.conf` for persistent rules

**Distros:** RHEL 8+, Debian 10+, Ubuntu 20.04+ (as alternative)
