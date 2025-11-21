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

## Command: cat

**Category:** File inspection  
**Distros:** All  
**Summary:** Dumps file contents to stdout for quick checks or for piping into other commands.

### Common usages

```bash
cat /etc/system-release                        # Confirm distro/release quickly
cat foo.txt >> combined.log                    # Append one file's contents into another
```

### Tips & troubleshooting

- Pipe through `less` or `head` when the target file is large to avoid flooding the terminal.
- Use here-docs (`cat <<'EOF' > file`) to draft short config snippets without opening an editor.

## Command: cd

**Category:** Filesystem navigation  
**Distros:** All  
**Summary:** Changes the shell’s current working directory.

### Common usages

```bash
cd ~/projects/app                             # Jump into a project tree
cd -                                          # Toggle between the last two directories
```

### Tips & troubleshooting

- `cd ~user` is an easy way to jump into another user’s home if you have permissions.
- Prefer `pushd`/`popd` when you need to maintain a directory stack for automation scripts.

## Command: cp

**Category:** File copy  
**Distros:** All  
**Summary:** Copies files or directories into a new location, overwriting existing paths by default.

### Common usages

```bash
cp helloworld.txt helloworld.bak               # Create a quick backup copy
cp -a /etc/skel/. /home/newuser/               # Recursively copy while preserving ownership and modes
```

### Tips & troubleshooting

- Add `-i` to force a prompt before overwriting a file; scripts should instead write to a temp file first.
- Use `-r` for directories and `-a` when you must preserve timestamps/permissions during migrations.

## Command: du

**Category:** Filesystems  
**Distros:** All  
**Summary:** Summarizes disk usage per file or directory so you can quickly identify the largest consumers.

### Common usages

```bash
sudo du -a /dir/ | sort -n -r | head -n 20      # Show top 20 space hogs underneath /dir
sudo du -sh /var/log/*                          # Human-readable size per log directory
du -hsx * | sort -rh | head -10                 # Quick top 10 in the current directory
```

### Tips & troubleshooting

- Redirect errors (e.g., `2>/dev/null`) when scanning `/` to avoid permission noise.
- Combine with `find ... -delete` only after validating that the reported directories are safe to clean.

## Command: find

**Category:** File search  
**Distros:** All  
**Summary:** Walks directory trees to locate files by name, type, size, age, or other predicates.

### Common usages

```bash
sudo find / -name hostname                      # Locate files named “hostname” anywhere on the system
find /var/log -type f -mtime -1                 # Files in /var/log modified within the last day
```

### Tips & troubleshooting

- Quote search expressions containing wildcards (`-name '*.conf'`) so the shell does not expand them first.
- Scope with `-maxdepth` or `-path` to keep searches fast, then pipe to `xargs`/`-delete` once validated.

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

## Command: growisofs

**Category:** Optical media  
**Distros:** All  
**Summary:** Burns ISO images to DVD/Blu-ray drives and blanks rewritable media from the command line.

### Common usages

```bash
sudo growisofs -Z /dev/dvdrw -R -J /some/files              # Create a new ISO from a directory tree
sudo growisofs -dvd-compat -Z /dev/sr1=~/Downloads/image.iso # Burn an ISO to Blu-ray/DVD and close the disc
sudo dvd+rw-format -blank /dev/cdrw                          # Blank a rewritable DVD+RW
```

### Tips & troubleshooting

- Run as root; the tool needs direct device access and can fail under sudo if device permissions are restricted.
- Use `-dvd-compat` when writing once so the disc finalizes properly; omit it for appendable media.

## Command: grep

**Category:** Text search  
**Distros:** All  
**Summary:** Searches files or streams for lines matching a string or regular expression.

### Common usages

```bash
grep -n "Listen" /etc/httpd/conf/httpd.conf     # Show matching lines with numbers
journalctl -u sshd | grep -i "error"            # Filter service logs for case-insensitive hits
```

### Tips & troubleshooting

- Add `-R` to recurse through directories and `-E` for extended regex syntax.
- Redirect binary-safe data through `grep -a` when scanning files in `/proc` or other pseudo filesystems.

## Command: less

**Category:** Pager  
**Distros:** All  
**Summary:** Interactive pager for files or command output, with navigation/search controls.

### Common usages

```bash
less -N ~/.bashrc                               # Show line numbers alongside the file contents
journalctl -u nginx | less -S                   # View long lines without wrapping
```

### Tips & troubleshooting

- Use `/pattern` and `?pattern` to search forward/backward; press `n`/`N` to cycle through matches.
- `less +F file` tails a file until you hit `Ctrl+C`, then returns to normal navigation.

## Command: ls

**Category:** Filesystem navigation  
**Distros:** All  
**Summary:** Lists directory contents; output can be customized with flags for long or human-readable views.

### Common usages

```bash
ls                                               # Quick glance at the current directory
ls -lah /var/log                                 # Show permissions, owners, and human-readable sizes
```

### Tips & troubleshooting

- Combine `-a` to surface dotfiles and `-t`/`-r` to sort by mtime or reverse order.
- Pipe into `column -t` or `sort` when feeding the output to scripts.

## Command: more

**Category:** Pager  
**Distros:** All  
**Summary:** Simple pager that lets you read stdout a page or line at a time.

### Common usages

```bash
ls /etc | more -4                               # Page through directory listings four lines at a time
journalctl -u sshd | more                       # Quick pager for log output on minimal installs
```

### Tips & troubleshooting

- The `<SPACE>` key advances by a page and `<ENTER>` by one line; `q` quits immediately.
- Prefer `less` for bidirectional search, but `more` is universal and exists even on recovery shells.

## Command: mv

**Category:** File move  
**Distros:** All  
**Summary:** Moves or renames files and directories, replacing the destination when it already exists.

### Common usages

```bash
mv ./documents ./docs-bak                       # Rename/move a directory
mv documents/hithere.txt documents/new_hithere.txt
```

### Tips & troubleshooting

- Use `mv -i` or `mv -n` in scripts to avoid accidental overwrites.
- Moves within the same filesystem are instantaneous; cross-filesystem moves perform a copy + delete.

## Command: pwd

**Category:** Filesystem navigation  
**Distros:** All  
**Summary:** Prints the absolute path of the current working directory.

### Common usages

```bash
pwd                                             # Display the current location (shell prompt agnostic)
pwd -P                                          # Resolve symlinks to show the physical path
```

### Tips & troubleshooting

- Compare `pwd` with the `$PWD` environment variable when debugging script logic that changes directories.
- When a path contains spaces, wrap the output (`"$(pwd)"`) before passing it to other commands.

## Command: rm

**Category:** File removal  
**Distros:** All  
**Summary:** Deletes files or directories; recursive operations cannot be undone without backups.

### Common usages

```bash
rm hithere.txt                                  # Remove a single file
rm -rf ./documents                              # Recursively delete a directory tree
```

### Tips & troubleshooting

- Pair with `--one-file-system` and explicit paths when pruning mountpoints to avoid nuking remote shares.
- Set the `rm` alias to `rm -i` on shared bastion hosts so users get a safety prompt for each file.

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

## Command: tar

**Category:** Archiving  
**Distros:** All  
**Summary:** Creates or extracts archives, commonly with gzip or bzip2 compression.

### Common usages

```bash
tar cvzf docs.tar.gz documents/                 # Create a compressed archive
tar -xvf docs.tar.gz -C ./new-docs             # Extract into an existing directory
```

### Tips & troubleshooting

- `tar tzf docs.tar.gz` lets you inspect archive contents before extracting.
- Always target an empty directory with `-C` to avoid overwriting similarly named files.
