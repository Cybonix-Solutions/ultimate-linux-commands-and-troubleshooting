# Firewall Commands

Commands for managing host-based firewalls across different Linux distributions.

[⬅ Back to Main Index](README.md)

## Command: firewall-cmd

**Category:** Firewall management
**Distros:** RHEL 7+, CentOS 7+, Fedora, Rocky, AlmaLinux
**Summary:** CLI for firewalld, the default dynamic firewall on RHEL-based systems.

### Common usages

```bash
# Status checks
firewall-cmd --state                           # Check if firewalld is running
firewall-cmd --get-active-zones                # Show active zones and interfaces
firewall-cmd --list-all                        # List all rules in default zone
firewall-cmd --list-all --zone=public          # List rules for specific zone

# Allow services
firewall-cmd --add-service=http --permanent    # Allow HTTP
firewall-cmd --add-service=https --permanent   # Allow HTTPS
firewall-cmd --add-service=ssh --permanent     # Allow SSH
firewall-cmd --list-services                   # List allowed services

# Allow ports
firewall-cmd --add-port=8080/tcp --permanent   # Allow TCP port 8080
firewall-cmd --add-port=5000-5100/tcp --permanent  # Allow port range
firewall-cmd --list-ports                      # List allowed ports

# Remove rules
firewall-cmd --remove-service=http --permanent
firewall-cmd --remove-port=8080/tcp --permanent

# Apply changes
firewall-cmd --reload                          # Reload to apply permanent rules

# Rich rules for complex scenarios
firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" accept' --permanent
firewall-cmd --add-rich-rule='rule family="ipv4" source address="10.0.0.1" port port="22" protocol="tcp" accept' --permanent

# Port forwarding
firewall-cmd --add-forward-port=port=80:proto=tcp:toport=8080 --permanent

# Zone management
firewall-cmd --get-zones
firewall-cmd --set-default-zone=work
firewall-cmd --zone=internal --add-interface=eth1 --permanent
```

### Tips & troubleshooting

- Always use `--permanent` then `--reload`, or rule is lost on reboot.
- Without `--permanent`, changes are temporary (good for testing).
- Default zone is `public`; use `firewall-cmd --get-default-zone` to verify.
- To start firewalld: `systemctl enable --now firewalld`.

## Command: ufw

**Category:** Firewall management
**Distros:** Ubuntu, Debian, Linux Mint
**Summary:** Uncomplicated Firewall provides a user-friendly interface to iptables.

### Common usages

```bash
# Status and control
sudo ufw status                    # Show firewall status
sudo ufw status verbose            # Detailed status with defaults
sudo ufw status numbered           # Show rules with numbers (for deletion)
sudo ufw enable                    # Enable firewall
sudo ufw disable                   # Disable firewall

# Allow services
sudo ufw allow ssh                 # Allow SSH (port 22)
sudo ufw allow http                # Allow HTTP (port 80)
sudo ufw allow https               # Allow HTTPS (port 443)
sudo ufw allow 'Nginx Full'        # Allow by app profile name

# Allow ports
sudo ufw allow 8080/tcp            # Allow TCP port 8080
sudo ufw allow 8080                # Allow both TCP and UDP
sudo ufw allow 5000:5100/tcp       # Allow port range

# Allow from specific IP
sudo ufw allow from 192.168.1.0/24
sudo ufw allow from 192.168.1.100 to any port 22
sudo ufw allow from 10.0.0.0/8 to any port 3306

# Deny rules
sudo ufw deny 23                   # Deny telnet
sudo ufw deny from 10.0.0.5

# Delete rules
sudo ufw delete allow 8080/tcp
sudo ufw delete 3                  # Delete by rule number

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Logging and reset
sudo ufw logging on
sudo ufw logging medium            # low/medium/high/full
sudo ufw reset                     # Reset all rules

# App profiles
sudo ufw app list                  # List available app profiles
sudo ufw app info 'OpenSSH'        # Show profile details
```

### Tips & troubleshooting

- Run `ufw enable` after setting rules; configuration persists across reboots.
- Use `ufw status numbered` to see rule numbers for deletion.
- App profiles are in `/etc/ufw/applications.d/`.
- UFW is a frontend to iptables; both can coexist but may conflict.

## Command: iptables

**Category:** Firewall management
**Distros:** All (low-level, legacy on modern systems)
**Summary:** Direct interface to the kernel's netfilter firewall framework.

### Common usages

```bash
# List rules
iptables -L -n -v                  # List all rules with packet counts
iptables -L -n --line-numbers      # Show rule numbers
iptables -t nat -L -n -v           # List NAT table rules

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

# Delete rules
iptables -D INPUT 3                # Delete rule by number
iptables -D INPUT -p tcp --dport 8080 -j ACCEPT  # Delete by spec

# Flush all rules (danger!)
iptables -F

# Save rules (RHEL/CentOS)
service iptables save
# Or:
iptables-save > /etc/sysconfig/iptables

# Save rules (Ubuntu/Debian)
iptables-save > /etc/iptables/rules.v4
# Install iptables-persistent for auto-restore

# Restore rules
iptables-restore < /etc/sysconfig/iptables
```

### Tips & troubleshooting

- Rules are processed in order; first match wins.
- Always allow ESTABLISHED,RELATED before restrictive rules.
- Rules don't persist by default; must save explicitly or use a persistence tool.
- Use `iptables -I INPUT 1` to insert at top instead of append.
- Prefer firewalld (RHEL) or ufw (Ubuntu) for easier management.

## Command: nft

**Category:** Firewall management
**Distros:** RHEL 8+, Debian 10+, Ubuntu 20.04+ (modern replacement for iptables)
**Summary:** nftables is the successor to iptables with cleaner syntax and better performance.

### Common usages

```bash
# List rules
nft list ruleset                   # Show all rules
nft list tables                    # List tables
nft list table inet filter         # Show specific table

# Add table and chain
nft add table inet filter
nft add chain inet filter input { type filter hook input priority 0 \; }

# Add rules
nft add rule inet filter input tcp dport 80 accept
nft add rule inet filter input tcp dport 443 accept
nft add rule inet filter input ct state established,related accept

# Delete rule (by handle)
nft -a list ruleset                # Show handles
nft delete rule inet filter input handle 5

# Save and restore
nft list ruleset > /etc/nftables.conf
nft -f /etc/nftables.conf

# Flush all rules
nft flush ruleset
```

### Tips & troubleshooting

- Syntax is more consistent than iptables.
- firewalld uses nftables as backend on RHEL 8+.
- Check `/etc/nftables.conf` for persistent rules.
- To enable: `systemctl enable --now nftables`.
