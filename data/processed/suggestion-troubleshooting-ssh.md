# SSH Troubleshooting - Suggested Addition

**Target:** troubleshooting/networking.md or troubleshooting/ssh.md (new file)
**Priority:** High (critical for remote access)

---

## Scenario: Permission Denied (publickey)

**Symptoms:**
- `Permission denied (publickey)`
- `Permission denied (publickey,gssapi-keyex,gssapi-with-mic)`
- Key-based auth fails silently

**Applies to:** All distros (RHEL, Ubuntu, Debian)

### Investigation

1. **Test with verbose output**

```bash
ssh -vvv user@host
# Look for:
# - "Offering public key"
# - "Server accepts key"
# - "Authentication succeeded"
```

2. **Check client-side key permissions**

```bash
ls -la ~/.ssh/
# Required permissions:
# ~/.ssh/           700 (drwx------)
# ~/.ssh/id_rsa     600 (-rw-------)
# ~/.ssh/id_rsa.pub 644 (-rw-r--r--)
# ~/.ssh/config     600

# Fix permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
```

3. **Check server-side authorized_keys**

```bash
# On the server:
ls -la ~/.ssh/
cat ~/.ssh/authorized_keys

# Required permissions on server:
# ~                 755 or stricter (not group/world writable)
# ~/.ssh/           700
# ~/.ssh/authorized_keys  600

# Fix
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
chmod go-w ~
```

4. **Verify key is actually being offered**

```bash
ssh-add -l                          # List keys in agent
ssh-add ~/.ssh/id_rsa               # Add key to agent
```

5. **Check sshd configuration**

```bash
# On server
grep -E "^(PubkeyAuthentication|AuthorizedKeysFile|PermitRootLogin)" /etc/ssh/sshd_config

# Common issues:
# PubkeyAuthentication no          → Change to yes
# AuthorizedKeysFile wrong path    → Fix or use default
# PermitRootLogin no               → Can't SSH as root
```

6. **Check SELinux context (RHEL)**

```bash
ls -laZ ~/.ssh/
# Should show ssh_home_t or user_home_t

# Fix
restorecon -Rv ~/.ssh/
```

### Resolution

**Permission fixes (most common):**
```bash
# On client
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa ~/.ssh/config

# On server (as the user)
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
chmod go-w ~
restorecon -Rv ~/.ssh/  # RHEL only
```

**If root login needed:**
```bash
# In /etc/ssh/sshd_config
PermitRootLogin prohibit-password    # Allow key-based only
# Or (less secure):
PermitRootLogin yes
systemctl restart sshd
```

---

## Scenario: Connection Refused

**Symptoms:**
- `ssh: connect to host X port 22: Connection refused`

**Applies to:** All distros

### Investigation

```bash
# Check if sshd is running
systemctl status sshd
systemctl status ssh    # Ubuntu uses 'ssh' not 'sshd'

# Check what's listening on 22
ss -tlnp | grep :22

# Check if sshd is configured for different port
grep "^Port" /etc/ssh/sshd_config

# Check firewall
firewall-cmd --list-all  # RHEL
ufw status               # Ubuntu
iptables -L -n | grep 22
```

### Resolution

```bash
# Start/enable sshd
systemctl start sshd
systemctl enable sshd

# Open firewall
firewall-cmd --add-service=ssh --permanent && firewall-cmd --reload  # RHEL
ufw allow ssh  # Ubuntu
```

---

## Scenario: Connection Timeout

**Symptoms:**
- `ssh: connect to host X port 22: Connection timed out`
- SSH hangs without any output

**Applies to:** All distros

### Investigation

```bash
# Check connectivity
ping host
traceroute host

# Try connecting with timeout
ssh -o ConnectTimeout=5 user@host

# Check if port is filtered (not refusing, not responding)
nmap -p 22 host
# filtered = firewall dropping packets
# closed = refusing connections
# open = should work

# Check intermediate firewalls
# - Cloud security groups (AWS, GCP, Azure)
# - Corporate firewalls
# - Host-based firewall
```

### Resolution

- Check cloud security groups / network ACLs
- Check corporate firewall rules
- Try alternate ports if 22 is blocked

---

## Scenario: Host Key Changed Warning

**Symptoms:**
- `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!`
- `Host key verification failed`
- `Offending RSA key in /home/user/.ssh/known_hosts:42`

**Applies to:** All distros

### Investigation

```bash
# This happens when:
# 1. Server was reinstalled (legitimate)
# 2. Server IP changed but name didn't
# 3. Man-in-the-middle attack (verify with admin!)
```

### Resolution

**If server change is legitimate:**
```bash
# Remove old key
ssh-keygen -R hostname
ssh-keygen -R ip.address

# Or remove specific line
sed -i '42d' ~/.ssh/known_hosts

# Reconnect and accept new key
ssh user@host
```

---

## Scenario: SSH Slow to Connect

**Symptoms:**
- Long delay before password prompt
- Long delay before "Last login" message
- Connection eventually works

**Applies to:** All distros

### Investigation

```bash
# Check DNS resolution (common culprit)
ssh -o GSSAPIAuthentication=no user@host
ssh -o UseDNS=no user@host  # Won't work client-side; server setting

# Verbose to find where delay occurs
ssh -vvv user@host 2>&1 | grep -i "debug1:"
```

### Resolution

**On server, edit /etc/ssh/sshd_config:**
```bash
# Disable reverse DNS lookup
UseDNS no

# Disable GSSAPI (if not used)
GSSAPIAuthentication no

systemctl restart sshd
```

**On client, add to ~/.ssh/config:**
```
Host *
    GSSAPIAuthentication no
```

---

## Scenario: Too Many Authentication Failures

**Symptoms:**
- `Received disconnect from X: Too many authentication failures`
- Happens before you can enter password

**Applies to:** All distros

### Investigation

```bash
# You have too many keys in your agent
ssh-add -l

# SSH tries each key in order; server gives up after N attempts
```

### Resolution

```bash
# Specify exact key to use
ssh -i ~/.ssh/specific_key user@host

# Or limit identity files tried
ssh -o IdentitiesOnly=yes -i ~/.ssh/key user@host

# Or add to ~/.ssh/config
Host specifichost
    HostName host.example.com
    User username
    IdentityFile ~/.ssh/specific_key
    IdentitiesOnly yes
```

---

## Scenario: SSH Agent Forwarding Not Working

**Symptoms:**
- Can SSH to hop1
- Can't SSH from hop1 to hop2 (permission denied)
- Agent forwarding expected to work

**Applies to:** All distros

### Investigation

```bash
# On client, check agent is running
ssh-add -l

# Connect with forwarding
ssh -A user@hop1

# On hop1, verify agent socket
echo $SSH_AUTH_SOCK
ssh-add -l   # Should show keys from local machine
```

### Resolution

**On client:**
```bash
# Ensure agent is running and has keys
eval $(ssh-agent)
ssh-add ~/.ssh/id_rsa

# Enable forwarding
ssh -A user@hop1

# Or in ~/.ssh/config
Host hop1
    ForwardAgent yes
```

**On server (hop1), check sshd_config:**
```bash
# Must allow forwarding
AllowAgentForwarding yes
```
