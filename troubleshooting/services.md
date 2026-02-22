# Service Troubleshooting Runbooks

Investigations for systemd service failures, startup issues, and dependency problems.

[⬅ Back to Main Index](README.md)

## Scenario: Service Fails to Start

**Symptoms:** `systemctl start service` exits without error but service isn't running; `Job for X.service failed`; `Active: failed (Result: exit-code)`.
**Applies to:** All systemd distros (RHEL 7+, Ubuntu 16.04+, Debian 8+).

### Investigation

1. Get detailed status and recent logs:

```bash
systemctl status nginx -l
journalctl -u nginx -n 50 --no-pager
journalctl -u nginx -xe
```

2. Check exit code:

```bash
systemctl show nginx -p ExecMainStatus
# 0 = success, 1 = general error, 126 = permission, 127 = not found
```

3. Check configuration syntax:

```bash
# Most services have a config test option
nginx -t
httpd -t                           # Apache on RHEL
apache2ctl configtest              # Apache on Ubuntu
sshd -t
named-checkconf
postfix check
```

4. Check file permissions:

```bash
# Does service user exist?
id nginx

# Can it access its files?
namei -l /var/log/nginx/error.log
namei -l /etc/nginx/nginx.conf
ls -la /var/run/nginx/
```

5. Run manually to see errors:

```bash
# Find the ExecStart command
systemctl cat nginx | grep ExecStart

# Run it directly
sudo -u nginx /usr/sbin/nginx -g 'daemon off;'
```

6. Check resource limits:

```bash
systemctl show nginx -p LimitNOFILE,LimitNPROC,MemoryLimit
```

7. Check port conflicts:

```bash
ss -tlnp | grep :80
lsof -i :80
```

8. Check SELinux (RHEL) or AppArmor (Ubuntu):

```bash
# RHEL SELinux
getenforce
ausearch -m avc -ts recent

# Ubuntu AppArmor
aa-status
journalctl -k | grep apparmor
```

### Resolution

**Permission fixes:**

```bash
chown -R nginx:nginx /var/log/nginx
chmod 755 /var/log/nginx
restorecon -Rv /var/log/nginx      # RHEL SELinux only
```

**Port conflict:**

```bash
fuser -k 80/tcp                    # Kill process on port 80
# Or change service port in config
```

**Missing dependencies:**

```bash
systemctl list-dependencies nginx
systemctl start required-service
```

## Scenario: Service Starts But Stops Immediately

**Symptoms:** Service shows "active" briefly then "failed"; health check fails; main process exits quickly.
**Applies to:** All systemd distros.

### Investigation

```bash
# Watch the service in real-time
journalctl -fu nginx

# In another terminal, start the service
systemctl start nginx

# Check for watchdog timeouts
journalctl -u nginx | grep -i timeout
```

Common causes: config error, old PID file exists, socket in use, dependency not ready, OOM killed.

### Resolution

**PID file issues:**

```bash
rm /var/run/nginx.pid
systemctl start nginx
```

**Increase startup timeout:**

```bash
# Create override: /etc/systemd/system/nginx.service.d/override.conf
[Service]
TimeoutStartSec=90

systemctl daemon-reload
systemctl start nginx
```

**Add startup delay for dependencies:**

```bash
# In service override
[Service]
ExecStartPre=/bin/sleep 5
```

## Scenario: Service Running But Not Responding

**Symptoms:** `systemctl status` shows active (running); service doesn't respond to requests; no errors in logs.
**Applies to:** All distros.

### Investigation

```bash
# Check if actually listening
curl -v http://localhost/
nc -zv localhost 80

# Check process state
ps aux | grep nginx
cat /proc/$(pgrep -o nginx)/status | grep State
# D = uninterruptible sleep (I/O wait)
# Z = zombie
# T = stopped

# Check file descriptors
ls -la /proc/$(pgrep -o nginx)/fd/ | wc -l

# Check if process is blocked
strace -p $(pgrep -o nginx) -f
```

### Resolution

- Increase file descriptor limits if exhausted.
- Check disk I/O if process is in D state.
- Check downstream dependencies (database, etc.).

## Scenario: Cannot Stop Service

**Symptoms:** `systemctl stop` hangs; service stuck in "deactivating"; process won't die.
**Applies to:** All systemd distros.

### Investigation

```bash
systemctl cat nginx | grep ExecStop
ps aux | grep nginx
cat /proc/$(pgrep nginx)/status | grep State
```

### Resolution

```bash
# Increase timeout
systemctl stop nginx --timeout=120

# Force kill if stuck
systemctl kill nginx
systemctl kill -s SIGKILL nginx

# Reset failed state
systemctl reset-failed nginx

# Nuclear option
pkill -9 nginx
systemctl daemon-reload
systemctl start nginx
```

## Scenario: Dependency Chain Failures

**Symptoms:** Service fails because dependency failed; `Requires=other.service` not running.
**Applies to:** All systemd distros.

### Investigation

```bash
# View dependency tree
systemctl list-dependencies nginx
systemctl list-dependencies --reverse nginx

# Check failed units
systemctl list-units --failed

# Check if dependencies are running
systemctl list-dependencies nginx --plain | xargs -I {} systemctl is-active {}
```

### Resolution

```bash
# Start dependencies first
systemctl start network.target
systemctl start nginx

# Or change Requires= to Wants= for optional dependency in unit file
# Add After= for ordering without hard requirement
```
