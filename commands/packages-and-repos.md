# Package & Repository Commands

Commands that help locate packages, manage firmware updates, and keep systems in sync with upstream repositories.

[⬅ Back to Main Index](README.md)

## Command: apt-file

**Category:** Package search  
**Distros:** Debian/Ubuntu  
**Summary:** Searches the APT package index for the package providing a given file path or pattern.

### Common usages

```bash
sudo apt update && sudo apt install apt-file    # Install the search helper
sudo apt-file update                            # Sync its index (separate from apt)
apt-file search <filename_pattern>              # Find which package ships the file
```

### Tips & troubleshooting

- Run `apt-file update` after every `apt update`; it maintains its own cache.
- Use anchored patterns (`usr/bin/foo$`) to avoid noisy hits.

## Command: fwupdmgr

**Category:** Firmware updates  
**Distros:** All (fwupd-supported hardware)  
**Summary:** Queries the LVFS to see if the system firmware has updates queued.

### Common usages

```bash
fwupdmgr get-devices           # Inventory supported hardware
fwupdmgr get-updates           # Show pending updates
fwupdmgr update                # Apply all applicable updates
```

### Tips & troubleshooting

- Ensure `fwupd` service is running; on servers without GUI you may need to start it manually.
- Updates usually require a reboot; schedule maintenance windows accordingly.

## Command: yum

**Category:** Package management  
**Distros:** RHEL/CentOS/Fedora (DNF-compatible)  
**Summary:** Installs, updates, or removes RPM packages while handling dependencies from configured repos.

### Common usages

```bash
sudo yum -y install net-tools                   # Pull in legacy toolkit (provides netstat, etc.)
sudo yum update                                 # Apply all available package updates
```

### Tips & troubleshooting

- Use `yum provides <file>` to discover which package ships a missing binary.
- `yum history undo <id>` quickly reverts a problematic transaction if a new package breaks workloads.
