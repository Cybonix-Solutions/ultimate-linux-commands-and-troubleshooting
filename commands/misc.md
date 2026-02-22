# Miscellaneous Command References

Handy commands that do not warrant their own topical bucket but are still regular fixtures in day-to-day ops work.

[⬅ Back to Main Index](README.md)

## Command: && (AND operator)

**Category:** Shell chaining  
**Distros:** All  
**Summary:** Runs the next command only if the previous one exited with status 0, making quick mini-pipelines safer.

### Common usages

```bash
cd /etc && ls                                  # List /etc only if cd succeeded
dnf makecache && dnf upgrade                   # Skip the upgrade whenever metadata sync fails
```

### Tips & troubleshooting

- Contrast with `;`, which runs subsequent commands regardless of failure.
- In complex scripts, combine with `set -e` or explicit `if` blocks for clearer error handling.

## Command: clear

**Category:** Terminal UX  
**Distros:** All  
**Summary:** Resets the terminal display by sending ANSI escape sequences to redraw a blank screen.

### Common usages

```bash
clear                                          # Wipe the current terminal contents
printf '\033c'                                 # Alternative when `clear` is unavailable
```

### Tips & troubleshooting

- Use `Ctrl+L` (readline shortcut) for the same effect inside Bash without forking a process.
- `TERM=dumb clear` falls back to printing newlines when terminfo data cannot be loaded.

## Command: dmidecode

**Category:** Hardware info  
**Distros:** All  
**Summary:** Dumps SMBIOS data to reveal chassis make/model, serial numbers, and BIOS versions.

### Common usages

```bash
sudo dmidecode -t system            # Quick summary of vendor, product, serial, BIOS
sudo dmidecode -t memory            # Inspect DIMM population and speeds
```

### Tips & troubleshooting

- Requires root because it queries `/dev/mem`; run in change windows if production policies restrict it.
- Redirect output to a ticket for future audits (`sudo dmidecode -t system > /tmp/hw.txt`).
- On Solaris hosts without dmidecode, reach for `prtdiag`, `prtconf`, and `psrinfo` to capture comparable chassis and CPU data.

## Command: echo

**Category:** Shell helpers  
**Distros:** All  
**Summary:** Writes strings or variable values to stdout or redirects them into files.

### Common usages

```bash
echo "Hello World"                               # Print a literal string
echo "Hello World" > data.txt                    # Overwrite a file with new content
```

### Tips & troubleshooting

- Prefer `printf` when you need consistent escape handling across shells.
- Use `echo "$VAR"` (quoted) so spaces and wildcard characters are not reinterpreted.

## Command: env

**Category:** Environment inspection  
**Distros:** All  
**Summary:** Prints the current environment variables or runs a command with a modified environment.

### Common usages

```bash
env | more                                      # Review all exported variables
FOO=bar env bash -c 'echo $FOO'                 # Run a command with a temporary value
```

### Tips & troubleshooting

- Pipe into `grep` to locate a single variable quickly (`env | grep ^PATH=`).
- Remember `env -i` starts from a clean slate—great for debugging scripts that depend on inherited state.

## Command: export

**Category:** Environment management  
**Distros:** All  
**Summary:** Creates or updates environment variables so that child processes inherit the value.

### Common usages

```bash
export WEB_PAGE="https://www.redhat.com/en"     # Set a variable for the current session
export PATH="$HOME/.local/bin:$PATH"            # Prepend a directory to PATH
```

### Tips & troubleshooting

- Put persistent exports inside `~/.bash_profile` (login shells) or `~/.bashrc` (interactive shells).
- Use `unset VAR` to remove a value entirely rather than exporting an empty string.

## Command: fips-mode-setup

**Category:** Security hardening  
**Distros:** RHEL/CentOS 8/9  
**Summary:** Toggles FIPS 140-2 compliant crypto mode on supported RHEL systems.

### Common usages

```bash
sudo fips-mode-setup --enable          # Enable FIPS mode (requires reboot)
sudo fips-mode-setup --disable         # Disable and return to standard crypto policies
```

### Tips & troubleshooting

- Reboot after switching modes so the kernel boots with the correct crypto modules.
- Verify status with `fips-mode-setup --check` before and after maintenance windows.

## Command: gh

**Category:** Developer tooling  
**Distros:** All  
**Summary:** GitHub CLI used to authenticate, create repos, and push existing projects without opening a browser.

### Common usages

```bash
sudo apt install gh git                      # Install requirements on Ubuntu/Debian
gh auth login                                # Interactive device or SSH auth
gh repo create --source=. --public --push    # Publish current repo and push with remote origin
```

### Tips & troubleshooting

- Run `git init && git add . && git commit -m "Initial commit"` before `gh repo create --source=. --push`.
- Use `gh repo create --private` (or `--public`) explicitly to avoid interactive prompts in scripts.
- Follow up with the standard flow: `git status`, `git add`, `git commit -m "...`, `git push -u <branch>` for ongoing work.

## Command: grep (PCRE)

**Category:** Text processing  
**Distros:** All (requires GNU grep with PCRE support)  
**Summary:** Uses the `-P` (PCRE) and `\K` features to drop the matched prefix and output only the desired suffix.

### Common usages

```bash
grep -oP 'pattern\K.*' file.txt        # Print everything after 'pattern' on each matching line
grep -oP '(?<=pattern).*' file.txt     # Equivalent when your grep supports lookbehind
```

### Tips & troubleshooting

- `\K` is faster than variable-length lookbehind and works even when lookbehind is unsupported.
- Validate your grep build (`grep --version`) because BusyBox and macOS/BSD `grep` lack `-P`.

## Command: inxi

**Category:** Hardware inventory  
**Distros:** All  
**Summary:** Console system profiler that prints hardware, driver, and system stats in a single, readable report.

### Common usages

```bash
inxi -S                                    # OS, kernel, desktop info
sudo inxi -Fxxxz                           # Full hardware report with extra detail (omit -z to show serials)
inxi -m                                    # Memory slot population and speeds
```

### Tips & troubleshooting

- Run with sudo to expose disk, sensor, and memory details that require elevated permissions.
- Filter output by class (`inxi -N` for network, `inxi -D` for disks) when you only need one subsystem.

## Command: lsb_release

**Category:** System info  
**Distros:** Debian/Ubuntu family  
**Summary:** Reports the distribution release name, description, and codename via the LSB database.

### Common usages

```bash
lsb_release -a           # Show distributor ID, description, release, codename
lsb_release -cs          # Output only the codename (useful for apt sources)
```

### Tips & troubleshooting

- Install `lsb-release` package if the utility is missing.
- Use in scripts to branch logic for `jammy`, `focal`, etc.

## Command: man

**Category:** Documentation  
**Distros:** All  
**Summary:** Displays on-system manual pages, providing canonical syntax and flag descriptions for commands.

### Common usages

```bash
man cp                                           # Read the manual for cp
man 5 passwd                                     # Open a specific manual section
```

### Tips & troubleshooting

- Use `/pattern` inside `man` to search within the page; `n` jumps to the next match.
- `man -k keyword` (equivalent to `apropos`) searches page descriptions when you are unsure of the command name.

## Command: openssl x509

**Category:** TLS inspection  
**Distros:** All  
**Summary:** Displays certificate metadata so you can quickly confirm issuer, subject, SANs, and validity windows.

### Common usages

```bash
openssl x509 -in /etc/pki/katello/certs/katello-apache.crt -text -noout \
  | grep -E "Issuer:|Subject:|CA:|DNS:|Digital|Not Before|Not After"
```

### Tips & troubleshooting

- Add `-purpose sslserver` to validate intended usage or `-checkend 86400` to test expiry within the next day.
- When certificates chain incorrectly, compare the `Issuer`/`Subject` fields against the CA bundle you expect.

## Command: printenv

**Category:** Environment inspection  
**Distros:** All  
**Summary:** Outputs the value of specified environment variables without the extra formatting `env` provides.

### Common usages

```bash
printenv HOSTNAME                                # Display a single variable
printenv | sort                                  # Alphabetize the whole environment dump
```

### Tips & troubleshooting

- In scripts, guard against unset variables (`printenv VAR || echo "Missing VAR"`) so pipelines do not fail silently.
- Combine with `xargs` to pass values into other commands (`printenv HOME | xargs ls`).

## Command: source

**Category:** Shell helpers  
**Distros:** All  
**Summary:** Executes a script in the current shell so any exported variables or functions persist.

### Common usages

```bash
source ./new_vars.sh                             # Load environment tweaks without spawning a subshell
. /etc/profile                                   # POSIX-compatible shorthand for sourcing
```

### Tips & troubleshooting

- Remember that syntax errors in the sourced file abort your current shell when `set -e` is active—test in a subshell first.
- Use absolute paths in login scripts to avoid sourcing the wrong file when `pwd` changes mid-script.

## Command: growisofs

**Category:** Optical media
**Distros:** All
**Summary:** Burns ISO images to DVD or Blu-ray discs; handles the entire process including filesystem preparation.

### Common usages

```bash
# Install the tool (RHEL/CentOS)
sudo dnf install dvd+rw-tools

# Identify your optical drive
lsblk
sudo cdrecord --scanbus

# Burn ISO to Blu-ray/DVD with maximum compatibility
sudo growisofs -dvd-compat -Z /dev/sr0=rhel-9.6-x86_64-dvd.iso
```

### Tips & troubleshooting

- `-dvd-compat` closes the disc (unappendable) for maximum boot compatibility on other systems.
- `-Z /dev/sr0=` starts an initial session; replace `/dev/sr0` with your actual device.
- Verify after burning: mount the disc and list contents to confirm successful write.
- Single-layer Blu-ray = 25GB, dual-layer = 50GB; ensure ISO fits the media.
- Use `dmesg` to troubleshoot optical drive issues if burning fails.

## Command: which

**Category:** Path lookup
**Distros:** All
**Summary:** Shows the full path of the executable that the shell would run, honoring `$PATH` order.

### Common usages

```bash
which clear                                      # Reveal where a command lives on disk
which -a python3                                 # Display every matching executable in PATH order
```

### Tips & troubleshooting

- Alias-heavy environments may mask binaries; run `command -v <cmd>` for a POSIX-defined alternative.
- On hashed Bash commands, `hash -r` clears the cache so `which` reflects freshly installed executables.

## Command: uname

**Category:** System info
**Distros:** All
**Summary:** Prints system information including kernel version, architecture, and hostname.

### Common usages

```bash
uname -a                           # All system info
uname -r                           # Kernel release version
uname -s                           # Kernel name
uname -m                           # Machine architecture (x86_64, aarch64)
uname -n                           # Hostname
```

### Tips & troubleshooting

- Quick kernel check: `uname -r`.
- Check if 64-bit: `uname -m` should show x86_64 or aarch64.

## Command: hostnamectl

**Category:** System configuration
**Distros:** All systemd-based (RHEL 7+, Ubuntu 16.04+)
**Summary:** Queries and changes the system hostname persistently.

### Common usages

```bash
hostnamectl                        # Show all hostname info
hostnamectl status                 # Same as above
hostnamectl set-hostname server01  # Set static hostname
hostnamectl set-hostname --pretty "Production Server"
```

### Tips & troubleshooting

- Changes are persistent (writes to `/etc/hostname`).
- Three types: static (stored), pretty (human-readable), transient (temporary).

## Command: timedatectl

**Category:** System configuration
**Distros:** All systemd-based (RHEL 7+, Ubuntu 16.04+)
**Summary:** Controls system time, timezone, and NTP synchronization.

### Common usages

```bash
timedatectl                        # Show current settings
timedatectl list-timezones         # List available timezones
timedatectl set-timezone America/New_York
timedatectl set-ntp true           # Enable NTP sync
timedatectl set-time "2024-01-15 10:30:00"  # Manual time (NTP must be off)
```

### Tips & troubleshooting

- Always use NTP in production (`set-ntp true`).
- Check this first if applications have timestamp issues.

## Command: uptime

**Category:** System info
**Distros:** All
**Summary:** Shows how long the system has been running and current load averages.

### Common usages

```bash
uptime                             # Uptime and load averages
uptime -p                          # Pretty format (up 2 days, 3 hours)
uptime -s                          # Boot timestamp
```

### Tips & troubleshooting

- Load averages show 1, 5, 15 minute averages.
- Load = running + waiting processes; compare to CPU count for saturation.

## Command: free

**Category:** System info
**Distros:** All
**Summary:** Displays memory usage including RAM and swap.

### Common usages

```bash
free                               # Memory in kilobytes
free -h                            # Human readable (MB, GB)
free -m                            # Megabytes
free -g                            # Gigabytes
free -s 5                          # Repeat every 5 seconds
```

### Tips & troubleshooting

- "available" column = usable memory (free + reclaimable cache).
- Low "available" (not just "free") indicates real memory pressure.
- Buffer/cache usage is normal; Linux uses free RAM for disk cache.

## Command: lscpu

**Category:** Hardware info
**Distros:** All
**Summary:** Displays CPU architecture information including cores, threads, and cache.

### Common usages

```bash
lscpu                              # All CPU info
lscpu -e                           # Extended per-CPU format
lscpu --json                       # JSON output
```

### Tips & troubleshooting

- Shows cores, threads, sockets, cache sizes, and CPU flags.
- Check flags for virtualization: grep for vmx (Intel) or svm (AMD).

## Command: lsblk

**Category:** Hardware info
**Distros:** All
**Summary:** Lists block devices in a tree format showing disks, partitions, and mount points.

### Common usages

```bash
lsblk                              # Tree view of block devices
lsblk -f                           # Show filesystems and UUIDs
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT # Custom columns
lsblk -d                           # Disks only (no partitions)
lsblk -J                           # JSON output
lsblk -p                           # Show full device paths
```

### Tips & troubleshooting

- Better than `fdisk -l` for quick disk overview.
- Shows LVM, RAID, and loop devices hierarchically.

## Command: lspci

**Category:** Hardware info
**Distros:** All
**Summary:** Lists PCI devices including network cards, GPUs, and storage controllers.

### Common usages

```bash
lspci                              # All PCI devices
lspci -v                           # Verbose output
lspci -k                           # Show kernel drivers in use
lspci -nn                          # Show vendor/device IDs
lspci | grep -i vga                # Graphics cards
lspci | grep -i net                # Network adapters
```

### Tips & troubleshooting

- Use `-k` to verify correct drivers are loaded.
- Vendor IDs help find drivers: `lspci -nn | grep Network`.

## Command: lsusb

**Category:** Hardware info
**Distros:** All
**Summary:** Lists USB devices connected to the system.

### Common usages

```bash
lsusb                              # All USB devices
lsusb -v                           # Verbose output
lsusb -t                           # Tree view showing hubs
lsusb -d 1234:5678                 # Filter by vendor:product
```

### Tips & troubleshooting

- Use after plugging in a device to verify it's detected.
- Check `dmesg | tail` for driver loading messages after USB connect.

## Command: dmesg

**Category:** System diagnostics
**Distros:** All
**Summary:** Prints kernel ring buffer messages showing hardware events and driver output.

### Common usages

```bash
dmesg                              # All kernel messages
dmesg -H                           # Human readable with pager
dmesg -T                           # Human-readable timestamps
dmesg -w                           # Follow live (like tail -f)
dmesg --level=err,warn             # Only errors and warnings
dmesg | grep -i usb                # USB-related messages
dmesg | tail -50                   # Recent messages
```

### Tips & troubleshooting

- First place to check after hardware issues or driver problems.
- `-T` converts boot-relative timestamps to wall clock time.
- On systemd systems, `journalctl -k` provides similar output with better filtering.

## Command: vmstat

**Category:** Performance monitoring
**Distros:** All
**Summary:** Reports virtual memory statistics including CPU, memory, and I/O.

### Common usages

```bash
vmstat                             # One-time snapshot
vmstat 1                           # Update every second
vmstat 1 10                        # Every second, 10 iterations
vmstat -s                          # Summary statistics
vmstat -d                          # Disk statistics
```

### Tips & troubleshooting

- Key columns: r (processes waiting for CPU), b (blocked on I/O), si/so (swap in/out).
- High si/so indicates memory pressure and swapping.
- wa column shows CPU time waiting for I/O.

## Command: iostat

**Category:** Performance monitoring
**Distros:** All (sysstat package)
**Summary:** Reports CPU and disk I/O statistics for performance analysis.

### Common usages

```bash
iostat                             # Basic CPU and disk stats
iostat -x                          # Extended disk stats
iostat -x 1                        # Extended stats every second
iostat -d sda                      # Specific device only
iostat -m                          # Show throughput in MB/sec
```

### Tips & troubleshooting

- Key columns (extended): await (I/O wait time ms), %util (device saturation).
- High await with high %util = disk bottleneck.
- Install: `apt install sysstat` (Ubuntu) or `dnf install sysstat` (RHEL).

## Command: sar

**Category:** Performance monitoring
**Distros:** All (sysstat package)
**Summary:** Collects and reports system activity including historical data.

### Common usages

```bash
sar                                # CPU usage today
sar -r                             # Memory usage
sar -b                             # I/O statistics
sar -n DEV                         # Network interface stats
sar -d                             # Disk activity
sar -q                             # Load averages and queue
sar -f /var/log/sa/sa15            # Specific day (15th)
sar -s 09:00:00 -e 17:00:00        # Time range
```

### Tips & troubleshooting

- Data collected by sadc cron job when sysstat is enabled.
- Historical data in `/var/log/sa/` (RHEL) or `/var/log/sysstat/` (Ubuntu).
- Essential for post-mortem analysis of performance issues.
