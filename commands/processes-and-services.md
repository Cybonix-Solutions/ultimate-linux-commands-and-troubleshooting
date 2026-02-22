# Processes & Services

Commands for inspecting and controlling init/service managers across Linux and Solaris, plus reliable backup tooling references.

[⬅ Back to Main Index](README.md)

## Command: chkconfig

**Category:** Service management  
**Distros:** RHEL/CentOS 6 and earlier  
**Summary:** Lists SysV init services and runlevel enablement on legacy releases.

### Common usages

```bash
chkconfig --list                 # Show every service and the runlevels it starts in
chkconfig network on             # Enable the service in the default runlevels
```

### Tips & troubleshooting

- Requires root privileges; pair with `service <name> status` to confirm state after changing runlevels.
- On RHEL7+, move to `systemctl` equivalents.

## Command: kill

**Category:** Process control  
**Distros:** All  
**Summary:** Sends POSIX signals (default SIGTERM) to processes referenced by PID.

### Common usages

```bash
kill 10                                         # Terminate PID 10 with SIGTERM
kill -9 $(pidof stuck-proc)                     # Forcefully kill a hung command when graceful stop fails
```

### Tips & troubleshooting

- Always try `kill -15` or `kill -2` before `-9`; the latter skips cleanup and can leave stale locks.
- Use `ps -fp <pid>` or `systemctl status <service>` to confirm you are targeting the correct process.

## Command: poweroff

**Category:** System control  
**Distros:** All  
**Summary:** Initiates an immediate shutdown, halting the system after cleanly stopping services.

### Common usages

```bash
sudo poweroff                                  # Systemd-compatible shutdown shortcut
sudo systemctl poweroff                        # Equivalent explicit systemd invocation
```

### Tips & troubleshooting

- Always warn logged-in users (`wall "System powering off in 5 minutes"`) before executing on shared hosts.
- If the command hangs, check `journalctl -xe` to see which unit is blocking the poweroff transaction.

## Command: ps

**Category:** Process inspection  
**Distros:** All  
**Summary:** Takes a snapshot of running processes with flexible formatting and filtering options.

### Common usages

```bash
ps aux | more -10                               # Show every process and page through the first few entries
ps -ef --forest                                 # Tree view with parent/child relationships
```

### Tips & troubleshooting

- Add `-p <pid> -o pid,ppid,cmd` for precise monitoring without extra noise.
- Pair with `grep -v grep` or `pgrep` to isolate a single service inside large process lists.

## Command: reboot

**Category:** System control  
**Distros:** All  
**Summary:** Cleanly restarts the host by stopping services, unmounting filesystems, then triggering a hardware reboot.

### Common usages

```bash
sudo reboot                                    # Standard reboot sequence
sudo systemctl reboot --force                  # Skip inhibitors when recovery requires an immediate restart
```

### Tips & troubleshooting

- `systemctl reboot --message "Kernel panic follow-up"` annotates the journal with context for postmortems.
- Use `needs-restarting -r` (on RHEL) beforehand to confirm a reboot is actually required after updates.

## Command: rear

**Category:** Backup & recovery  
**Distros:** All (Relax-and-Recover)  
**Summary:** Automates bare-metal recovery images and backups, useful for scheduled DR exports.

### Common usages

```bash
sudo vi /etc/rear/local.conf              # Customize backup options
sudo rear -d -v mkbackup                  # Create a verbose backup archive
sudo rear mkrescue                        # Build a rescue ISO or image
```

### Tips & troubleshooting

- Mount the destination (e.g., `mount c1nfs10g:/flar_recovery /mnt`) before running `rear`.
- Schedule recurring jobs via cron:

```bash
0 22 * * 1-5 root /usr/sbin/rear mkrescue
0 23 * * 1-5 root /usr/sbin/rear -d -v mkbackup
```

- `tar -zcvf /home/recovery/<folder>-$(date +%y-%m-%d).tar.gz /home/recovery/<folder>` is a quick follow-up to archive created ISOs; remember to `chown admin:admin` on the outputs.
- When aggregating images from physical servers, copy the generated archives off-host (`scp admin@server:/home/recovery/*.gz /adm/flash/rhel_rear/`) before cleaning `/home/recovery`.

## Command: svcadm

**Category:** Service management  
**Distros:** Solaris  
**Summary:** Enables, disables, and refreshes SMF service instances with optional verbose output.

### Common usages

```bash
/usr/sbin/svcadm -v enable <service>     # Enable and start a service
/usr/sbin/svcadm -v restart <service>    # Restart with logging
/usr/sbin/svcadm -v clear <service>      # Clear maintenance state
```

### Tips & troubleshooting

- `-v` is invaluable to see SMF's reasoning when operations silently fail.
- Combine with `svcs -xv <service>` to inspect failure explanations after a restart.

## Command: svcs

**Category:** Service inspection  
**Distros:** Solaris  
**Summary:** Queries SMF to show service state, dependencies, and fault information.

### Common usages

```bash
svcs -a                          # List every service instance and state
svcs -lp <service>               # Show log location, dependencies, and FMRI
svcs -xv <service>               # Explain why a service is in maintenance
```

### Tips & troubleshooting

- Use `svcs -p <service>` to see associated PIDs.
- Pipe through `grep` to isolate disabled services needing remediation.

## Command: top

**Category:** Process monitoring
**Distros:** All
**Summary:** Interactive, real-time view of CPU, memory, and load statistics plus per-process details.

### Common usages

```bash
top | more                                   # Snapshot the header data without entering full-screen mode
top -b -n 1 | head -n 20                     # Batch mode for automation/log capture
```

### Tips & troubleshooting

- Press `1` to expand CPU utilization per core and `c` to show full command lines.
- When analyzing historic spikes, prefer `sar` or `pidstat`; `top` only shows the current moment.

## Command: systemctl

**Category:** Service management
**Distros:** All systemd-based (RHEL 7+, Ubuntu 16.04+, Debian 8+)
**Summary:** Controls the systemd system and service manager for starting, stopping, and inspecting services.

### Common usages

```bash
# Service management
systemctl start nginx              # Start service
systemctl stop nginx               # Stop service
systemctl restart nginx            # Restart service
systemctl reload nginx             # Reload config without restart
systemctl status nginx             # Status and recent logs
systemctl enable nginx             # Start on boot
systemctl disable nginx            # Don't start on boot
systemctl enable --now nginx       # Enable and start immediately
systemctl is-active nginx          # Check if running (for scripts)
systemctl is-enabled nginx         # Check boot status
systemctl mask nginx               # Prevent starting entirely
systemctl unmask nginx             # Remove mask

# Listing and inspection
systemctl list-units               # All loaded units
systemctl list-units --failed      # Failed units only
systemctl list-unit-files          # All unit files and states
systemctl list-dependencies nginx  # Dependency tree
systemctl show nginx               # All unit properties
systemctl cat nginx                # Show unit file contents

# System state
systemctl daemon-reload            # Reload unit files after editing
systemctl reboot                   # Reboot system
systemctl poweroff                 # Shutdown
systemctl isolate multi-user.target  # Switch to text mode
```

### Tips & troubleshooting

- After editing unit files, always run `daemon-reload` before restart.
- `mask` is stronger than `disable`; prevents manual start too.
- Use `--user` for user-level services.
- SSH service is `sshd` on RHEL, `ssh` on Ubuntu.

## Command: journalctl

**Category:** Log management
**Distros:** All systemd-based (RHEL 7+, Ubuntu 16.04+, Debian 8+)
**Summary:** Queries the systemd journal for structured logs from services, kernel, and system.

### Common usages

```bash
# Basic queries
journalctl                         # All logs (oldest first)
journalctl -f                      # Follow live (like tail -f)
journalctl -n 100                  # Last 100 entries
journalctl -r                      # Reverse order (newest first)
journalctl -k                      # Kernel messages only (like dmesg)
journalctl -b                      # Current boot only
journalctl -b -1                   # Previous boot
journalctl --list-boots            # List recorded boots

# Filtering
journalctl -u nginx                # Specific unit
journalctl -u nginx -u php-fpm     # Multiple units
journalctl _PID=1234               # Specific PID
journalctl _UID=1000               # Specific user
journalctl -p err                  # Priority: emerg,alert,crit,err,warning,notice,info,debug
journalctl -p err..warning         # Priority range
journalctl --since "1 hour ago"    # Time-based
journalctl --since "2024-01-15 10:00" --until "2024-01-15 12:00"

# Output and maintenance
journalctl -o json-pretty          # JSON output
journalctl --no-pager              # Don't page output
journalctl --disk-usage            # Space used by journal
journalctl --vacuum-time=7d        # Delete logs older than 7 days
journalctl --vacuum-size=500M      # Shrink journal to 500M
```

### Tips & troubleshooting

- Use `-xe` for recent errors with explanations.
- `journalctl -u service --since "10 min ago"` is essential for debugging.
- Journal survives reboots if persistent storage is enabled (`/var/log/journal/`).

## Command: htop

**Category:** Process monitoring
**Distros:** All (htop package)
**Summary:** Interactive process viewer with visual CPU/memory meters and mouse support.

### Common usages

```bash
htop                               # Launch interactive viewer
htop -u username                   # Filter by user
htop -p 1234,5678                  # Monitor specific PIDs
htop -t                            # Tree view by default
```

### Tips & troubleshooting

- Press F2 for setup, F3 to search, F4 to filter, F5 for tree view, F9 to kill.
- Press `H` to hide user threads, `K` to hide kernel threads.
- Install: `apt install htop` (Ubuntu) or `dnf install htop` (RHEL).

## Command: lsof

**Category:** Process inspection
**Distros:** All
**Summary:** Lists open files, network connections, and file descriptors by process.

### Common usages

```bash
lsof -u username                   # Files opened by user
lsof -c nginx                      # Files opened by process name
lsof -p 1234                       # Files opened by PID
lsof /var/log/syslog               # Processes using this file
lsof +D /var/log                   # Processes using this directory
lsof -i                            # All network connections
lsof -i :80                        # Connections on port 80
lsof -i tcp                        # TCP connections only
lsof -i @192.168.1.1               # Connections to/from IP
lsof -i -s TCP:LISTEN              # Listening sockets only
lsof +L1                           # Deleted files still open
```

### Tips & troubleshooting

- Find what's holding a deleted file: `lsof +L1`.
- Find why you can't unmount: `lsof +D /mnt/usb`.
- "Too many open files" error? Check count: `lsof -u user | wc -l`.

## Command: strace

**Category:** Process debugging
**Distros:** All
**Summary:** Traces system calls and signals to debug process behavior and failures.

### Common usages

```bash
strace ls                          # Trace a command
strace -p 1234                     # Attach to running process
strace -f command                  # Follow child processes (forks)
strace -e open command             # Trace only specific syscalls
strace -e trace=file command       # File-related syscalls
strace -e trace=network command    # Network syscalls
strace -e trace=process command    # Process management syscalls
strace -c command                  # Summary statistics
strace -o output.log command       # Write to file
strace -t command                  # Add timestamps
strace -T command                  # Show time spent in syscalls
```

### Tips & troubleshooting

- Process hanging? `strace -p PID` shows what it's waiting for.
- Permission denied? strace shows the exact path being accessed.
- `-f` is essential for multi-process applications.

## Command: iotop

**Category:** I/O monitoring
**Distros:** All (iotop package)
**Summary:** Top-like I/O monitor showing per-process disk read/write activity.

### Common usages

```bash
iotop                              # Interactive view
iotop -o                           # Only show processes with active I/O
iotop -b                           # Batch mode (non-interactive)
iotop -a                           # Accumulated I/O since start
iotop -p 1234                      # Monitor specific PID
```

### Tips & troubleshooting

- Requires root privileges.
- Shows which process is causing disk thrashing.
- Install: `apt install iotop` (Ubuntu) or `dnf install iotop` (RHEL).

## Command: pgrep / pkill

**Category:** Process control
**Distros:** All
**Summary:** Searches for processes by name and optionally sends signals to them.

### Common usages

```bash
pgrep nginx                        # Show PIDs matching name
pgrep -l nginx                     # Show PID and name
pgrep -a nginx                     # Show PID and full command
pgrep -u root                      # Processes owned by root
pgrep -f "python script.py"        # Match full command line
pgrep -c nginx                     # Count matches
pkill nginx                        # Kill by name (SIGTERM)
pkill -9 nginx                     # Kill by name (SIGKILL)
pkill -HUP nginx                   # Send SIGHUP (reload)
pkill -u username                  # Kill all user's processes
```

### Tips & troubleshooting

- Safer than `killall` due to more precise matching options.
- Use `-f` when process name differs from command (e.g., Python scripts).
- Use `pgrep -a` to verify matches before using `pkill`.
