# Process Debugging Commands - Suggested Addition

**Target:** commands/processes-and-services.md
**Priority:** High

---

## systemctl

Control the systemd system and service manager.

```bash
# Service management
systemctl start nginx              # Start service
systemctl stop nginx               # Stop service
systemctl restart nginx            # Restart service
systemctl reload nginx             # Reload config (no restart)
systemctl status nginx             # Status and recent logs
systemctl enable nginx             # Start on boot
systemctl disable nginx            # Don't start on boot
systemctl enable --now nginx       # Enable and start
systemctl is-active nginx          # Check if running
systemctl is-enabled nginx         # Check boot status
systemctl mask nginx               # Prevent starting entirely
systemctl unmask nginx             # Remove mask

# Listing and searching
systemctl list-units               # All loaded units
systemctl list-units --failed      # Failed units only
systemctl list-unit-files          # All unit files
systemctl list-dependencies nginx  # Dependency tree
systemctl show nginx               # All properties

# System state
systemctl daemon-reload            # Reload unit files
systemctl reboot                   # Reboot system
systemctl poweroff                 # Shutdown
systemctl suspend                  # Suspend to RAM
systemctl isolate multi-user.target # Switch to text mode
```

**Tips:**
- After editing unit files, always `daemon-reload`
- `mask` is stronger than `disable` (prevents manual start too)
- Use `--user` for user-level services

---

## journalctl

Query the systemd journal.

```bash
# Basic queries
journalctl                         # All logs
journalctl -f                      # Follow (like tail -f)
journalctl -n 100                  # Last 100 entries
journalctl -r                      # Reverse order (newest first)
journalctl -k                      # Kernel messages only (dmesg)
journalctl -b                      # Current boot only
journalctl -b -1                   # Previous boot
journalctl --list-boots            # List recorded boots

# Filtering
journalctl -u nginx                # Specific unit
journalctl -u nginx -u php-fpm    # Multiple units
journalctl _PID=1234               # Specific PID
journalctl _UID=1000               # Specific user
journalctl -p err                  # Priority (emerg,alert,crit,err,warning,notice,info,debug)
journalctl -p err..warning         # Priority range
journalctl --since "1 hour ago"    # Time-based
journalctl --since "2024-01-15 10:00" --until "2024-01-15 12:00"

# Output formats
journalctl -o json                 # JSON output
journalctl -o json-pretty          # Pretty JSON
journalctl -o short-iso            # ISO timestamps
journalctl --no-pager              # Don't page output

# Maintenance
journalctl --disk-usage            # Space used by journal
journalctl --vacuum-time=7d        # Delete logs older than 7 days
journalctl --vacuum-size=500M      # Shrink to 500M
```

**Tips:**
- Use `-xe` for recent errors with explanations
- `journalctl -u service --since "10 min ago"` is your debugging friend
- Journal survives reboots if persistent storage is enabled

---

## htop

Interactive process viewer.

```bash
htop                               # Launch interactive viewer
htop -u username                   # Filter by user
htop -p 1234,5678                  # Monitor specific PIDs
htop -d 5                          # Update every 0.5 seconds
htop -C                            # Monochrome mode
htop -t                            # Tree view by default
```

**Keybindings:**
- F2: Setup (customize display)
- F3: Search
- F4: Filter
- F5: Tree view
- F6: Sort by column
- F9: Kill process
- Space: Tag process
- u: Filter by user
- H: Hide user threads
- K: Hide kernel threads

**Tips:**
- Shows CPU per-core, memory bars, and load graphically
- Can send any signal to processes (F9)
- Install: `apt install htop` or `dnf install htop`

---

## lsof

List open files (and network connections).

```bash
lsof                               # All open files (huge output)
lsof -u username                   # Files opened by user
lsof -c nginx                      # Files opened by process name
lsof -p 1234                       # Files opened by PID
lsof /var/log/syslog               # Processes using file
lsof +D /var/log                   # Processes using directory
lsof -i                            # Network connections
lsof -i :80                        # Connections on port 80
lsof -i tcp                        # TCP connections only
lsof -i @192.168.1.1               # Connections to/from IP
lsof -i -s TCP:LISTEN              # Listening sockets only
lsof +L1                           # Deleted files still open
```

**Tips:**
- Find what's holding a deleted file: `lsof +L1`
- Find why you can't unmount: `lsof +D /mnt/usb`
- "Too many open files" → `lsof -u user | wc -l`

---

## strace

Trace system calls.

```bash
strace ls                          # Trace command
strace -p 1234                     # Attach to running process
strace -f command                  # Follow forks
strace -e open command             # Only specific syscalls
strace -e trace=file command       # File-related syscalls
strace -e trace=network command    # Network syscalls
strace -e trace=process command    # Process management
strace -c command                  # Summary statistics
strace -o output.log command       # Write to file
strace -t command                  # Timestamps
strace -T command                  # Time spent in syscalls
strace -s 200 command              # Longer string output
```

**Tips:**
- Process hanging? `strace -p PID` shows what it's waiting for
- Permission denied? strace shows the exact path being accessed
- `-f` is essential for multi-process apps

---

## ltrace

Trace library calls.

```bash
ltrace command                     # Trace library calls
ltrace -p 1234                     # Attach to process
ltrace -e malloc+free command      # Specific functions
ltrace -c command                  # Summary
ltrace -S command                  # Include syscalls
```

**Tips:**
- Useful when strace shows the syscall but not why it's called
- Shows glibc function calls

---

## perf

Performance analysis tool.

```bash
perf stat command                  # Basic performance stats
perf top                           # Live CPU usage by function
perf record -g command             # Record with call graphs
perf report                        # View recorded data
perf list                          # List available events
```

**Tips:**
- Powerful but complex; start with `perf top` or `perf stat`
- Requires kernel support and `linux-tools-generic` package

---

## pidstat

Per-process statistics.

```bash
pidstat                            # CPU stats per process
pidstat 1                          # Every second
pidstat -d                         # Disk I/O per process
pidstat -r                         # Memory stats
pidstat -u                         # CPU usage (default)
pidstat -p 1234                    # Specific PID
pidstat -C "nginx"                 # Match command name
```

**Tips:**
- Part of `sysstat` package
- More detailed than top for specific process analysis

---

## iotop

I/O monitoring per process.

```bash
iotop                              # Interactive view
iotop -o                           # Only show active I/O
iotop -b                           # Batch mode (non-interactive)
iotop -a                           # Accumulated I/O
iotop -p 1234                      # Specific PID
```

**Tips:**
- Requires root
- Shows which process is thrashing the disk
- Install: `apt install iotop` or `dnf install iotop`

---

## pgrep / pkill

Process grep and kill.

```bash
pgrep nginx                        # PIDs matching name
pgrep -l nginx                     # PID + name
pgrep -a nginx                     # PID + full command
pgrep -u root                      # Processes owned by root
pgrep -f "python script.py"        # Match full command line
pgrep -c nginx                     # Count matches
pkill nginx                        # Kill by name
pkill -9 nginx                     # SIGKILL by name
pkill -HUP nginx                   # Send SIGHUP
pkill -u username                  # Kill user's processes
```

**Tips:**
- Safer than `killall` (more precise matching)
- Use `-f` when process name doesn't match command
