# SSH Troubleshooting Runbooks

Investigations for SSH connection failures, authentication issues, and key problems.

[⬅ Back to Main Index](README.md)

## Scenario: Permission Denied (publickey)

**Symptoms:** `Permission denied (publickey)`; key-based auth fails silently; can't connect even with correct key.
**Applies to:** All distros.

### Investigation

1. Test with verbose output:

```bash
ssh -vvv user@host
# Look for:
# - "Offering public key"
# - "Server accepts key"
# - "Authentication succeeded"
```

2. Check client-side key permissions:

```bash
ls -la ~/.ssh/
# Required permissions:
# ~/.ssh/           drwx------ (700)
# ~/.ssh/id_rsa     -rw------- (600)
# ~/.ssh/id_rsa.pub -rw-r--r-- (644)
# ~/.ssh/config     -rw------- (600)
```

3. Check server-side authorized_keys:

```bash
# On the server:
ls -la ~/.ssh/
cat ~/.ssh/authorized_keys

# Required permissions:
# ~                 755 or stricter (not group/world writable)
# ~/.ssh/           700
# ~/.ssh/authorized_keys  600
```

4. Verify key is being offered:

```bash
ssh-add -l                         # List keys in agent
ssh-add ~/.ssh/id_rsa              # Add key to agent
```

5. Check sshd configuration (on server):

```bash
grep -E "^(PubkeyAuthentication|AuthorizedKeysFile|PermitRootLogin)" /etc/ssh/sshd_config

# Common issues:
# PubkeyAuthentication no   → Change to yes
# PermitRootLogin no        → Can't SSH as root
```

6. Check SELinux context (RHEL):

```bash
ls -laZ ~/.ssh/
restorecon -Rv ~/.ssh/
```

### Resolution

**Permission fixes (most common):**

```bash
# On client
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa ~/.ssh/config

# On server (as the connecting user)
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
chmod go-w ~
restorecon -Rv ~/.ssh/             # RHEL only
```

**If root login needed:**

```bash
# In /etc/ssh/sshd_config
PermitRootLogin prohibit-password  # Allow key-based only

# RHEL
systemctl restart sshd

# Ubuntu
systemctl restart ssh
```

## Scenario: Connection Refused

**Symptoms:** `ssh: connect to host X port 22: Connection refused`.
**Applies to:** All distros.

### Investigation

```bash
# Check if sshd is running
systemctl status sshd              # RHEL
systemctl status ssh               # Ubuntu

# Check what's listening on 22
ss -tlnp | grep :22

# Check if sshd uses a different port
grep "^Port" /etc/ssh/sshd_config

# Check firewall
firewall-cmd --list-all            # RHEL
ufw status                         # Ubuntu
iptables -L -n | grep 22
```

### Resolution

```bash
# Start/enable sshd
systemctl start sshd && systemctl enable sshd   # RHEL
systemctl start ssh && systemctl enable ssh     # Ubuntu

# Open firewall
firewall-cmd --add-service=ssh --permanent && firewall-cmd --reload  # RHEL
ufw allow ssh                                                          # Ubuntu
```

## Scenario: Connection Timeout

**Symptoms:** `ssh: connect to host X port 22: Connection timed out`; SSH hangs without output.
**Applies to:** All distros.

### Investigation

```bash
# Check connectivity
ping host
traceroute host

# Try with timeout
ssh -o ConnectTimeout=5 user@host

# Check if port is filtered
nmap -p 22 host
# filtered = firewall dropping packets
# closed = refusing
# open = should work
```

### Resolution

- Check cloud security groups / network ACLs.
- Check corporate firewall rules.
- Try alternate port if 22 is blocked.

## Scenario: Host Key Changed Warning

**Symptoms:** `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!`; `Host key verification failed`.
**Applies to:** All distros.

### Investigation

This happens when: server was reinstalled, IP changed but name didn't, or (rarely) man-in-the-middle attack.

### Resolution

**If server change is legitimate:**

```bash
# Remove old key
ssh-keygen -R hostname
ssh-keygen -R ip.address

# Or remove specific line shown in error
sed -i '42d' ~/.ssh/known_hosts

# Reconnect and accept new key
ssh user@host
```

## Scenario: SSH Slow to Connect

**Symptoms:** Long delay before password prompt; long delay before "Last login" message.
**Applies to:** All distros.

### Investigation

```bash
# Check if GSSAPI is the culprit
ssh -o GSSAPIAuthentication=no user@host

# Verbose to find where delay occurs
ssh -vvv user@host 2>&1 | grep "debug1:"
```

### Resolution

**On server, edit /etc/ssh/sshd_config:**

```bash
UseDNS no
GSSAPIAuthentication no

# RHEL
systemctl restart sshd

# Ubuntu
systemctl restart ssh
```

**On client, add to ~/.ssh/config:**

```
Host *
    GSSAPIAuthentication no
```

## Scenario: Too Many Authentication Failures

**Symptoms:** `Received disconnect from X: Too many authentication failures`; happens before password prompt.
**Applies to:** All distros.

### Investigation

```bash
# You have too many keys in your agent
ssh-add -l
# SSH tries each key; server gives up after N attempts
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

## Scenario: SSH Agent Forwarding Not Working

**Symptoms:** Can SSH to hop1; can't SSH from hop1 to hop2; agent forwarding expected to work.
**Applies to:** All distros.

### Investigation

```bash
# On client, check agent is running
ssh-add -l

# Connect with forwarding
ssh -A user@hop1

# On hop1, verify agent socket exists
echo $SSH_AUTH_SOCK
ssh-add -l                         # Should show keys from local machine
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
