# Service Failure Troubleshooting - Suggested Addition

**Target:** troubleshooting/services.md (new file)
**Priority:** Critical

---

## Scenario: Service Fails to Start

**Symptoms:**
- `systemctl start service` exits without error but service isn't running
- `Job for X.service failed because the control process exited with error code`
- Service starts then immediately stops
- `Active: failed (Result: exit-code)`

**Applies to:** All systemd distros (RHEL 7+, Ubuntu 16+, Debian 8+)

### Investigation

1. **Get detailed status and recent logs**

```bash
systemctl status nginx -l
journalctl -u nginx -n 50 --no-pager
journalctl -u nginx -xe
```

2. **Check exit code**

```bash
systemctl show nginx -p ExecMainStatus
# 0 = success, non-zero = error
# Common codes: 1=general error, 2=misuse, 126=permission, 127=not found
```

3. **Check configuration syntax**

```bash
# Most services have a config test option
nginx -t
httpd -t
named-checkconf
sshd -t
postfix check
```

4. **Check file permissions**

```bash
# Does service user exist?
id nginx

# Can it access its files?
namei -l /var/log/nginx/error.log
namei -l /etc/nginx/nginx.conf
ls -la /var/run/nginx/

# Check if directories exist
ls -la /var/log/nginx/
ls -la /var/lib/nginx/
```

5. **Run manually to see errors**

```bash
# Find the ExecStart command
systemctl cat nginx | grep ExecStart

# Run it directly (with same user if possible)
sudo -u nginx /usr/sbin/nginx -g 'daemon off;'
```

6. **Check resource limits**

```bash
# Service-specific limits
systemctl show nginx -p LimitNOFILE,LimitNPROC,MemoryLimit

# System limits
ulimit -a
cat /proc/sys/fs/file-max
```

7. **Check port conflicts**

```bash
ss -tlnp | grep :80
lsof -i :80
# Is something else using the port?
```

8. **Check SELinux/AppArmor**

```bash
# SELinux
getenforce
ausearch -m avc -ts recent
sealert -a /var/log/audit/audit.log

# AppArmor
aa-status
dmesg | grep apparmor
journalctl -k | grep apparmor
```

### Resolution

**Missing dependencies:**
```bash
# Check requires
systemctl list-dependencies nginx

# Start dependencies
systemctl start nginx.socket  # if socket-activated
```

**Permission fixes:**
```bash
chown -R nginx:nginx /var/log/nginx
chmod 755 /var/log/nginx
restorecon -Rv /var/log/nginx  # SELinux
```

**Port conflict:**
```bash
# Find and stop conflicting service
fuser -k 80/tcp  # Kill process on port 80
# Or change the service's port in config
```

---

## Scenario: Service Starts But Stops Immediately

**Symptoms:**
- Service shows "active" briefly then "failed"
- Health check fails
- Main process exits with code

**Applies to:** All systemd distros

### Investigation

```bash
# Watch the service in real-time
journalctl -fu nginx

# In another terminal, start the service
systemctl start nginx

# Check for watchdog timeouts
journalctl -u nginx | grep -i timeout
journalctl -u nginx | grep -i watchdog
```

Common causes:
- Config error causes immediate exit
- PID file issues (old PID file exists)
- Socket already in use
- Dependency not ready yet
- OOM killed

### Resolution

**PID file issues:**
```bash
rm /var/run/nginx.pid
systemctl start nginx
```

**Increase startup timeout:**
```bash
# In /etc/systemd/system/nginx.service.d/override.conf
[Service]
TimeoutStartSec=90
```

**Add startup delay for dependencies:**
```bash
# In service override
[Service]
ExecStartPre=/bin/sleep 5
```

---

## Scenario: Service Running But Not Responding

**Symptoms:**
- `systemctl status` shows active (running)
- Service doesn't respond to requests
- No errors in logs

**Applies to:** All distros

### Investigation

```bash
# Check if process is actually responding
curl -v http://localhost/
nc -zv localhost 80

# Check process state
ps aux | grep nginx
cat /proc/$(pgrep -o nginx)/status | grep State
# D = uninterruptible sleep (usually I/O wait)
# Z = zombie
# T = stopped

# Check file descriptors
ls -la /proc/$(pgrep -o nginx)/fd/ | wc -l
cat /proc/$(pgrep -o nginx)/limits | grep "open files"

# Check if process is blocked
strace -p $(pgrep -o nginx) -f
```

### Resolution

- Increase file descriptor limits if exhausted
- Check disk I/O if process is in D state
- Investigate deadlocks if process is stuck
- Check downstream dependencies (database, etc.)

---

## Scenario: Cannot Stop Service

**Symptoms:**
- `systemctl stop` hangs
- Service stuck in "deactivating"
- Process won't die

**Applies to:** All systemd distros

### Investigation

```bash
# Check what stop command does
systemctl cat nginx | grep ExecStop

# Check process state
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

---

## Scenario: Dependency Chain Failures

**Symptoms:**
- Service fails because dependency failed
- `Requires=other.service` failed
- Circular dependency errors

**Applies to:** All systemd distros

### Investigation

```bash
# View dependency tree
systemctl list-dependencies nginx
systemctl list-dependencies --reverse nginx

# Check if dependencies are running
systemctl list-dependencies nginx --plain | xargs -I {} systemctl is-active {}

# Check for failed units
systemctl list-units --failed
```

### Resolution

```bash
# Start dependencies first
systemctl start network.target
systemctl start nginx

# Or fix dependency in unit file
# Change Requires= to Wants= for optional dependency
# Add After= for ordering without hard requirement
```
