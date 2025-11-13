# Filesystem and Storage Commands

Reference commands for inspecting disks, verifying filesystems, and spotting space hogs quickly.

[⬅ Back to Main Index](README.md)

## Command: badblocks

**Category:** Filesystems  
**Distros:** All  
**Summary:** Scans a block device for unreadable sectors without modifying data when run in read-only mode.

### Common usages

```bash
sudo badblocks -v /dev/sda1          # Verbose read-only scan (safe on mounted volumes)
sudo badblocks -sw /dev/sdb          # Destructive write-mode test (only on empty disks)
```

### Tips & troubleshooting

- Always prefer the `-v` read-only check on mounted filesystems (`-sw` will destroy data).
- Pair with `smartctl` output to decide whether to schedule maintenance or a proactive replacement.

## Command: du

**Category:** Filesystems  
**Distros:** All  
**Summary:** Summarizes disk usage per file or directory so you can quickly identify the largest consumers.

### Common usages

```bash
sudo du -a /dir/ | sort -n -r | head -n 20      # Show top 20 space hogs underneath /dir
sudo du -sh /var/log/*                          # Human-readable size per log directory
```

### Tips & troubleshooting

- Redirect errors (e.g., `2>/dev/null`) when scanning `/` to avoid permission noise.
- Combine with `find ... -delete` only after validating that the reported directories are safe to clean.

## Command: fsck

**Category:** Filesystems  
**Distros:** All  
**Summary:** Checks and repairs filesystem metadata inconsistencies such as orphaned inodes or directory corruption.

### Common usages

```bash
sudo fsck -f /dev/sda1       # Force a check even if the filesystem appears clean
sudo fsck -n /dev/sdb1       # Report issues without modifying anything
```

### Tips & troubleshooting

- Never run `fsck` against a mounted, in-use root filesystem—boot from rescue media or switch to single-user mode.
- Use after `smartctl`/`badblocks` confirm the underlying media is healthy; otherwise prioritize data recovery.

## Command: smartctl

**Category:** Filesystems  
**Distros:** All  
**Summary:** Reads S.M.A.R.T. telemetry from disks and can launch self-tests to predict impending failures.

### Common usages

```bash
sudo apt install smartmontools                 # Ubuntu/Debian install
sudo smartctl -H /dev/sda                      # Overall drive health check
sudo smartctl -t short /dev/sda                # Quick self-test (minutes)
sudo smartctl -t long /dev/sda                 # Extended self-test (hours)
```

### Tips & troubleshooting

- Kick off a `short` test first; escalate to `long` when you can spare the IO window.
- Review error counters (`smartctl -a /dev/sda`) before scheduling maintenance or evacuating data.
