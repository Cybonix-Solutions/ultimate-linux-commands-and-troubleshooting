# Ubuntu 24.04 — Runaway Syslog Growth: Diagnosis & Prevention

**Platform:** Ubuntu 24.04 LTS  
**Applies to:** Workstations and servers running rsyslog, Docker, SSSD, and/or YubiKey/MFA  
**Severity:** High — syslog.1 files in excess of 100GB have been observed  

---

## Overview

Under certain conditions, `/var/log/syslog.1` can grow to extreme sizes (100GB+) in a short period of time. This is almost always caused by a process logging at an abnormally high rate, combined with logrotate failing to cap the damage. This article covers the most common root causes, diagnostic steps, and hardening measures to prevent recurrence.

---

## Common Root Causes

### 1. SSSD Debug Level Left Elevated

On domain-joined systems with SSSD, a `debug_level` value left at `7`, `8`, or `9` (often from a prior troubleshooting session) will generate millions of log lines per hour. This is the **most likely culprit** on YubiKey/MFA-configured machines.

### 2. Docker Container Using the syslog Logging Driver

Docker's default logging driver (`json-file`) does not feed into syslog. However, if the daemon or individual containers are configured to use the `syslog` driver, every line of container stdout/stderr hits syslog. A misbehaving container in a crash loop will produce catastrophic output.

### 3. Web/App Service with Verbose Error Logging to syslog

If a web service or application is configured to route logs through syslog rather than its own log file, repeated errors or debug output can flood the log rapidly.

### 4. rsyslog Feedback Loop

A misconfigured rsyslog can log its own messages back to itself, creating an exponential feedback loop.

### 5. Kernel/udev Hardware Spam

Flaky hardware (e.g., a YubiKey being repeatedly detected/disconnected, a misbehaving USB device) can cause the kernel to emit continuous udev messages into syslog.

---

## Diagnostic Commands

> **Note:** If the file has already been removed, focus on the prevention steps below. If the file still exists, use these commands to identify the source without loading the full file into memory.

```bash
# Sample the end of the log without opening the full file
sudo tail -n 100 /var/log/syslog.1

# Identify the top logging sources by process name
sudo grep -oP '^\S+ \S+ \S+' /var/log/syslog.1 | sort | uniq -c | sort -rn | head -20

# Check what has been logging most heavily in the last hour
sudo journalctl --since "1 hour ago" | awk '{print $5}' | sort | uniq -c | sort -rn | head -20

# Monitor live log rate (lines per second)
sudo tail -f /var/log/syslog | pv -l -i 5 > /dev/null
```

---

## Prevention Steps

### Step 1 — Check SSSD Debug Level

```bash
grep -i debug_level /etc/sssd/sssd.conf
grep -rn debug_level /etc/sssd/conf.d/
```

Any value above `2` is chatty in production. Set it to `1` or `2` across all `[domain/...]` and `[sssd]` sections, then restart the service:

```bash
sudo systemctl restart sssd
```

**Recommended production setting:**

```ini
[sssd]
debug_level = 1

[domain/yourdomain.com]
debug_level = 1
```

---

### Step 2 — Audit Docker Logging Configuration

Check what logging driver is active at the daemon and container level:

```bash
# Check daemon-level driver
cat /etc/docker/daemon.json | grep -i log

# Check per-container logging drivers
docker inspect $(docker ps -q) --format '{{.Name}}: {{.HostConfig.LogConfig.Type}}'
```

If any containers are using the `syslog` driver, switch them to `json-file` with size limits. Edit or create `/etc/docker/daemon.json`:

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "50m",
    "max-file": "3"
  }
}
```

Restart the Docker daemon after making changes:

```bash
sudo systemctl restart docker
```

---

### Step 3 — Harden logrotate with a Size Cap

Even if a log flood occurs, logrotate should limit the blast radius. Check the current configuration:

```bash
cat /etc/logrotate.d/rsyslog
```

Add or update the configuration to include a `size` directive, which forces rotation before the file grows uncontrollably regardless of the daily schedule:

```
/var/log/syslog
/var/log/syslog.1
{
    rotate 4
    daily
    missingok
    notifempty
    compress
    delaycompress
    sharedscripts
    size 500M
    postrotate
        /usr/lib/rsyslog/rsyslog-rotate
    endscript
}
```

Test logrotate config for syntax errors:

```bash
sudo logrotate --debug /etc/logrotate.d/rsyslog
```

---

### Step 4 — Enable rsyslog Rate Limiting

Add a global rate limit to rsyslog to prevent any single process from flooding the log:

```bash
sudo nano /etc/rsyslog.conf
```

Add or verify the following lines near the top of the file:

```
# Rate limiting — max 200 messages per 5 seconds per process
$SystemLogRateLimitInterval 5
$SystemLogRateLimitBurst 200
```

Restart rsyslog to apply:

```bash
sudo systemctl restart rsyslog
```

---

### Step 5 — Add a Size Alert via Cron

A lightweight cron job that fires an alert when syslog exceeds a threshold provides early warning before files reach problematic sizes.

```bash
sudo crontab -e
```

**If mail is configured:**

```bash
*/30 * * * * find /var/log -name "syslog*" -size +1G -exec echo "WARNING: {} is oversized on $(hostname)" \; | mail -s "Syslog size alert" admin@yourdomain.com 2>/dev/null
```

**If mail is not configured (log to file instead):**

```bash
*/30 * * * * find /var/log -name "syslog*" -size +1G -exec echo "$(date) WARNING: {} is oversized on $(hostname)" \; >> /var/log/syslog_size_alerts.log
```

---

## Summary Checklist

| Priority | Action | Command / File |
|----------|--------|----------------|
| 1 | Verify SSSD debug level ≤ 2 | `/etc/sssd/sssd.conf` |
| 2 | Confirm Docker uses `json-file` driver | `/etc/docker/daemon.json` |
| 3 | Add `size 500M` to logrotate config | `/etc/logrotate.d/rsyslog` |
| 4 | Enable rsyslog rate limiting | `/etc/rsyslog.conf` |
| 5 | Set up cron-based size alert | `sudo crontab -e` |

---

## Related Files

| File | Purpose |
|------|---------|
| `/etc/sssd/sssd.conf` | SSSD configuration including debug levels |
| `/etc/docker/daemon.json` | Docker daemon logging driver settings |
| `/etc/logrotate.d/rsyslog` | Log rotation schedule and size limits |
| `/etc/rsyslog.conf` | rsyslog global configuration and rate limits |
| `/var/log/syslog` | Active system log |
| `/var/log/syslog.1` | Previous rotation of system log |

---

*Last updated: February 2026 | Platform: Ubuntu 24.04 LTS*
