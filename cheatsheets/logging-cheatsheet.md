# Logging & Journald Cheatsheet

Fast references for legacy log locations and `journalctl` filters on RHEL/systemd-based systems.

[⬅ Back to Main Index](README.md)

## Topic: Classic `/var/log` Files

| Path | Quick query |
|------|-------------|
| `/var/log/messages` | `grep -i "kernel:.*error" /var/log/messages` |
| `/var/log/secure` | `awk '$3=="sshd" && /Failed/' /var/log/secure` |
| `/var/log/cron` | `grep "$(date +%b' '%d)" /var/log/cron` |
| Archives (`*.gz`) | `zgrep -i panic /var/log/messages-*.gz` |
| Follow live | `tail -F /var/log/secure` |

- Pair `less +F` with sudo for a scrollable follow mode that you can exit with `Ctrl+C`.

## Topic: `journalctl` Filters

| Goal | Command | Notes |
|------|---------|-------|
| Jump to newest | `journalctl -e --no-pager` | `-e` starts at the end. |
| Previous boot | `journalctl -b -1` | `-b` counts from current boot = 0. |
| Between dates | `journalctl --since "2025-06-20" --until "2025-06-25"` | Natural language works (`"2 hours ago"`). |
| By service | `journalctl -u sshd` | Add `--follow` to tail live. |
| By PID | `journalctl _PID=1234` | Underscore fields are journal keys. |
| Errors only | `journalctl -p err..alert` | Range syntax for priorities. |
| Keyword search | `journalctl | grep -Ei "disk|nvme"` | Useful with any pipe. |
| Kernel ring buffer | `journalctl -k -p warning` | Replaces `dmesg` for persistent logs. |
| Disk usage summary | `journalctl --disk-usage` | Shows on-disk footprint. |
| Export sample | `journalctl -u firewalld --since yesterday > firewalld.log` | Handy for ticket uploads. |
| JSON for scripts | `journalctl -o json-pretty -n 50` | Pipe to `jq` for parsing. |

## Topic: SELinux & Firewall Quick Checks

- `sealert -a /var/log/audit/audit.log` → human-readable suggestions for AVCs.
- `journalctl -u firewalld -g "IN=eth0"` → live firewall log view filtered for an interface.
