# systemd Cheatsheet

High-frequency `systemctl` and `journalctl` commands for managing services and units.

[⬅ Back to Main Index](README.md)

## Topic: Service Lifecycle

| Command | Description |
|---------|-------------|
| `sudo systemctl status <unit>` | Show status, last logs, dependencies. |
| `sudo systemctl start <unit>` | Start a unit immediately. |
| `sudo systemctl stop <unit>` | Stop a unit. |
| `sudo systemctl restart <unit>` | Restart service and dependencies. |
| `sudo systemctl reload <unit>` | Reload config without a full restart (if supported). |
| `sudo systemctl enable --now <unit>` | Enable at boot and start immediately. |
| `sudo systemctl disable --now <unit>` | Disable at boot and stop right away. |

## Topic: Unit & Dependency Inspection

| Command | Description |
|---------|-------------|
| `systemctl list-unit-files --type=service` | Show installed services and enablement state. |
| `systemctl list-dependencies <unit>` | Display dependency tree. |
| `systemctl cat <unit>` | Show the full unit definition (including drop-ins). |
| `systemctl edit <unit>` | Create an override file under `/etc/systemd/system`. |

## Topic: Journald Queries

| Command | Description |
|---------|-------------|
| `journalctl -u <unit>` | Logs for a specific unit (oldest first). |
| `journalctl -u <unit> -f` | Follow live logs. |
| `journalctl -b -1` | Logs from the previous boot. |
| `journalctl --disk-usage` | Report journal storage usage. |
| `sudo journalctl --vacuum-time=7d` | Keep only the last 7 days of logs. |

- Use `systemd-analyze blame` to spot services that delayed boot, and `systemd-analyze critical-chain` for dependency timing diagrams.
