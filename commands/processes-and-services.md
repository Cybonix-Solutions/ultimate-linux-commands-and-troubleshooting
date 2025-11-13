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
