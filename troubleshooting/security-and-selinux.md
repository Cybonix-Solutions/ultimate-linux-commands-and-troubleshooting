# Security & SELinux Runbooks

Recovery guides for auth issues, SELinux blocks, and related security tooling.

[⬅ Back to Main Index](README.md)

## Scenario: Reset forgotten root password via GRUB (`rd.break`)

**Symptoms:** Root password unknown, console access available, need to regain control.  
**Applies to:** RHEL/CentOS 6–8 with GRUB access (physical or virtual).

### Investigation
1. Reboot and interrupt GRUB by tapping the arrow keys so the countdown pauses.
2. Highlight the desired kernel and press `e` to edit the boot entry.
3. Find the kernel line (starts with `linux16` on RHEL7, `linux` on RHEL8) and append `rd.break` to the end.
4. Press `Ctrl+X` to boot into the temporary rescue prompt (`switch_root:/#`).

### Resolution
- Remount the real root filesystem read/write and chroot into it:

```bash
mount -o remount,rw /sysroot
chroot /sysroot
```

- Reset the password, then flag SELinux to relabel on reboot:

```bash
passwd root
touch /.autorelabel
```

- Type `exit` to leave the chroot, then run `reboot`. SELinux relabeling may take several minutes on large filesystems; let it finish before logging back in.
