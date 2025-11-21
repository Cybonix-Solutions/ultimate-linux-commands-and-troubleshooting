# User & Permission Commands

Create accounts, reset lockouts, and manage project-level group access with these admin-friendly snippets.

[⬅ Back to Main Index](README.md)

## Command: chage

**Category:** Account aging  
**Distros:** All  
**Summary:** Views or modifies password expiration metadata to enforce rotations or force resets.

### Common usages

```bash
sudo chage -l username             # List password expiry, warning, inactivity
sudo chage -d 0 username           # Force password change on next login
```

### Tips & troubleshooting

- Pair with `passwd username` to set a temporary password before `chage -d 0`.
- Use `chage -M 90 -W 7 username` to enforce a 90-day rotation with 7-day warnings.

## Command: chmod (setgid directories)

**Category:** Permissions  
**Distros:** All  
**Summary:** Applies the setgid bit so group-owned project directories automatically assign new files to the same group.

### Common usages

```bash
sudo mkdir -p /opt/myproject
sudo chown root:myproject /opt/myproject
sudo chmod 2775 /opt/myproject
```

### Tips & troubleshooting

- Verify with `ls -ld /opt/myproject`; the `rws` in the group field confirms the setgid bit.
- Ensure every collaborator is added to the group (`usermod -aG myproject user`) or they'll see permission denied.

## Command: faillock

**Category:** Authentication  
**Distros:** RHEL/CentOS 7+, Fedora  
**Summary:** Resets or inspects deny lists created by PAM faillock after repeated bad logins.

### Common usages

```bash
sudo faillock --user <acct> --reset     # Clear fail counts for a user
sudo faillock --user <acct>             # Show current failure stats
```

### Tips & troubleshooting

- Clear both `faillock` and `pam_tally2` counters on hybrid environments so legacy PAM stacks stay in sync.
- Review `/var/log/secure` (RHEL) or `/var/log/auth.log` (Debian) to confirm the lock source before resetting.

## Command: lslogins

**Category:** Account inventory  
**Distros:** All  
**Summary:** Summarizes account metadata, group membership, expiration, and login history.

### Common usages

```bash
lslogins --logins=0,500,jdoe --output=UID,USER,LAST-LOGIN,LAST-TTY,FAILED-LOGIN,FAILED-TTY
lslogins --user-accs --supp-groups --acc-expiration
lslogins <acctname>                            # Focused view for a single account
```

### Tips & troubleshooting

- Filter by UID ranges (e.g., `--logins=1000-60000`) to skip service accounts.
- Use `--json` when you need to feed the output to automation.

## Command: pam_tally2

**Category:** Authentication  
**Distros:** RHEL/CentOS 6, Debian derivatives  
**Summary:** Legacy counter for failed logins; still present on many long-lived servers.

### Common usages

```bash
sudo pam_tally2 --user <acct>           # Show failures
sudo pam_tally2 --user <acct> --reset   # Clear failures
```

### Tips & troubleshooting

- Clear both `pam_tally2` and `faillock` when unsure which stack enforced the lockout.
- Use the `--service` flag to scope to a PAM service (e.g., `sshd`).

## Command: useradd

**Category:** Account management  
**Distros:** All  
**Summary:** Creates new users and home directories; typically paired with `passwd`/`chage`.

### Common usages

```bash
sudo useradd -m username             # Create user with home directory
sudo passwd username                 # Set a temporary password
sudo chage -d 0 username             # Force password reset on first login
```

### Tips & troubleshooting

- Use `-s /bin/bash` or similar to set the default shell explicitly.
- Automate provisioning with `/etc/skel` templates for dotfiles.

## Command: usermod

**Category:** Group membership  
**Distros:** All  
**Summary:** Adjusts primary or supplementary groups so users inherit the correct access.

### Common usages

```bash
sudo usermod -g primary user                 # Change primary group
sudo usermod -G wheel,devops user            # Replace supplementary groups
sudo usermod -aG myproject user              # Append group(s) without dropping existing ones
```

### Tips & troubleshooting

- Remember `-a` only works together with `-G`; without it the previous supplementary list is overwritten.
- After group changes, tell the user to re-login or run `newgrp <group>` to pick up permissions immediately.

## Command: whoami

**Category:** Identity  
**Distros:** All  
**Summary:** Prints the effective username for the current shell, making it easy to confirm sudo/su context.

### Common usages

```bash
whoami                                          # Show your current login identity
sudo whoami                                     # Verify that sudo elevated you to root
```

### Tips & troubleshooting

- Combine with `id` to see UID/GID numbers and supplementary groups when debugging permission issues.
- Inside scripts, `whoami` helps gate dangerous actions (`[ "$(whoami)" = "root" ] || exit 1`).
