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
