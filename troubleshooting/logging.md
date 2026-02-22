# Logging & Syslog Runbooks

Investigations for runaway log growth, rsyslog issues, and log management problems.

[⬅ Back to Main Index](README.md)

## Scenario: Runaway syslog growth (100GB+ files)

**Symptoms:** `/var/log/syslog.1` grows to extreme sizes (100GB+) in hours, disk fills up, services fail.
**Applies to:** Ubuntu 24.04 LTS workstations and servers running rsyslog, Docker, SSSD, and/or YubiKey/MFA.

### Investigation

1. Sample the end of the log without loading the full file:

```bash
sudo tail -n 100 /var/log/syslog.1
```

2. Identify top logging sources by process name:

```bash
sudo grep -oP '^\S+ \S+ \S+' /var/log/syslog.1 | sort | uniq -c | sort -rn | head -20
```

3. Check what has been logging most heavily in the last hour:

```bash
sudo journalctl --since "1 hour ago" | awk '{print $5}' | sort | uniq -c | sort -rn | head -20
```

4. Monitor live log rate (lines per second):

```bash
sudo tail -f /var/log/syslog | pv -l -i 5 > /dev/null
```

### Root Causes

| Cause | Description |
|-------|-------------|
| SSSD debug level elevated | `debug_level` left at 7-9 from troubleshooting generates millions of lines/hour |
| Docker syslog driver | Containers using `syslog` driver instead of `json-file` flood syslog on crash loops |
| Verbose app logging | Web/app service routing debug output through syslog |
| rsyslog feedback loop | Misconfigured rsyslog logging its own messages back to itself |
| Kernel/udev hardware spam | Flaky USB device (e.g., YubiKey) causing continuous udev messages |

### Resolution

**1. Check SSSD debug level (most common on MFA systems):**

```bash
grep -i debug_level /etc/sssd/sssd.conf
grep -rn debug_level /etc/sssd/conf.d/
```

Set to `1` or `2` for production:

```ini
[sssd]
debug_level = 1

[domain/yourdomain.com]
debug_level = 1
```

```bash
sudo systemctl restart sssd
```

**2. Audit Docker logging configuration:**

```bash
# Check daemon-level driver
cat /etc/docker/daemon.json | grep -i log

# Check per-container drivers
docker inspect $(docker ps -q) --format '{{.Name}}: {{.HostConfig.LogConfig.Type}}'
```

Switch to `json-file` with size limits in `/etc/docker/daemon.json`:

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "50m",
    "max-file": "3"
  }
}
```

```bash
sudo systemctl restart docker
```

**3. Harden logrotate with a size cap:**

Edit `/etc/logrotate.d/rsyslog` to add `size 500M`:

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

Test the config:

```bash
sudo logrotate --debug /etc/logrotate.d/rsyslog
```

**4. Enable rsyslog rate limiting:**

Add to `/etc/rsyslog.conf`:

```
# Rate limiting — max 200 messages per 5 seconds per process
$SystemLogRateLimitInterval 5
$SystemLogRateLimitBurst 200
```

```bash
sudo systemctl restart rsyslog
```

**5. Add a size alert via cron:**

```bash
sudo crontab -e
```

With mail configured:

```bash
*/30 * * * * find /var/log -name "syslog*" -size +1G -exec echo "WARNING: {} is oversized on $(hostname)" \; | mail -s "Syslog size alert" admin@yourdomain.com 2>/dev/null
```

Without mail (log to file):

```bash
*/30 * * * * find /var/log -name "syslog*" -size +1G -exec echo "$(date) WARNING: {} is oversized on $(hostname)" \; >> /var/log/syslog_size_alerts.log
```

### Prevention Checklist

| Priority | Action | File |
|----------|--------|------|
| 1 | Verify SSSD debug level ≤ 2 | `/etc/sssd/sssd.conf` |
| 2 | Confirm Docker uses `json-file` driver | `/etc/docker/daemon.json` |
| 3 | Add `size 500M` to logrotate config | `/etc/logrotate.d/rsyslog` |
| 4 | Enable rsyslog rate limiting | `/etc/rsyslog.conf` |
| 5 | Set up cron-based size alert | `sudo crontab -e` |
