# System Information Commands - Suggested Addition

**Target:** commands/misc.md or commands/system-info.md (new file)
**Priority:** High

---

## uname

Print system information.

```bash
uname -a                           # All info
uname -r                           # Kernel release
uname -s                           # Kernel name
uname -m                           # Machine architecture (x86_64, aarch64)
uname -n                           # Hostname
uname -v                           # Kernel version details
```

**Tips:**
- Quick kernel version: `uname -r`
- Check if 64-bit: `uname -m` should show x86_64 or aarch64

---

## hostnamectl

Query and change system hostname (systemd).

```bash
hostnamectl                        # Show all hostname info
hostnamectl status                 # Same as above
hostnamectl set-hostname server01  # Set hostname
hostnamectl set-hostname --static server01
hostnamectl set-hostname --pretty "Production Server"
```

**Tips:**
- Changes are persistent (writes to /etc/hostname)
- Three types: static, pretty (human-readable), transient

---

## timedatectl

Control system time and timezone.

```bash
timedatectl                        # Show current settings
timedatectl list-timezones         # List available timezones
timedatectl set-timezone America/New_York
timedatectl set-ntp true           # Enable NTP sync
timedatectl set-time "2024-01-15 10:30:00"  # Manual time (NTP must be off)
timedatectl show                   # Machine-readable output
```

**Tips:**
- Always use NTP in production
- Check `timedatectl` if apps have timestamp issues

---

## uptime

System uptime and load averages.

```bash
uptime                             # Uptime + load averages
uptime -p                          # Pretty format (up 2 days, 3 hours)
uptime -s                          # Boot timestamp
```

**Tips:**
- Load averages: 1, 5, 15 minute averages
- Load = running + waiting processes; compare to CPU count

---

## free

Memory usage.

```bash
free                               # Memory in kilobytes
free -h                            # Human readable
free -m                            # Megabytes
free -g                            # Gigabytes
free -s 5                          # Repeat every 5 seconds
free -t                            # Show totals row
```

**Tips:**
- "available" column = usable memory (free + reclaimable cache)
- Low "available" (not just low "free") indicates memory pressure
- Buffer/cache is normal; Linux uses free RAM for disk cache

---

## lscpu

CPU architecture information.

```bash
lscpu                              # All CPU info
lscpu -e                           # Extended format (per-CPU)
lscpu --json                       # JSON output
```

**Tips:**
- Shows cores, threads, sockets, cache sizes, flags
- Check flags for virtualization: grep for vmx (Intel) or svm (AMD)

---

## lsblk

List block devices.

```bash
lsblk                              # Tree view of disks
lsblk -f                           # Show filesystems
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT # Custom columns
lsblk -d                           # Disks only (no partitions)
lsblk -b                           # Sizes in bytes
lsblk -J                           # JSON output
lsblk -p                           # Full device paths
```

**Tips:**
- Better than `fdisk -l` for quick disk overview
- Shows LVM, RAID, and loop devices hierarchically

---

## lspci

List PCI devices.

```bash
lspci                              # All PCI devices
lspci -v                           # Verbose
lspci -vv                          # Very verbose
lspci -k                           # Show kernel drivers
lspci -nn                          # Show vendor/device IDs
lspci | grep -i vga                # Graphics cards
lspci | grep -i net                # Network adapters
```

**Tips:**
- Use `-k` to verify drivers are loaded
- Vendor IDs help find drivers: `lspci -nn | grep Net`

---

## lsusb

List USB devices.

```bash
lsusb                              # All USB devices
lsusb -v                           # Verbose
lsusb -t                           # Tree view (hubs)
lsusb -d 1234:5678                 # Specific vendor:product
```

---

## dmesg

Kernel ring buffer messages.

```bash
dmesg                              # All kernel messages
dmesg -H                           # Human readable (pager)
dmesg -T                           # Human-readable timestamps
dmesg -w                           # Follow (like tail -f)
dmesg --level=err,warn             # Only errors and warnings
dmesg | grep -i usb                # USB-related messages
dmesg | tail -50                   # Recent messages
dmesg -c                           # Clear buffer (root)
```

**Tips:**
- First place to check after hardware issues
- `-T` converts boot-relative timestamps to wall clock
- Combines well with `journalctl -k` on systemd systems

---

## vmstat

Virtual memory statistics.

```bash
vmstat                             # One-time snapshot
vmstat 1                           # Every second
vmstat 1 10                        # Every second, 10 times
vmstat -s                          # Summary statistics
vmstat -d                          # Disk statistics
vmstat -w                          # Wide output
```

**Columns:**
- r: processes waiting for CPU
- b: processes in uninterruptible sleep (usually I/O)
- si/so: swap in/out (should be near 0)
- wa: CPU time waiting for I/O

---

## iostat

CPU and I/O statistics.

```bash
iostat                             # Basic CPU and disk stats
iostat -x                          # Extended disk stats
iostat -x 1                        # Every second
iostat -d sda                      # Specific device
iostat -p sda                      # Include partitions
iostat -m                          # Megabytes/sec
```

**Key columns (extended):**
- await: average I/O wait time (ms)
- %util: device saturation (100% = fully busy)

**Tips:**
- High await with high %util = disk bottleneck
- Part of `sysstat` package

---

## sar

System activity reporter (historical data).

```bash
sar                                # CPU usage today
sar -r                             # Memory usage
sar -b                             # I/O stats
sar -n DEV                         # Network interfaces
sar -d                             # Disk activity
sar -q                             # Load averages and queue
sar -f /var/log/sa/sa15            # Specific day (15th)
sar -s 09:00:00 -e 17:00:00        # Time range
```

**Tips:**
- Data collected by sadc cron job (sysstat package)
- Historical data in `/var/log/sa/` or `/var/log/sysstat/`
- Essential for post-mortem analysis
