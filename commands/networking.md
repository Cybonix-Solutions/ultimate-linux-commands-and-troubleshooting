# Networking Commands

Diagnostic and maintenance commands for time synchronization, connectivity checks, and related network services.

[⬅ Back to Main Index](README.md)

## Command: ntpdate

**Category:** Time sync  
**Distros:** All  
**Summary:** Queries an NTP server for the correct time (or steps the local clock when run as root).

### Common usages

```bash
ntpdate -q <server>                # Query only; does not set the clock
sudo ntpdate <server>              # Force-sync local clock immediately
```

### Tips & troubleshooting

- Inspect `/etc/ntp.conf` to confirm the servers you expect are configured; `grep -v '^#' /etc/ntp.conf` strips comments for a quick read.
- Prefer `chronyc tracking` for modern chrony deployments, but `ntpdate -q` is still handy when debugging legacy nodes.
